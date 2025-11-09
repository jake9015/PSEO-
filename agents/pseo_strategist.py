#!/usr/bin/env python3
"""
PSEO Strategist Agent
Analyzes patterns, creates content blueprints, delegates to worker agents
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_framework import BaseAgent, AgentMessage, AgentResponse, ContentBlueprint
from typing import Dict, Any
import time


class PSEOStrategistAgent(BaseAgent):
    """Master PSEO strategist that plans content generation"""

    def __init__(self, pattern_library: Dict, model=None):
        super().__init__(
            name="PSEO_Strategist_Agent",
            role="PSEO Content Strategist & Planning Architect",
            model=model
        )
        self.pattern_library = pattern_library

    def execute(self, message: AgentMessage) -> AgentResponse:
        """
        Analyze pattern + variables and create content blueprint
        """
        start_time = time.time()
        self.log_message(message)

        task = message.task
        pattern_id = task.get('pattern_id')
        variables = task.get('variables', {})

        # Load pattern configuration
        pattern = self._get_pattern(pattern_id)
        if not pattern:
            return self.create_response(
                message,
                status="failed",
                data={'error': f"Pattern {pattern_id} not found"},
                execution_time=time.time() - start_time
            )

        # Create blueprint
        blueprint = self._create_blueprint(pattern, variables)

        execution_time = time.time() - start_time

        return self.create_response(
            message,
            status="completed",
            data={
                'blueprint': blueprint.to_dict(),
                'agent_task_list': self._create_agent_tasks(blueprint, variables)
            },
            execution_time=execution_time,
            confidence=1.0
        )

    def _get_pattern(self, pattern_id: str) -> Dict:
        """Retrieve pattern configuration"""
        for pattern in self.pattern_library.get('patterns', []):
            if str(pattern.get('id')) == str(pattern_id):
                return pattern
        return None

    def _create_blueprint(self, pattern: Dict, variables: Dict) -> ContentBlueprint:
        """Create detailed content blueprint"""

        pattern_id = str(pattern['id'])
        pattern_name = pattern['name']

        # Determine funnel stage and generation model
        funnel_stage, generation_model = self._determine_strategy(pattern_id)

        # Build page ID
        page_id = self._build_page_id(pattern_id, variables)

        # Determine required agents
        required_agents = self._get_required_agents(pattern_id, generation_model)

        # Define sections needed
        sections_needed = self._get_sections_for_pattern(pattern_id)

        # Identify research requirements
        research_requirements = self._get_research_needs(pattern_id, variables)

        # Determine priority
        priority = pattern.get('priority', 'MEDIUM')

        return ContentBlueprint(
            page_id=page_id,
            pattern_id=pattern_id,
            pattern_name=pattern_name,
            funnel_stage=funnel_stage,
            generation_model=generation_model,
            required_agents=required_agents,
            sections_needed=sections_needed,
            research_requirements=research_requirements,
            priority=priority
        )

    def _determine_strategy(self, pattern_id: str) -> tuple:
        """Determine funnel stage and generation model"""

        # Bottom-funnel patterns requiring research (Model 2)
        if pattern_id in ['1', '4', '5']:
            return ('bottom', 'Model 2')

        # Mid-funnel patterns (Model 1 with optional research)
        elif pattern_id in ['2', '3', '6']:
            return ('mid', 'Model 1')

        # Default
        return ('top', 'Model 1')

    def _get_required_agents(self, pattern_id: str, generation_model: str) -> list:
        """Determine which agents are needed"""

        agents = ['PSEO_Strategist_Agent']  # Always include self

        if generation_model == 'Model 2':
            # Research-intensive patterns
            if pattern_id in ['1', '4']:  # Comparison, Alternative
                agents.extend([
                    'Competitor_Research_Agent',
                    'Audience_Insight_Agent',
                    'Copywriting_Agent',
                    'FAQ_Generator_Agent',
                    'SEO_Optimization_Agent',
                    'Quality_Control_Agent'
                ])
            elif pattern_id == '6':  # Content Crisis
                agents.extend([
                    'Market_Statistics_Agent',
                    'Audience_Insight_Agent',
                    'Copywriting_Agent',
                    'FAQ_Generator_Agent',
                    'SEO_Optimization_Agent',
                    'Quality_Control_Agent'
                ])
        else:
            # Model 1 - simpler generation
            agents.extend([
                'Copywriting_Agent',
                'FAQ_Generator_Agent',
                'SEO_Optimization_Agent'
            ])

        return agents

    def _get_sections_for_pattern(self, pattern_id: str) -> list:
        """Define sections needed for each pattern"""

        base_sections = [
            'hero_section',
            'problem_agitation',
            'solution_overview',
            'faq',
            'final_cta'
        ]

        # Comparison patterns need comparison table
        if pattern_id in ['1', '4']:
            base_sections.insert(3, 'comparison_table')

        # All patterns can have feature sections
        base_sections.insert(4, 'feature_sections')

        return base_sections

    def _get_research_needs(self, pattern_id: str, variables: Dict) -> list:
        """Identify what research is needed"""

        research_needs = []

        # Competitor comparison patterns
        if pattern_id in ['1', '4'] and 'competitor' in variables:
            research_needs.append({
                'type': 'competitor_analysis',
                'target': variables['competitor'],
                'required_data': [
                    'features_list',
                    'pricing_tiers',
                    'pros_cons',
                    'audience_fit',
                    'nsfw_support'
                ]
            })

        # All patterns need audience insights
        if 'audience' in variables:
            research_needs.append({
                'type': 'audience_insights',
                'target': variables['audience'],
                'required_data': [
                    'pain_points',
                    'desires',
                    'objections',
                    'current_solutions'
                ]
            })

        # Content Crisis pattern needs market statistics
        if pattern_id == '6':
            research_needs.append({
                'type': 'market_statistics',
                'target': 'creator_economy',
                'required_data': [
                    'burnout_stats',
                    'demand_supply_ratio',
                    'platform_growth',
                    'industry_benchmarks'
                ]
            })

        return research_needs

    def _build_page_id(self, pattern_id: str, variables: Dict) -> str:
        """Generate unique page ID"""
        parts = [f"pat{pattern_id}"]

        if 'competitor' in variables:
            parts.append(variables['competitor'][:5].lower().replace(' ', ''))
        if 'audience' in variables:
            parts.append(variables['audience'][:5].lower().replace(' ', ''))
        if 'platform' in variables:
            parts.append(variables['platform'][:5].lower().replace(' ', ''))

        return '_'.join(parts)

    def _create_agent_tasks(self, blueprint: ContentBlueprint, variables: Dict) -> list:
        """Create task list for each agent"""

        tasks = []

        for research_req in blueprint.research_requirements:
            if research_req['type'] == 'competitor_analysis':
                tasks.append({
                    'agent': 'Competitor_Research_Agent',
                    'action': 'research_competitor',
                    'params': {
                        'competitor': research_req['target'],
                        'required_data': research_req['required_data']
                    },
                    'priority': 'high',
                    'parallel': True
                })

            elif research_req['type'] == 'audience_insights':
                tasks.append({
                    'agent': 'Audience_Insight_Agent',
                    'action': 'research_audience',
                    'params': {
                        'audience': research_req['target'],
                        'required_data': research_req['required_data']
                    },
                    'priority': 'high',
                    'parallel': True
                })

        # Copywriting task (sequential, after research)
        tasks.append({
            'agent': 'Copywriting_Agent',
            'action': 'generate_content',
            'params': {
                'sections': blueprint.sections_needed,
                'variables': variables
            },
            'priority': 'high',
            'parallel': False,
            'depends_on': ['research_complete']
        })

        # FAQ and SEO can run in parallel after copywriting
        tasks.append({
            'agent': 'FAQ_Generator_Agent',
            'action': 'generate_faqs',
            'params': {
                'pattern_id': blueprint.pattern_id,
                'count': 5
            },
            'priority': 'medium',
            'parallel': True
        })

        tasks.append({
            'agent': 'SEO_Optimization_Agent',
            'action': 'generate_metadata',
            'params': {
                'h1': '',  # Will be filled by orchestrator
                'pattern_id': blueprint.pattern_id
            },
            'priority': 'medium',
            'parallel': True
        })

        # Final QC
        tasks.append({
            'agent': 'Quality_Control_Agent',
            'action': 'review_page',
            'params': {},
            'priority': 'high',
            'parallel': False,
            'depends_on': ['all_content_complete']
        })

        return tasks
