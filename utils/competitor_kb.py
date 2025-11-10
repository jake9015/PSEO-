#!/usr/bin/env python3
"""
Competitor Knowledge Base Manager
Handles CRUD operations for competitor_profiles.json
"""

import json
import os
from typing import Dict, Optional
from datetime import datetime


class CompetitorKnowledgeBase:
    """Manages the competitor knowledge base file"""

    def __init__(self, kb_path: str = None):
        """Initialize KB with path to competitor_profiles.json"""
        if kb_path is None:
            # Default path: config/competitor_profiles.json
            kb_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'config',
                'competitor_profiles.json'
            )
        self.kb_path = kb_path
        self._ensure_kb_exists()

    def _ensure_kb_exists(self):
        """Ensure KB file exists with proper structure"""
        if not os.path.exists(self.kb_path):
            # Create directory if needed
            os.makedirs(os.path.dirname(self.kb_path), exist_ok=True)
            # Create empty KB
            self._save_kb({
                "competitors": {},
                "metadata": {
                    "version": "1.0",
                    "last_updated": datetime.now().isoformat(),
                    "total_competitors": 0,
                    "notes": "Agent-managed competitor knowledge base. Auto-populated during page generation."
                }
            })

    def _load_kb(self) -> dict:
        """Load KB from file"""
        try:
            with open(self.kb_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ Error loading KB: {e}")
            return {
                "competitors": {},
                "metadata": {
                    "version": "1.0",
                    "last_updated": datetime.now().isoformat(),
                    "total_competitors": 0
                }
            }

    def _save_kb(self, kb_data: dict):
        """Save KB to file"""
        try:
            # Update metadata
            kb_data['metadata']['last_updated'] = datetime.now().isoformat()
            kb_data['metadata']['total_competitors'] = len(kb_data.get('competitors', {}))

            with open(self.kb_path, 'w') as f:
                json.dump(kb_data, f, indent=2)
        except Exception as e:
            print(f"❌ Error saving KB: {e}")

    def get_profile(self, competitor: str) -> Optional[Dict]:
        """
        Get competitor profile from KB
        Returns None if competitor not found
        """
        kb = self._load_kb()
        return kb.get('competitors', {}).get(competitor)

    def profile_exists(self, competitor: str) -> bool:
        """Check if competitor exists in KB"""
        kb = self._load_kb()
        return competitor in kb.get('competitors', {})

    def save_profile(self, competitor: str, profile: dict):
        """
        Save new competitor profile to KB
        """
        kb = self._load_kb()

        # Ensure competitors dict exists
        if 'competitors' not in kb:
            kb['competitors'] = {}

        # Add research timestamp
        profile['kb_metadata'] = {
            'added_at': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat(),
            'source': 'agent_research'
        }

        # Save profile
        kb['competitors'][competitor] = profile

        self._save_kb(kb)
        print(f"  ✓ Saved {competitor} profile to KB")

    def update_profile(self, competitor: str, new_data: dict):
        """
        Update existing profile with new research data
        Merges new data with existing, new data takes priority
        """
        kb = self._load_kb()

        if 'competitors' not in kb:
            kb['competitors'] = {}

        # Get existing profile or create new
        existing = kb['competitors'].get(competitor, {})

        # Deep merge
        updated = self._deep_merge(existing, new_data)

        # Update timestamp
        if 'kb_metadata' not in updated:
            updated['kb_metadata'] = {}
        updated['kb_metadata']['last_updated'] = datetime.now().isoformat()
        if 'added_at' not in updated.get('kb_metadata', {}):
            updated['kb_metadata']['added_at'] = datetime.now().isoformat()
        updated['kb_metadata']['source'] = 'agent_research'

        kb['competitors'][competitor] = updated

        self._save_kb(kb)
        print(f"  ✓ Updated {competitor} profile in KB")

    def _deep_merge(self, base: dict, update: dict) -> dict:
        """
        Deep merge two dictionaries
        Update values take priority over base values
        """
        result = base.copy()

        for key, value in update.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                # Recursively merge nested dicts
                result[key] = self._deep_merge(result[key], value)
            else:
                # Update value (new data takes priority)
                result[key] = value

        return result

    def list_competitors(self) -> list:
        """Get list of all competitors in KB"""
        kb = self._load_kb()
        return list(kb.get('competitors', {}).keys())

    def get_stats(self) -> dict:
        """Get KB statistics"""
        kb = self._load_kb()
        competitors = kb.get('competitors', {})

        return {
            'total_competitors': len(competitors),
            'last_updated': kb.get('metadata', {}).get('last_updated'),
            'competitors': list(competitors.keys())
        }
