# PSEO Agent Specifications

## Overview

This document provides detailed specifications for all 10 specialized agents in the PSEO landing page generation system. Each agent has a specific role, capabilities, and integration points within the multi-agent pipeline.

---

## Agent Classification

### Research Agents (3)
Extend `ResearchAgent` base class - gather external data and insights:
- Competitor Research Agent
- Audience Insight Agent
- Statistics Agent ⭐ NEW

### Content Agents (4)
Extend `BaseAgent` - create page content:
- PSEO Strategist Agent (Master Planner)
- Copywriting Agent
- Comparison Table Agent ⭐ NEW
- FAQ Generator Agent

### Optimization Agents (3)
Extend `BaseAgent` - refine and validate:
- SEO Optimization Agent
- Schema Markup Agent ⭐ NEW
- Quality Control Agent

---

## 1. PSEO Strategist Agent

**File:** `agents/pseo_strategist.py` (312 lines)
**Type:** Content Agent (BaseAgent)
**Role:** Master planner and content architect

### Responsibilities
- Analyzes page variables (competitor, audience, platform, pattern)
- Creates comprehensive `ContentBlueprint` for page generation
- Determines which agents are needed for the specific pattern
- Plans content sections and research requirements
- Sets page priority and funnel stage

### Input
```python
AgentMessage(
    task={
        'action': 'create_blueprint',
        'variables': {
            'competitor': str,
            'audience': str,
            'platform': str,
            'pattern_id': str
        }
    }
)
```

### Output
```python
AgentResponse(
    data={
        'blueprint': ContentBlueprint(
            page_id=str,
            pattern_id=str,
            pattern_name=str,
            funnel_stage=str,  # 'bottom', 'mid', 'top'
            generation_model=str,  # 'Model 2'
            required_agents=List[str],
            sections_needed=List[str],
            research_requirements=List[Dict],
            priority=str
        )
    }
)
```

### Dependencies
- `config/patterns.json` - Landing page pattern definitions
- `config/variables.json` - Valid competitors, audiences, platforms

### Key Logic
1. Validates input variables
2. Selects appropriate pattern formula
3. Determines funnel stage (bottom/mid/top)
4. Maps pattern requirements to agents
5. Creates section blueprint

### Integration Points
- **Called by:** AgentManager (first step in pipeline)
- **Calls:** None (planning only)
- **Output used by:** All downstream agents

---

## 2. Competitor Research Agent

**File:** `agents/competitor_research.py` (135 lines)
**Type:** Research Agent
**Role:** Competitive intelligence gathering

### Responsibilities
- Researches competitor strengths/weaknesses
- Identifies market positioning
- Finds differentiation opportunities
- Gathers competitor feature sets
- Analyzes pricing strategies

### Input
```python
AgentMessage(
    task={
        'action': 'research_competitor',
        'competitor': str,
        'context': Dict  # From blueprint
    }
)
```

### Output
```python
AgentResponse(
    data={
        'competitor_name': str,
        'strengths': List[str],
        'weaknesses': List[str],
        'unique_features': List[str],
        'pricing_model': str,
        'target_markets': List[str],
        'differentiation_opportunities': List[str]
    },
    sources=List[Dict]  # Citation URLs
)
```

### Research Methods
- Web search for competitor information
- Feature comparison analysis
- Market positioning research
- User review synthesis

### Integration Points
- **Called by:** AgentManager (parallel research phase)
- **Output used by:** Copywriting, Comparison Table, SEO agents

---

## 3. Audience Insight Agent

**File:** `agents/audience_insight.py` (247 lines)
**Type:** Research Agent
**Role:** Audience psychology and needs analysis

### Responsibilities
- Identifies audience pain points
- Discovers emotional triggers
- Maps user goals and motivations
- Analyzes decision-making factors
- Provides messaging recommendations

### Input
```python
AgentMessage(
    task={
        'action': 'analyze_audience',
        'audience': str,
        'competitor': str,
        'context': Dict
    }
)
```

### Output
```python
AgentResponse(
    data={
        'audience_name': str,
        'pain_points': List[str],
        'goals': List[str],
        'emotional_triggers': List[str],
        'decision_factors': List[str],
        'messaging_recommendations': List[str],
        'objections': List[str]
    }
)
```

### Analysis Framework
- Jobs-to-be-Done (JTBD) methodology
- Emotional vs. rational drivers
- Barrier identification
- Value proposition mapping

### Integration Points
- **Called by:** AgentManager (parallel research phase)
- **Output used by:** Copywriting, FAQ Generator agents

---

## 4. Statistics Agent ⭐ NEW

**File:** `agents/statistics_agent.py` (290 lines)
**Type:** Research Agent
**Role:** Market data and statistics generation

### Responsibilities
- Generates credible market statistics
- Creates data-driven insights
- Provides industry benchmarks
- Synthesizes trend data
- Adds authority to content

### Input
```python
AgentMessage(
    task={
        'action': 'generate_statistics',
        'topic': str,
        'context': Dict
    }
)
```

### Output
```python
AgentResponse(
    data={
        'statistics': List[Dict[str, str]],  # stat + context
        'trends': List[str],
        'benchmarks': List[str],
        'sources': List[str]
    }
)
```

### Statistics Types
- Market size and growth rates
- User adoption metrics
- Productivity improvements
- Cost savings data
- Industry benchmarks

### Integration Points
- **Called by:** AgentManager (parallel research phase)
- **Output used by:** Copywriting agent (problem/solution sections)

---

## 5. Copywriting Agent

**File:** `agents/copywriting.py` (276 lines)
**Type:** Content Agent
**Role:** Core content generation

### Responsibilities
- Writes hero section (H1, subheadline, CTA)
- Creates problem/agitation content
- Develops solution overview
- Crafts feature sections
- Writes final CTA

### Input
```python
AgentMessage(
    task={
        'action': 'write_content',
        'blueprint': ContentBlueprint,
        'research': Dict,  # Combined research from all research agents
        'viral_hooks': List[str]
    }
)
```

### Output
```python
AgentResponse(
    data={
        'hero_section': {
            'h1': str,
            'subheadline': str,
            'cta_text': str,
            'cta_subtext': str
        },
        'problem_agitation': str,  # HTML
        'solution_overview': str,  # HTML
        'feature_sections': List[Dict[str, str]],
        'final_cta': str  # HTML
    }
)
```

### Content Patterns
Uses pattern-specific formulas from `config/patterns.json`:
- **Best X for Y**: Comparison-focused, feature-heavy
- **X vs Y**: Side-by-side feature analysis
- **How to Use X for Y**: Step-by-step tutorial format
- **X for Y**: Solution-focused benefits
- **Is X Good for Y?**: Educational Q&A format
- **Best Alternative to X for Y**: Competitive differentiation

### Quality Standards
- Conversion-focused messaging
- Emotional + rational appeals
- Clear value propositions
- Specific, actionable CTAs
- SEO keyword integration

### Integration Points
- **Called by:** AgentManager (content generation phase)
- **Depends on:** All research agents
- **Output used by:** Quality Control, SEO Optimizer

---

## 6. Comparison Table Agent ⭐ NEW

**File:** `agents/comparison_table.py` (241 lines)
**Type:** Content Agent
**Role:** Structured feature comparison generation

### Responsibilities
- Creates feature-by-feature comparisons
- Highlights competitive advantages
- Generates structured JSON tables
- Ensures fair but persuasive comparison

### Input
```python
AgentMessage(
    task={
        'action': 'create_comparison',
        'our_product': str,
        'competitor': str,
        'research': Dict
    }
)
```

### Output
```python
AgentResponse(
    data={
        'comparison_table_json': List[Dict[str, str]],
        # Each row: {'feature': str, 'our_product': str, 'competitor': str}
    }
)
```

### Table Structure
```json
[
    {
        "feature": "Feature Name",
        "our_product": "✓ Detailed capability",
        "competitor": "✗ Limitation or ✓ Their capability"
    }
]
```

### Best Practices
- 5-8 key features
- Factual accuracy
- Balanced presentation
- Visual indicators (✓, ✗, ⚡)
- Mobile-responsive format

### Integration Points
- **Called by:** AgentManager (content generation phase)
- **Depends on:** Competitor Research
- **Output used by:** Quality Control

---

## 7. FAQ Generator Agent

**File:** `agents/faq_generator.py` (206 lines)
**Type:** Content Agent
**Role:** FAQ section creation

### Responsibilities
- Identifies common user questions
- Addresses objections preemptively
- Creates SEO-friendly Q&A
- Generates structured FAQ JSON
- Covers decision-making concerns

### Input
```python
AgentMessage(
    task={
        'action': 'generate_faq',
        'topic': str,
        'research': Dict,
        'audience_objections': List[str]
    }
)
```

### Output
```python
AgentResponse(
    data={
        'faq_json': List[Dict[str, str]]
        # Each: {'question': str, 'answer': str}
    }
)
```

### FAQ Categories
1. **Product/Feature Questions**: "Does X support Y?"
2. **Comparison Questions**: "How is this different from Z?"
3. **Pricing Questions**: "Is there a free trial?"
4. **Use Case Questions**: "Can I use this for [audience need]?"
5. **Technical Questions**: "What platforms does it work on?"

### SEO Optimization
- Long-tail keyword questions
- Natural language queries
- Schema markup compatible
- Featured snippet targeting

### Integration Points
- **Called by:** AgentManager (content generation phase)
- **Depends on:** Audience Insight, Competitor Research
- **Output used by:** Schema Markup, Quality Control

---

## 8. SEO Optimization Agent

**File:** `agents/seo_optimizer.py` (183 lines)
**Type:** Optimization Agent
**Role:** SEO metadata and optimization

### Responsibilities
- Generates SEO title (meta title)
- Creates meta description
- Generates URL slug
- Optimizes post title (H1)
- Ensures keyword optimization

### Input
```python
AgentMessage(
    task={
        'action': 'optimize_seo',
        'content': Dict,  # All page content
        'variables': Dict  # Competitor, audience, platform
    }
)
```

### Output
```python
AgentResponse(
    data={
        'post_title': str,  # WordPress post title
        'url_slug': str,  # kebab-case URL
        'meta_title': str,  # SEO title (50-60 chars)
        'meta_description': str,  # 150-160 chars
        'primary_keyword': str,
        'secondary_keywords': List[str]
    }
)
```

### SEO Best Practices
- **Meta Title**: 50-60 characters, keyword-front-loaded
- **Meta Description**: 150-160 chars, includes CTA
- **URL Slug**: Concise, keyword-rich, readable
- **Keyword Density**: Natural integration, no stuffing
- **SERP Optimization**: Click-worthy, competitive

### Integration Points
- **Called by:** AgentManager (optimization phase)
- **Depends on:** Copywriting agent output
- **Output used by:** Final PageOutput assembly

---

## 9. Schema Markup Agent ⭐ NEW

**File:** `agents/schema_markup.py` (299 lines)
**Type:** Optimization Agent
**Role:** Structured data generation

### Responsibilities
- Generates JSON-LD schema markup
- Creates SoftwareApplication schema
- Adds FAQPage schema
- Includes BreadcrumbList schema
- Ensures Google rich results eligibility

### Input
```python
AgentMessage(
    task={
        'action': 'generate_schema',
        'page_data': Dict,  # All page content
        'faq_json': List[Dict]
    }
)
```

### Output
```python
AgentResponse(
    data={
        'schema_markup': List[Dict[str, Any]]
        # List of schema.org JSON-LD objects
    }
)
```

### Schema Types Generated

#### 1. SoftwareApplication Schema
```json
{
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "Product Name",
    "applicationCategory": "BusinessApplication",
    "offers": {...},
    "aggregateRating": {...}
}
```

#### 2. FAQPage Schema
```json
{
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
        {
            "@type": "Question",
            "name": "Question text?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "Answer text"
            }
        }
    ]
}
```

#### 3. BreadcrumbList Schema
```json
{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [...]
}
```

### SEO Benefits
- Rich snippets in Google search
- FAQ accordion in SERP
- Enhanced click-through rates
- Better indexing signals
- Voice search optimization

### Integration Points
- **Called by:** AgentManager (optimization phase)
- **Depends on:** FAQ Generator, Copywriting
- **Output used by:** Final PageOutput assembly

---

## 10. Quality Control Agent

**File:** `agents/quality_control.py` (372 lines)
**Type:** Optimization Agent
**Role:** Final validation and quality assurance

### Responsibilities
- Validates all content sections
- Checks for completeness
- Ensures uniqueness (no templates)
- Verifies conversion elements
- Calculates quality score

### Input
```python
AgentMessage(
    task={
        'action': 'validate_quality',
        'page_output': PageOutput
    }
)
```

### Output
```python
AgentResponse(
    data={
        'quality_score': float,  # 0.0 - 1.0
        'uniqueness_check': str,  # 'passed' or 'failed'
        'issues': List[str],
        'recommendations': List[str],
        'validation_details': Dict
    }
)
```

### Quality Checks

#### 1. Completeness
- All required sections present
- No placeholder text
- Proper HTML structure
- All CTAs included

#### 2. Uniqueness
- No generic templates
- Specific to competitor/audience
- Original phrasing
- Factual accuracy

#### 3. SEO Quality
- Meta tags within length limits
- Keyword integration
- URL slug format
- Schema markup validity

#### 4. Conversion Optimization
- Clear value propositions
- Multiple CTAs
- Emotional triggers
- Objection handling

#### 5. Content Quality
- Grammar and spelling
- Readability
- Tone consistency
- Brand alignment

### Scoring System
```
Quality Score = Average of:
- Completeness (0-1)
- Uniqueness (0-1)
- SEO (0-1)
- Conversion (0-1)
- Content quality (0-1)
```

**Passing Threshold**: 0.7+ (70%)

### Integration Points
- **Called by:** AgentManager (final validation)
- **Depends on:** All other agents
- **Output used by:** Final PageOutput + decision to publish

---

## Agent Communication Patterns

### 1. Sequential Execution
```
Strategist → Copywriting → SEO → Quality Control
```

### 2. Parallel Research
```
           ┌→ Competitor Research ─┐
Strategist ├→ Audience Insight    ─┤ → Copywriting
           └→ Statistics          ─┘
```

### 3. Dependent Generation
```
Copywriting ─→ FAQ Generator ─→ Schema Markup
```

---

## Agent State Management

### Stateless Execution
- Each agent executes independently
- All context passed via `AgentMessage`
- No persistent state between pages
- Research cache per session only

### Message History
- `AgentManager` logs all messages
- Used for debugging and auditing
- Not used for agent decision-making

---

## Error Handling

### Agent Response Status
- `"completed"`: Successful execution
- `"failed"`: Complete failure (with error details)
- `"partial"`: Partial success (degraded output)

### Graceful Degradation
1. Research agents: Return best-effort data
2. Content agents: Skip optional sections
3. Quality Control: Flag issues but allow output

---

## Performance Optimization

### Caching Strategy
- Research agents cache results per session
- Pattern library loaded once
- Viral hooks shared across agents

### API Efficiency
- Batch similar API calls
- Reuse research data across agents
- Minimize redundant prompts

---

## Extension Guidelines

### Adding a New Agent

1. **Create Agent File**
```python
from agent_framework import BaseAgent, AgentMessage, AgentResponse

class MyNewAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="my_new_agent",
            role="What this agent does"
        )

    def execute(self, message: AgentMessage) -> AgentResponse:
        # Implementation
        return self.create_response(
            message=message,
            status="completed",
            data={...}
        )
```

2. **Register in AgentManager**
```python
# pseo_orchestrator.py
self.agents['my_new_agent'] = MyNewAgent()
```

3. **Update Blueprint Requirements**
```python
# agents/pseo_strategist.py
required_agents.append('my_new_agent')
```

4. **Add to Orchestration Pipeline**
```python
# pseo_orchestrator.py - ContentPipeline
response = self.send_message(
    from_agent='orchestrator',
    to_agent='my_new_agent',
    task={...},
    context={...}
)
```

---

## Related Documentation

- **[ARCHITECTURE.md](ARCHITECTURE.md)**: Overall system architecture
- **[README.md](README.md)**: Project overview
- **[TESTING_GUIDE.md](TESTING_GUIDE.md)**: Quality testing procedures
- **Individual Agent Files**: See `agents/*.py` for implementation details
