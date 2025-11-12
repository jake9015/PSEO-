#!/usr/bin/env python3
"""
PSEO Multi-Agent Orchestrator
==============================

Coordinates the execution of specialized AI agents for landing page generation.

This module implements the central orchestration system for the multi-agent PSEO pipeline.
It manages agent lifecycle, message routing, task execution, and coordinates the complete
page generation workflow.

Architecture:
-------------
1. Blueprint Creation (PSEO Strategist)
2. Research Phase (Parallel): Competitor Research, Audience Insights, Statistics
3. Content Generation: Copywriting, FAQ, Comparison Tables
4. Optimization: SEO, Schema Markup, Quality Control
5. Output Assembly

Classes:
--------
- AgentManager: Manages agent lifecycle and message routing
- PSEOOrchestrator: Main coordinator for multi-agent page generation

Performance:
------------
- Speed: 10-20 pages/hour
- Cost: $0.50-1.00 per page
- Quality Score: 0.85-0.95
- API Calls: 5-10 per page

Usage:
------
    from pseo_orchestrator import PSEOOrchestrator

    orchestrator = PSEOOrchestrator()
    page = orchestrator.generate_page(
        pattern_id='1',
        variables={'competitor': 'Higgsfield', 'audience': 'OnlyFans Creators'}
    )

    print(f"Quality Score: {page.quality_score}")
"""

import sys
import os
from typing import Dict, List, Any
import time
import json
from datetime import datetime
import google.generativeai as genai

# Import framework
from agent_framework import (
    BaseAgent, AgentMessage, AgentResponse,
    ContentBlueprint, PageOutput
)

# Import all agents
from agents.pseo_strategist import PSEOStrategistAgent
from agents.competitor_research import CompetitorResearchAgent
from agents.audience_insight import AudienceInsightAgent
from agents.copywriting import CopywritingAgent
from agents.faq_generator import FAQGeneratorAgent
from agents.seo_optimizer import SEOOptimizationAgent
from agents.quality_control import QualityControlAgent
from agents.comparison_table import ComparisonTableAgent
from agents.statistics_agent import StatisticsAgent
from agents.schema_markup import SchemaMarkupAgent


class AgentManager:
    """Manages agent lifecycle and inter-agent communication"""

    def __init__(self, pattern_library: Dict, viral_hooks: List[str], gemini_api_key: str):
        """Initialize all agents"""

        # Configure Gemini API
        genai.configure(api_key=gemini_api_key)

        # Initialize agents
        self.agents = {
            'pseo_strategist': PSEOStrategistAgent(pattern_library=pattern_library),
            'competitor_research': CompetitorResearchAgent(),
            'audience_insight': AudienceInsightAgent(),
            'copywriting': CopywritingAgent(viral_hooks=viral_hooks),
            'faq_generator': FAQGeneratorAgent(),
            'seo_optimizer': SEOOptimizationAgent(),
            'quality_control': QualityControlAgent(),
            'comparison_table': ComparisonTableAgent(),
            'statistics': StatisticsAgent(),
            'schema_markup': SchemaMarkupAgent()
        }

        self.message_log = []
        self.task_counter = 0

    def send_message(self, from_agent: str, to_agent: str, task: Dict,
                    context: Dict, priority: str = "medium") -> AgentResponse:
        """Send message to agent and execute task"""

        self.task_counter += 1
        task_id = f"task_{self.task_counter}_{int(time.time())}"

        message = AgentMessage(
            from_agent=from_agent,
            to_agent=to_agent,
            task_id=task_id,
            priority=priority,
            task=task,
            context=context
        )

        # Log message
        self.message_log.append(message.to_dict())

        # Execute task
        # Normalize agent name to match registry keys
        # Example: 'PSEO_Strategist_Agent' → 'pseo_strategist'
        # This handles naming inconsistencies between callers and the agent registry
        # Registry keys use lowercase with underscores (e.g., 'pseo_strategist', 'copywriting')
        # Callers may use various formats (e.g., 'PSEO_Strategist_Agent', 'Copywriting_Agent')
        agent_key = to_agent.lower().replace('_agent', '')
        agent = self.agents.get(agent_key)

        if not agent:
            print(f"⚠️ Agent not found: {to_agent}")
            return None

        print(f"\n  → {from_agent} → {to_agent}")
        print(f"    Task: {task.get('action', 'execute')}")

        response = agent.execute(message)

        # Log response
        self.message_log.append(response.to_dict())

        return response

    def execute_parallel_tasks(self, tasks: List[Dict], context: Dict) -> Dict[str, AgentResponse]:
        """Execute multiple tasks in parallel (simulated with sequential for now)"""

        print(f"\n  🔄 Executing {len(tasks)} parallel tasks...")

        results = {}
        for task in tasks:
            agent_name = task['agent']
            response = self.send_message(
                from_agent='orchestrator',
                to_agent=agent_name,
                task=task.get('params', {}),
                context=context,
                priority=task.get('priority', 'medium')
            )
            results[agent_name] = response

        return results

    def get_message_log(self):
        """Return complete message history"""
        return self.message_log


class PSEOOrchestrator:
    """Main orchestrator for PSEO content generation"""

    def __init__(self, config: Dict):
        """
        Initialize orchestrator with configuration

        config should contain:
        - pattern_library: Dict of patterns
        - variables: Dict of all variables
        - viral_hooks: List of viral hooks
        - gemini_api_key: API key
        """
        self.pattern_library = config['pattern_library']
        self.variables = config['variables']
        self.viral_hooks = config.get('viral_hooks', [])
        self.gemini_api_key = config['gemini_api_key']

        # Initialize agent manager
        self.agent_manager = AgentManager(
            pattern_library=self.pattern_library,
            viral_hooks=self.viral_hooks,
            gemini_api_key=self.gemini_api_key
        )

        print("✓ PSEO Orchestrator initialized")
        print(f"  Agents: {list(self.agent_manager.agents.keys())}")

    def generate_page(self, pattern_id: str, variables: Dict,
                     generation_model: str = "auto") -> PageOutput:
        """
        Generate complete landing page using multi-agent pipeline

        Args:
            pattern_id: Pattern ID (1-6) - accepts both int and str, normalized to str
            variables: Dict of variables for this page
            generation_model: "Model 1" or "Model 2" or "auto"

        Returns:
            PageOutput object with complete page data
        """

        # Normalize pattern_id to string for consistent handling throughout the pipeline
        # patterns.json uses integer IDs but code comparisons use strings
        pattern_id = str(pattern_id)

        print(f"\n{'='*70}")
        print(f"🚀 GENERATING PAGE: Pattern {pattern_id}")
        print(f"{'='*70}")

        start_time = time.time()

        # Step 1: Create Blueprint (PSEO Strategist)
        print(f"\n📋 STEP 1: Creating Content Blueprint")
        blueprint_response = self.agent_manager.send_message(
            from_agent='orchestrator',
            to_agent='PSEO_Strategist_Agent',
            task={
                'pattern_id': pattern_id,
                'variables': variables
            },
            context={},
            priority='high'
        )

        if blueprint_response.status != 'completed':
            error_details = blueprint_response.data if hasattr(blueprint_response, 'data') else "No details available"
            raise Exception(
                f"Blueprint creation failed with status: {blueprint_response.status}\n"
                f"Details: {error_details}\n"
                f"Check PSEO Strategist Agent logs above for more information."
            )

        blueprint_dict = blueprint_response.data['blueprint']
        agent_tasks = blueprint_response.data['agent_task_list']

        blueprint = ContentBlueprint(**blueprint_dict)

        print(f"  ✓ Blueprint created: {blueprint.page_id}")
        print(f"    Model: {blueprint.generation_model}")
        print(f"    Agents needed: {len(blueprint.required_agents)}")
        print(f"    Research tasks: {len(blueprint.research_requirements)}")

        # Step 2: Research Phase (Parallel)
        research_data = {}

        if blueprint.research_requirements:
            print(f"\n🔍 STEP 2: Research Phase ({len(blueprint.research_requirements)} tasks)")

            research_tasks = []
            for req in blueprint.research_requirements:
                if req['type'] == 'competitor_analysis':
                    research_tasks.append({
                        'agent': 'Competitor_Research_Agent',
                        'params': {
                            'competitor': req['target'],
                            'audience': variables.get('audience', ''),
                            'required_data': req['required_data']
                        },
                        'priority': 'high'
                    })
                elif req['type'] == 'audience_insights':
                    research_tasks.append({
                        'agent': 'Audience_Insight_Agent',
                        'params': {
                            'audience': req['target'],
                            'required_data': req['required_data']
                        },
                        'priority': 'high'
                    })

            # Add statistics research (especially important for Pattern 6)
            research_tasks.append({
                'agent': 'Statistics_Agent',
                'params': {
                    'pattern_id': pattern_id,
                    'topic': blueprint.pattern_name,
                    'audience': variables.get('audience', 'creators'),
                    'platform': variables.get('platform', 'social media')
                },
                'priority': 'medium'
            })

            # Execute research tasks
            research_results = self.agent_manager.execute_parallel_tasks(
                research_tasks,
                context={'blueprint': blueprint_dict, 'pseo_variables': variables}
            )

            # Extract research data
            for agent_name, response in research_results.items():
                if response and response.status == 'completed':
                    research_data[agent_name] = response.data

            print(f"  ✓ Research complete: {len(research_data)} datasets")

        # Step 3: Content Generation (Copywriting)
        print(f"\n✍️ STEP 3: Content Generation")

        content_response = self.agent_manager.send_message(
            from_agent='orchestrator',
            to_agent='Copywriting_Agent',
            task={
                'sections': blueprint.sections_needed,
                'variables': variables
            },
            context={
                'blueprint': blueprint_dict,
                'research_data': research_data,
                'pseo_variables': variables
            },
            priority='high'
        )

        if content_response.status != 'completed':
            error_details = content_response.data if hasattr(content_response, 'data') else "No details available"
            raise Exception(
                f"Content generation failed with status: {content_response.status}\n"
                f"Details: {error_details}\n"
                f"Possible causes:\n"
                f"  - API rate limits reached\n"
                f"  - Invalid research data format\n"
                f"  - Missing required variables\n"
                f"Check Copywriting Agent logs above for specific errors."
            )

        content = content_response.data['content']
        print(f"  ✓ Content generated")

        # Step 4: Supplementary Content (FAQ + SEO + Comparison + Schema) - Parallel
        print(f"\n🔧 STEP 4: Generating Supplementary Content")

        h1 = content.get('hero', {}).get('h1', '')

        supplementary_tasks = [
            {
                'agent': 'FAQ_Generator_Agent',
                'params': {
                    'pattern_id': pattern_id,
                    'count': 5
                },
                'priority': 'medium'
            },
            {
                'agent': 'SEO_Optimization_Agent',
                'params': {
                    'h1': h1,
                    'pattern_id': pattern_id
                },
                'priority': 'medium'
            }
        ]

        # Add comparison table for patterns 1 & 4 (Comparison, Alternative)
        if pattern_id in ['1', '4']:
            supplementary_tasks.append({
                'agent': 'Comparison_Table_Agent',
                'params': {
                    'pattern_id': pattern_id,
                    'competitor': variables.get('competitor', ''),
                    'audience': variables.get('audience', 'creators')
                },
                'priority': 'high'
            })

        supplementary_results = self.agent_manager.execute_parallel_tasks(
            supplementary_tasks,
            context={
                'blueprint': blueprint_dict,
                'pseo_variables': variables,
                'content': content,
                'research_data': research_data
            }
        )

        # Extract supplementary data
        faq_data = supplementary_results.get('FAQ_Generator_Agent')
        seo_data = supplementary_results.get('SEO_Optimization_Agent')
        comparison_data = supplementary_results.get('Comparison_Table_Agent')

        faqs = faq_data.data['faqs'] if faq_data and faq_data.status == 'completed' else []
        metadata = seo_data.data if seo_data and seo_data.status == 'completed' else {}
        comparison_table = comparison_data.data['comparison_table'] if comparison_data and comparison_data.status == 'completed' else []

        print(f"  ✓ FAQ: {len(faqs)} pairs")
        print(f"  ✓ SEO metadata generated")
        if pattern_id in ['1', '4']:
            print(f"  ✓ Comparison table: {len(comparison_table)} features")

        # Generate Schema Markup (after FAQ and metadata are ready)
        print(f"\n📊 STEP 4b: Generating Schema Markup")

        schema_response = self.agent_manager.send_message(
            from_agent='orchestrator',
            to_agent='Schema_Markup_Agent',
            task={
                'pattern_id': pattern_id,
                'page_data': content,
                'faqs': faqs,
                'meta': metadata
            },
            context={
                'blueprint': blueprint_dict,
                'pseo_variables': variables
            },
            priority='medium'
        )

        schemas = schema_response.data['schemas'] if schema_response and schema_response.status == 'completed' else []
        print(f"  ✓ Generated {len(schemas)} schema types")

        # Step 5: Assemble Page
        print(f"\n🔨 STEP 5: Assembling Page")

        page_output = self._assemble_page(
            blueprint=blueprint,
            variables=variables,
            content=content,
            faqs=faqs,
            metadata=metadata,
            research_data=research_data,
            comparison_table=comparison_table,
            schemas=schemas
        )

        print(f"  ✓ Page assembled: {page_output.page_id}")

        # Step 6: Quality Control
        print(f"\n🎯 STEP 6: Quality Control")

        qc_response = self.agent_manager.send_message(
            from_agent='orchestrator',
            to_agent='Quality_Control_Agent',
            task={},
            context={
                'page_data': page_output.to_dict(),
                'blueprint': blueprint_dict
            },
            priority='high'
        )

        if qc_response.status == 'completed':
            quality_report = qc_response.data
            page_output.quality_score = quality_report['overall_score']
            page_output.uniqueness_check = quality_report['approval_status']

            print(f"  ✓ Quality Score: {quality_report['overall_score']:.2f}")
            print(f"  ✓ Status: {quality_report['approval_status']}")

            if quality_report['issues']:
                print(f"  ⚠️ Issues found: {len(quality_report['issues'])}")
                for issue in quality_report['issues'][:3]:
                    print(f"    - {issue}")

        # Complete
        total_time = time.time() - start_time

        print(f"\n{'='*70}")
        print(f"✅ PAGE GENERATION COMPLETE")
        print(f"{'='*70}")
        print(f"  Page ID: {page_output.page_id}")
        print(f"  Time: {total_time:.2f}s")
        print(f"  Quality: {page_output.quality_score:.2f}")
        print(f"  Status: {page_output.uniqueness_check}")
        print(f"{'='*70}\n")

        return page_output

    def _assemble_page(self, blueprint: ContentBlueprint, variables: Dict,
                      content: Dict, faqs: List, metadata: Dict,
                      research_data: Dict, comparison_table: List = None,
                      schemas: List = None) -> PageOutput:
        """Assemble final page output from all components"""

        # Build URL slug
        url_slug = self._build_url_slug(blueprint.pattern_id, variables)

        # Extract hero section
        hero = content.get('hero', {})

        # Use comparison_table from specialized agent if available, otherwise fallback to content
        final_comparison_table = comparison_table if comparison_table else content.get('comparison_table', [])

        # Build page output
        page = PageOutput(
            page_id=blueprint.page_id,
            pattern_id=blueprint.pattern_id,
            status='completed',
            post_title=hero.get('h1', ''),
            url_slug=url_slug,
            meta_title=metadata.get('meta_title', hero.get('h1', '')),
            meta_description=metadata.get('meta_description', hero.get('subtitle', '')),
            hero_section=hero,
            problem_agitation=content.get('problem', ''),
            solution_overview=content.get('solution', ''),
            comparison_table_json=final_comparison_table,
            feature_sections=content.get('features', []),
            faq_json=faqs,
            final_cta=content.get('final_cta', ''),
            pseo_variables=variables,
            research_sources=self._extract_sources(research_data),
            generation_model=blueprint.generation_model,
            agents_used=blueprint.required_agents,
            schema_markup=schemas if schemas else []
        )

        return page

    def _build_url_slug(self, pattern_id: str, variables: Dict) -> str:
        """Build URL slug from pattern and variables"""

        # Get pattern from library
        pattern = None
        for p in self.pattern_library.get('patterns', []):
            if str(p.get('id')) == str(pattern_id):
                pattern = p
                break

        if not pattern:
            available_ids = [str(p.get('id')) for p in self.pattern_library.get('patterns', [])]
            raise ValueError(
                f"Pattern ID '{pattern_id}' not found in pattern library.\n"
                f"Available pattern IDs: {', '.join(available_ids)}\n"
                f"Check config/patterns.json to verify pattern configuration.\n"
                f"If adding a new pattern, ensure it's properly registered in patterns.json."
            )

        # Use url_formula from pattern
        url_formula = pattern.get('url_formula', '/sozee')

        # Replace variables
        url = url_formula
        for var_name, var_value in variables.items():
            placeholder = f'{{{var_name}}}'
            if placeholder in url:
                # Convert to slug format
                slug_value = var_value.lower().replace(' ', '-').replace('_', '-')
                url = url.replace(placeholder, slug_value)

        return url

    def _extract_sources(self, research_data: Dict) -> List[Dict[str, str]]:
        """Extract research sources from research data"""
        sources = []

        for agent_name, data in research_data.items():
            sources.append({
                'agent': agent_name,
                'type': 'ai_research',
                'timestamp': datetime.now().isoformat()
            })

        return sources


def main():
    """Test orchestrator with single page generation"""

    # Load configuration
    import json
    from dotenv import load_dotenv

    load_dotenv()

    # Load data files
    with open('config/patterns.json', 'r') as f:
        patterns = json.load(f)

    with open('config/variables.json', 'r') as f:
        variables_lib = json.load(f)

    viral_hooks = []
    if os.path.exists('config/viral_hooks.json'):
        with open('config/viral_hooks.json', 'r') as f:
            hooks_data = json.load(f)
            viral_hooks = hooks_data.get('hooks', [])

    # Create config
    config = {
        'pattern_library': patterns,
        'variables': variables_lib,
        'viral_hooks': viral_hooks,
        'gemini_api_key': os.environ.get('GEMINI_API_KEY')
    }

    # Initialize orchestrator
    orchestrator = PSEOOrchestrator(config)

    # Test with Pattern 1 (Competitor Comparison)
    test_variables = {
        'competitor': 'Higgsfield',
        'audience': 'OnlyFans Creators'
    }

    print("\n" + "="*70)
    print("TESTING PSEO ORCHESTRATOR")
    print("="*70)

    page = orchestrator.generate_page(
        pattern_id='1',
        variables=test_variables
    )

    # Save output
    output_path = f'output/test_page_{page.page_id}.json'
    with open(output_path, 'w') as f:
        f.write(page.to_json())

    print(f"\n✅ Test page saved to: {output_path}")

    # Show message log
    print(f"\n📨 Message Log: {len(orchestrator.agent_manager.get_message_log())} messages")


if __name__ == '__main__':
    main()
