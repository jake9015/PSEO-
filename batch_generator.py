#!/usr/bin/env python3
"""
PSEO Batch Generator - Phased Rollout Script
=============================================

Generates PSEO landing pages in controlled batches following the 6-week rollout strategy.

This module implements production-scale batch processing with checkpointing, error recovery,
and phased rollout capabilities. It uses the PSEOOrchestrator to generate pages and exports
results to WordPress-compatible CSV and JSON formats.

Rollout Phases:
---------------
- Week 1: 10 high-priority pages (manual QA)
- Week 2: 50 pages (patterns 1 & 4)
- Week 3: 200 pages (patterns 1, 4, 6, 2)
- Week 4-6: All remaining pages (~418 pages)

Features:
---------
- Checkpoint system (saves every 10 pages)
- Resume from interruption
- Failed task logging
- CSV and JSON export
- Variable combination generation

⚠️  IMPORTANT: Update COMPETITORS, PLATFORMS, AUDIENCES lists to match config/variables.json

Usage:
------
    # Test with single page
    python batch_generator.py --phase week_1 --limit 1

    # Generate Week 1 (10 pages)
    python batch_generator.py --phase week_1

    # Resume from checkpoint
    python batch_generator.py --phase week_2 --start-index 10
"""

import asyncio
import json
import pandas as pd
from typing import List, Dict
from datetime import datetime
import argparse
from pseo_orchestrator import PSEOOrchestrator
import os
from dotenv import load_dotenv

# ⚠️ IMPORTANT: Variable lists are now loaded from config/variables.json
# This prevents duplication and ensures consistency across the codebase.
# To add new competitors/platforms/audiences, update config/variables.json instead of here.

# Pattern Combinations - Maps to patterns.json
PATTERN_DEFINITIONS = {
    "1": {
        "name": "Competitor Comparison",
        "variables": ["competitor", "audience"],
        "priority": "HIGH"
    },
    "2": {
        "name": "Best Tool",
        "variables": ["tool_type", "audience", "platform"],
        "priority": "MEDIUM"
    },
    "3": {
        "name": "Direct Tool",
        "variables": ["tool_type", "use_case"],
        "priority": "MEDIUM"
    },
    "4": {
        "name": "Alternative",
        "variables": ["competitor", "audience"],
        "priority": "HIGH"
    },
    "5": {
        "name": "Review",
        "variables": ["competitor", "audience"],
        "priority": "MEDIUM"
    },
    "6": {
        "name": "Content Crisis",
        "variables": ["audience"],
        "priority": "HIGH"
    }
}

# Phased Rollout Schedule
ROLLOUT_PHASES = {
    "week_1": {
        "patterns": ["1"],
        "limit": 10,
        "priority_filter": "HIGH",
        "specific_combos": [
            {"competitor": "Higgsfield", "audience": "OnlyFans Agencies"},
            {"competitor": "Midjourney", "audience": "OnlyFans Creators"},
            {"competitor": "Krea", "audience": "OnlyFans Agencies"},
            {"competitor": "Higgsfield", "audience": "Content Creators"},
            {"competitor": "Midjourney", "audience": "OnlyFans Agencies"},
            {"competitor": "Runway", "audience": "OnlyFans Creators"},
            {"competitor": "Leonardo AI", "audience": "OnlyFans Agencies"},
            {"competitor": "Stability AI", "audience": "OnlyFans Creators"},
            {"competitor": "Krea", "audience": "Content Creators"},
            {"competitor": "Civitai", "audience": "OnlyFans Creators"}
        ]
    },
    "week_2": {
        "patterns": ["1", "4"],
        "limit": 50,
        "priority_filter": "HIGH"
    },
    "week_3": {
        "patterns": ["1", "4", "6", "2"],
        "limit": 200,
        "priority_filter": None
    },
    "week_4_6": {
        "patterns": ["1", "2", "3", "4", "5", "6"],
        "limit": None,  # All remaining
        "priority_filter": None
    }
}


class PSEOMatrixGenerator:
    """
    Generates the complete PSEO page matrix from patterns and variables.

    Loads variable lists from config/variables.json to ensure consistency
    across the codebase and prevent duplication.
    """

    def __init__(self, variables_config: Dict = None):
        """
        Initialize matrix generator with variables from config.

        Args:
            variables_config: Optional pre-loaded variables config.
                            If None, will load from config/variables.json
        """
        # Load variables from config file if not provided
        if variables_config is None:
            config_path = os.path.join('config', 'variables.json')
            with open(config_path, 'r') as f:
                variables_config = json.load(f)

        # Extract 'all' lists from each variable category in config
        self.variables = {
            "competitor": variables_config.get('competitors', {}).get('all', []),
            "platform": variables_config.get('platforms', {}).get('all', []),
            "audience": variables_config.get('audiences', {}).get('all', []),
            "use_case": variables_config.get('use_cases', {}).get('all', []),
            "tool_type": variables_config.get('tool_types', {}).get('all', []),
            # Note: pain_points not in variables.json, keeping minimal default
            "pain_point": [
                "Creator Burnout", "Content Bottleneck", "Revenue Instability"
            ]
        }

        # Validate that we loaded variables successfully
        if not self.variables.get("competitor"):
            print("⚠️ Warning: No competitors loaded from config")
        if not self.variables.get("platform"):
            print("⚠️ Warning: No platforms loaded from config")

    def generate_matrix(self, patterns: List[str] = None) -> pd.DataFrame:
        """Generate all possible page combinations"""

        if patterns is None:
            patterns = PATTERN_DEFINITIONS.keys()

        all_combinations = []

        for pattern_id in patterns:
            if pattern_id not in PATTERN_DEFINITIONS:
                print(f"⚠️ Unknown pattern: {pattern_id}")
                continue

            pattern = PATTERN_DEFINITIONS[pattern_id]
            required_vars = pattern["variables"]

            # Generate all combinations for this pattern
            combos = self._generate_combinations(pattern_id, required_vars)
            all_combinations.extend(combos)

        df = pd.DataFrame(all_combinations)
        print(f"✓ Generated matrix: {len(df)} total page combinations")

        return df

    def _generate_combinations(self, pattern_id: str, required_vars: List[str]) -> List[Dict]:
        """
        Generate all combinations for a specific pattern.

        This method creates a Cartesian product of all variable lists required
        by a pattern. For example, if a pattern needs ['competitor', 'audience']
        and we have 15 competitors and 8 audiences, this generates 15 × 8 = 120 pages.

        Args:
            pattern_id: The pattern ID (e.g., '1' for Competitor Comparison)
            required_vars: List of variable names needed (e.g., ['competitor', 'audience'])

        Returns:
            List of dicts, each representing one page's variables

        Example:
            Input: pattern_id='1', required_vars=['competitor', 'audience']
            Output: [
                {'pattern_id': '1', 'priority': 'HIGH', 'competitor': 'Higgsfield', 'audience': 'Creators'},
                {'pattern_id': '1', 'priority': 'HIGH', 'competitor': 'Higgsfield', 'audience': 'Agencies'},
                ...
            ]
        """
        import itertools

        # Get variable lists from loaded config
        # e.g., if required_vars = ['competitor', 'audience'], get both lists
        var_lists = [self.variables.get(var, []) for var in required_vars]

        # Check for empty variable lists (indicates config issue)
        if any(len(vlist) == 0 for vlist in var_lists):
            print(f"⚠️ Missing variables for pattern {pattern_id}: {required_vars}")
            print(f"   Available: {list(self.variables.keys())}")
            return []

        # Generate Cartesian product (all possible combinations)
        # itertools.product(['A', 'B'], ['X', 'Y']) → [('A','X'), ('A','Y'), ('B','X'), ('B','Y')]
        combos = []
        for combo in itertools.product(*var_lists):
            # Map variable names to values: ('Higgsfield', 'Creators') → {'competitor': 'Higgsfield', 'audience': 'Creators'}
            variables = dict(zip(required_vars, combo))

            # Add pattern metadata
            combos.append({
                "pattern_id": pattern_id,
                "priority": PATTERN_DEFINITIONS[pattern_id]["priority"],
                **variables
            })

        return combos

    def filter_matrix(
        self,
        df: pd.DataFrame,
        patterns: List[str] = None,
        priority: str = None,
        limit: int = None,
        specific_combos: List[Dict] = None
    ) -> pd.DataFrame:
        """Filter matrix based on criteria"""

        filtered = df.copy()

        # Filter by pattern
        if patterns:
            filtered = filtered[filtered['pattern_id'].isin(patterns)]

        # Filter by priority
        if priority:
            filtered = filtered[filtered['priority'] == priority]

        # Filter by specific combinations (Week 1 hand-picked)
        if specific_combos:
            # Match on all variables
            mask = pd.Series([False] * len(filtered))
            for combo in specific_combos:
                combo_mask = pd.Series([True] * len(filtered))
                for key, value in combo.items():
                    if key in filtered.columns:
                        combo_mask &= (filtered[key] == value)
                mask |= combo_mask
            filtered = filtered[mask]

        # Apply limit
        if limit and len(filtered) > limit:
            filtered = filtered.head(limit)

        print(f"✓ Filtered to {len(filtered)} pages")
        return filtered


class BatchProcessor:
    """Processes batches of PSEO pages with progress tracking and error handling"""

    def __init__(self, orchestrator: PSEOOrchestrator, output_dir: str = "output"):
        self.orchestrator = orchestrator
        self.output_dir = output_dir
        self.checkpoint_file = f"{output_dir}/checkpoint.json"

        os.makedirs(output_dir, exist_ok=True)

    def process_batch(
        self,
        tasks_df: pd.DataFrame,
        start_index: int = 0,
        save_every: int = 10
    ) -> List[Dict]:
        """Process a batch of tasks with checkpointing"""

        print(f"\n{'='*80}")
        print(f"🚀 Starting batch processing")
        print(f"   Total tasks: {len(tasks_df)}")
        print(f"   Starting at index: {start_index}")
        print(f"   Save checkpoint every: {save_every} pages")
        print(f"{'='*80}\n")

        generated_pages = []
        failed_tasks = []

        for idx in range(start_index, len(tasks_df)):
            row = tasks_df.iloc[idx]

            print(f"\n[{idx + 1}/{len(tasks_df)}] Processing task...")

            # Create variables dict
            variables = {k: v for k, v in row.items() if k not in ['pattern_id', 'priority']}

            try:
                # Generate page
                page = self.orchestrator.generate_page(
                    pattern_id=row['pattern_id'],
                    variables=variables
                )

                # Convert to dict (use public export - excludes internal metadata)
                page_dict = page.to_dict_public()
                generated_pages.append(page_dict)

                # Save individual page
                page_file = f"{self.output_dir}/page_{page.page_id}.json"
                with open(page_file, 'w') as f:
                    json.dump(page_dict, f, indent=2)

                # Checkpoint progress
                if (idx + 1) % save_every == 0:
                    self._save_checkpoint(idx + 1, generated_pages)
                    print(f"\n💾 Checkpoint saved at index {idx + 1}")

            except Exception as e:
                print(f"\n❌ Failed to generate page: {str(e)}")
                import traceback
                traceback.print_exc()

                failed_tasks.append({
                    "index": idx,
                    "pattern_id": row['pattern_id'],
                    "variables": variables,
                    "error": str(e)
                })
                continue

        # Final save
        self._save_checkpoint(len(tasks_df), generated_pages)

        # Save failed tasks log
        if failed_tasks:
            with open(f"{self.output_dir}/failed_tasks.json", 'w') as f:
                json.dump(failed_tasks, f, indent=2)
            print(f"\n⚠️ {len(failed_tasks)} tasks failed. See failed_tasks.json")

        return generated_pages

    def _save_checkpoint(self, last_index: int, pages: List[Dict]):
        """Save progress checkpoint"""
        checkpoint = {
            "last_index": last_index,
            "timestamp": datetime.now().isoformat(),
            "pages_generated": len(pages)
        }

        with open(self.checkpoint_file, 'w') as f:
            json.dump(checkpoint, f, indent=2)

    def load_checkpoint(self) -> int:
        """Load checkpoint to resume from last index"""
        if os.path.exists(self.checkpoint_file):
            with open(self.checkpoint_file, 'r') as f:
                checkpoint = json.load(f)
                print(f"📂 Checkpoint found: Resume from index {checkpoint['last_index']}")
                return checkpoint['last_index']
        return 0

    def save_to_csv(self, pages: List[Dict], filename: str):
        """
        Save generated pages to CSV for WordPress import.

        Only includes keyword-relevant content and SEO-optimized fields.
        Excludes internal metadata (quality scores, agent tracking, etc.)
        """

        # Flatten for CSV
        flattened = []
        for page in pages:
            flat = {
                "page_id": page["page_id"],
                "pattern_id": page["pattern_id"],
                "status": page["status"],
                "post_title": page["post_title"],
                "url_slug": page["url_slug"],
                "meta_title": page["meta_title"],
                "meta_description": page["meta_description"],
                "hero_h1": page["hero_section"].get("h1", ""),
                "hero_subtitle": page["hero_section"].get("subtitle", ""),
                "hero_primary_cta": page["hero_section"].get("primary_cta", ""),
                "problem_agitation": page["problem_agitation"],
                "solution_overview": page["solution_overview"],
                "faq_json": json.dumps(page["faq_json"]),
                "comparison_table_json": json.dumps(page.get("comparison_table_json", [])),
                "feature_sections_json": json.dumps(page.get("feature_sections", [])),
                "schema_markup_json": json.dumps(page.get("schema_markup", [])),
                "final_cta": page["final_cta"],
                "generated_at": page["generated_at"]
            }

            flattened.append(flat)

        df = pd.DataFrame(flattened)
        csv_path = f"{self.output_dir}/{filename}"
        df.to_csv(csv_path, index=False)

        print(f"\n💾 Saved {len(pages)} pages to {csv_path}")
        return csv_path


def main():
    """Main execution function"""

    parser = argparse.ArgumentParser(description="PSEO Batch Generator")
    parser.add_argument("--phase", choices=["week_1", "week_2", "week_3", "week_4_6", "all"],
                       default="week_1", help="Rollout phase")
    parser.add_argument("--pattern", nargs="+", help="Specific patterns to generate")
    parser.add_argument("--limit", type=int, help="Limit number of pages")
    parser.add_argument("--start-index", type=int, default=0, help="Start from index (resume)")
    parser.add_argument("--save-every", type=int, default=10, help="Save checkpoint every N pages")
    parser.add_argument("--output-dir", default="output", help="Output directory")

    args = parser.parse_args()

    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                                 ║
    ║         PSEO Batch Generator - Phased Rollout                  ║
    ║              Powered by Google Gemini API                      ║
    ║                                                                 ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)

    # Load environment
    load_dotenv()

    # Load configuration files
    print("\n📦 Loading configuration...")

    with open('config/patterns.json', 'r') as f:
        patterns_data = json.load(f)

    with open('config/variables.json', 'r') as f:
        variables_data = json.load(f)

    viral_hooks = []
    if os.path.exists('config/viral_hooks.json'):
        with open('config/viral_hooks.json', 'r') as f:
            hooks_data = json.load(f)
            # Use manifesto_hooks (brand-specific), NOT generic hooks
            viral_hooks = hooks_data.get('manifesto_hooks', [])

    # Create orchestrator config
    config = {
        'pattern_library': patterns_data,
        'variables': variables_data,
        'viral_hooks': viral_hooks,
        'gemini_api_key': os.environ.get('GEMINI_API_KEY')
    }

    if not config['gemini_api_key']:
        print("❌ Error: GEMINI_API_KEY not found in environment")
        print("   Please set it in .env file or export it")
        return

    # Initialize orchestrator
    print("🔧 Initializing orchestrator...")
    orchestrator = PSEOOrchestrator(config)

    # Initialize generators (pass variables_data to avoid duplication)
    matrix_gen = PSEOMatrixGenerator(variables_config=variables_data)
    processor = BatchProcessor(orchestrator, output_dir=args.output_dir)

    # Check for checkpoint
    start_index = args.start_index
    if start_index == 0:
        checkpoint_index = processor.load_checkpoint()
        if checkpoint_index > 0:
            resume = input(f"Resume from checkpoint index {checkpoint_index}? (y/n): ")
            if resume.lower() == 'y':
                start_index = checkpoint_index

    # Generate matrix
    print("\n📊 Generating PSEO matrix...")

    if args.phase == "all":
        # Generate all patterns
        full_matrix = matrix_gen.generate_matrix()
        tasks_df = full_matrix
    else:
        # Use phase configuration
        phase_config = ROLLOUT_PHASES[args.phase]
        patterns = args.pattern if args.pattern else phase_config["patterns"]

        # Generate and filter
        full_matrix = matrix_gen.generate_matrix(patterns=patterns)
        tasks_df = matrix_gen.filter_matrix(
            full_matrix,
            patterns=patterns,
            priority=phase_config.get("priority_filter"),
            limit=args.limit or phase_config.get("limit"),
            specific_combos=phase_config.get("specific_combos")
        )

    print(f"\n✓ Tasks to process: {len(tasks_df)}")
    print(f"  Phase: {args.phase}")
    print(f"  Patterns: {tasks_df['pattern_id'].unique().tolist()}")

    # Show sample
    if len(tasks_df) > 0:
        print(f"\n📋 Sample tasks:")
        for i, row in tasks_df.head(3).iterrows():
            vars_str = ", ".join([f"{k}={v}" for k, v in row.items() if k not in ['pattern_id', 'priority']])
            print(f"  {i + 1}. Pattern {row['pattern_id']}: {vars_str}")

    # Confirm before proceeding
    proceed = input("\nProceed with generation? (y/n): ")
    if proceed.lower() != 'y':
        print("Cancelled.")
        return

    # Process batch
    start_time = datetime.now()

    generated_pages = processor.process_batch(
        tasks_df,
        start_index=start_index,
        save_every=args.save_every
    )

    execution_time = (datetime.now() - start_time).total_seconds()

    # Save to CSV
    csv_filename = f"sozee_landing_pages_{args.phase}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    csv_path = processor.save_to_csv(generated_pages, csv_filename)

    # Print summary
    print(f"\n{'='*80}")
    print(f"✅ Batch Complete")
    print(f"{'='*80}")
    print(f"  Total pages generated: {len(generated_pages)}")
    print(f"  Total execution time: {execution_time / 60:.1f} minutes")
    if len(generated_pages) > 0:
        print(f"  Average time per page: {execution_time / len(generated_pages):.1f}s")
    print(f"  Output CSV: {csv_path}")
    print(f"  Individual JSON files: {args.output_dir}/")
    print(f"\n🚀 Ready for WordPress import!")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    main()
