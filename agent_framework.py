#!/usr/bin/env python3
"""
PSEO Agent Framework
Base classes and utilities for multi-agent content generation
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import json


@dataclass
class AgentMessage:
    """Inter-agent communication message"""
    from_agent: str
    to_agent: str
    task_id: str
    priority: str  # high, medium, low
    task: Dict[str, Any]
    context: Dict[str, Any]
    timestamp: str = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()

    def to_dict(self):
        return {
            'from': self.from_agent,
            'to': self.to_agent,
            'task_id': self.task_id,
            'priority': self.priority,
            'task': self.task,
            'context': self.context,
            'timestamp': self.timestamp
        }


@dataclass
class AgentResponse:
    """Agent task response"""
    from_agent: str
    to_agent: str
    task_id: str
    status: str  # completed, failed, partial
    data: Dict[str, Any]
    sources: List[Dict[str, str]] = None
    execution_time: float = 0.0
    confidence: float = 1.0
    timestamp: str = None
    from_cache: bool = False  # Indicates if response came from cache

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()
        if self.sources is None:
            self.sources = []

    def to_dict(self):
        return {
            'from': self.from_agent,
            'to': self.to_agent,
            'task_id': self.task_id,
            'status': self.status,
            'data': self.data,
            'sources': self.sources,
            'execution_time': self.execution_time,
            'confidence': self.confidence,
            'timestamp': self.timestamp,
            'from_cache': self.from_cache
        }


class BaseAgent(ABC):
    """Base class for all PSEO agents"""

    def __init__(self, name: str, role: str, model=None):
        self.name = name
        self.role = role
        self.model = model
        self.message_history = []

    @abstractmethod
    def execute(self, message: AgentMessage) -> AgentResponse:
        """Execute the agent's task"""
        pass

    def log_message(self, message: AgentMessage):
        """Log incoming message"""
        self.message_history.append(message.to_dict())

    def create_response(self, message: AgentMessage, status: str, data: Dict[str, Any],
                       sources: List[Dict] = None, execution_time: float = 0.0,
                       confidence: float = 1.0) -> AgentResponse:
        """Helper to create standardized response"""
        return AgentResponse(
            from_agent=self.name,
            to_agent=message.from_agent,
            task_id=message.task_id,
            status=status,
            data=data,
            sources=sources or [],
            execution_time=execution_time,
            confidence=confidence
        )


class ResearchAgent(BaseAgent):
    """
    Base class for agents that perform research using AI

    Research agents use Gemini AI to gather information, analyze data, and synthesize insights.
    They maintain an in-memory cache to avoid redundant API calls for the same research.

    Note: This implementation uses AI-based research rather than web scraping. The agents
    leverage Gemini's knowledge base to provide factual, current information without
    requiring external web search APIs.
    """

    def __init__(self, name: str, role: str, model=None):
        """
        Initialize a research agent

        Args:
            name: Agent name (e.g., 'Competitor_Research_Agent')
            role: Agent's role description (e.g., 'Market Intelligence Analyst')
            model: Optional Gemini model name (defaults to gemini-2.0-flash-exp in subclasses)
        """
        super().__init__(name, role, model)
        self.research_cache = {}

    def cache_research(self, key: str, data: Any) -> None:
        """
        Cache research results for reuse

        Args:
            key: Unique cache key
            data: Data to cache (any JSON-serializable type)
        """
        self.research_cache[key] = {
            'data': data,
            'timestamp': datetime.now().isoformat()
        }

    def get_cached(self, key: str) -> Optional[Any]:
        """
        Retrieve cached research data

        Args:
            key: Cache key to look up

        Returns:
            Cached data if found, None otherwise
        """
        if key in self.research_cache:
            return self.research_cache[key]['data']
        return None


@dataclass
class ContentBlueprint:
    """Structured plan for content generation"""
    page_id: str
    pattern_id: str
    pattern_name: str
    funnel_stage: str  # bottom, mid, top
    generation_model: str  # Model 1, Model 2
    required_agents: List[str]
    sections_needed: List[str]
    research_requirements: List[Dict[str, Any]]
    priority: str

    def to_dict(self):
        return {
            'page_id': self.page_id,
            'pattern_id': self.pattern_id,
            'pattern_name': self.pattern_name,
            'funnel_stage': self.funnel_stage,
            'generation_model': self.generation_model,
            'required_agents': self.required_agents,
            'sections_needed': self.sections_needed,
            'research_requirements': self.research_requirements,
            'priority': self.priority
        }


@dataclass
class PageOutput:
    """Final page output structure"""
    page_id: str
    pattern_id: str
    status: str

    # SEO & Structure
    post_title: str
    url_slug: str
    meta_title: str
    meta_description: str

    # Content Sections
    hero_section: Dict[str, str]
    problem_agitation: str
    solution_overview: str
    comparison_table_json: List[Dict[str, str]] = None
    feature_sections: List[Dict[str, str]] = None
    faq_json: List[Dict[str, str]] = None
    final_cta: str = ""
    schema_markup: List[Dict[str, Any]] = None

    # Metadata
    pseo_variables: Dict[str, str] = None
    research_sources: List[Dict[str, str]] = None
    quality_score: float = 0.0
    uniqueness_check: str = "passed"
    generated_at: str = None
    generation_model: str = ""
    agents_used: List[str] = None

    def __post_init__(self):
        if self.generated_at is None:
            self.generated_at = datetime.now().isoformat()
        if self.pseo_variables is None:
            self.pseo_variables = {}
        if self.research_sources is None:
            self.research_sources = []
        if self.agents_used is None:
            self.agents_used = []
        if self.comparison_table_json is None:
            self.comparison_table_json = []
        if self.feature_sections is None:
            self.feature_sections = []
        if self.faq_json is None:
            self.faq_json = []
        if self.schema_markup is None:
            self.schema_markup = []

    def to_dict_public(self):
        """
        Export user-facing content only (excludes internal metadata).
        Use this for CSV exports, API responses, and WordPress imports.
        All content is keyword-relevant and SEO-optimized.
        """
        return {
            'page_id': self.page_id,
            'pattern_id': self.pattern_id,
            'status': self.status,
            'post_title': self.post_title,
            'url_slug': self.url_slug,
            'meta_title': self.meta_title,
            'meta_description': self.meta_description,
            'hero_section': self.hero_section,
            'problem_agitation': self.problem_agitation,
            'solution_overview': self.solution_overview,
            'comparison_table_json': self.comparison_table_json,
            'feature_sections': self.feature_sections,
            'faq_json': self.faq_json,
            'final_cta': self.final_cta,
            'schema_markup': self.schema_markup,
            'generated_at': self.generated_at
        }

    def to_dict(self):
        """
        Export complete data including internal metadata.
        Use this for debugging, quality control, and analytics.
        """
        return {
            'page_id': self.page_id,
            'pattern_id': self.pattern_id,
            'status': self.status,
            'post_title': self.post_title,
            'url_slug': self.url_slug,
            'meta_title': self.meta_title,
            'meta_description': self.meta_description,
            'hero_section': self.hero_section,
            'problem_agitation': self.problem_agitation,
            'solution_overview': self.solution_overview,
            'comparison_table_json': self.comparison_table_json,
            'feature_sections': self.feature_sections,
            'faq_json': self.faq_json,
            'final_cta': self.final_cta,
            'schema_markup': self.schema_markup,
            'generated_at': self.generated_at,
            # Internal metadata (for debugging/analytics only)
            'pseo_variables': self.pseo_variables,
            'research_sources': self.research_sources,
            'quality_score': self.quality_score,
            'uniqueness_check': self.uniqueness_check,
            'generation_model': self.generation_model,
            'agents_used': self.agents_used
        }

    def to_json(self, indent=2, public_only=False):
        """
        Convert to JSON string.

        Args:
            indent: JSON indentation level
            public_only: If True, excludes internal metadata (default: False)
        """
        if public_only:
            return json.dumps(self.to_dict_public(), indent=indent)
        return json.dumps(self.to_dict(), indent=indent)
