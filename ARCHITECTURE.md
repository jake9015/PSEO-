# PSEO System Architecture

## Overview

The PSEO (Programmatic SEO) Landing Page Generator is a **multi-agent AI system** that generates high-quality, SEO-optimized landing pages at scale. The system uses specialized AI agents that work together to create comprehensive, conversion-focused content.

## System Design Philosophy

### Two-Tiered Generation Models

The system supports two generation approaches:

1. **System 1 (Simple)**: Single API call generation
   - File: `generate_pages.py`
   - Use case: Quick generation for testing
   - Agents: Single monolithic prompt

2. **System 2 (Multi-Agent)**: Collaborative agent pipeline
   - Files: `pseo_orchestrator.py`, `batch_generator.py`
   - Use case: Production-quality content
   - Agents: 10 specialized agents working together

## Core Components

### 1. Agent Framework (`agent_framework.py`)

Provides base classes and data structures:

```
BaseAgent (ABC)
├── execute(message) → AgentResponse
├── log_message(message)
└── create_response(...)

ResearchAgent (extends BaseAgent)
├── web_search(query)
├── web_fetch(url)
├── cache_research(key, data)
└── get_cached(key)
```

**Key Data Structures:**
- `AgentMessage`: Inter-agent communication
- `AgentResponse`: Agent task results
- `ContentBlueprint`: Content generation plan
- `PageOutput`: Final structured page data

### 2. Orchestrator (`pseo_orchestrator.py`)

**AgentManager** coordinates all agent interactions:
- Manages agent lifecycle
- Routes messages between agents
- Tracks task execution
- Logs inter-agent communication

**Workflow Pipeline:**
```
1. Blueprint Creation (Strategist)
2. Research Phase (Parallel):
   ├── Competitor Research
   ├── Audience Insights
   └── Statistics Gathering
3. Content Generation (Sequential):
   ├── Copywriting (main content)
   ├── Comparison Tables
   ├── FAQ Generation
   └── Schema Markup
4. Optimization Phase:
   ├── SEO Optimization
   └── Quality Control
5. Output Assembly
```

### 3. Batch Generator (`batch_generator.py`)

Handles large-scale content generation:
- **Phased rollout**: Validates quality before scaling
- **Progress tracking**: Saves state between runs
- **Error handling**: Graceful degradation
- **Output management**: Structured JSON/CSV exports

**Batch Phases:**
1. Pilot (5 pages) - Initial quality check
2. Phase 1 (25 pages) - Early validation
3. Phase 2 (50 pages) - Scaling confidence
4. Full production

## Agent Architecture

### Agent Hierarchy

```
agents/
├── __init__.py
├── pseo_strategist.py      [Master Planner]
│
├── RESEARCH AGENTS (extend ResearchAgent)
│   ├── competitor_research.py
│   ├── audience_insight.py
│   └── statistics_agent.py
│
├── CONTENT AGENTS (extend BaseAgent)
│   ├── copywriting.py
│   ├── comparison_table.py
│   └── faq_generator.py
│
└── OPTIMIZATION AGENTS (extend BaseAgent)
    ├── seo_optimizer.py
    ├── schema_markup.py
    └── quality_control.py
```

### Agent Communication Pattern

```
┌─────────────────┐
│ PSEO Strategist │ ← Creates blueprint
└────────┬────────┘
         │
         ├──→ [Competitor Research] ──┐
         ├──→ [Audience Insight]    ──┤ Parallel
         └──→ [Statistics]          ──┘ Research
                    │
         ┌──────────┴──────────┐
         ↓                     ↓
    [Copywriting]        [SEO Optimizer]
         │                     │
         ├──→ [Comparison]     │
         ├──→ [FAQ]            │
         └──→ [Schema]         │
                    │          │
         ┌──────────┴──────────┘
         ↓
   [Quality Control] ← Final validation
         │
         ↓
    PageOutput (JSON)
```

## Configuration System

### Config Files (`config/`)

| File | Purpose | Used By |
|------|---------|---------|
| `patterns.json` | 6 landing page formulas | Strategist, Copywriting |
| `variables.json` | Competitors, audiences, platforms | All agents |
| `viral_hooks.json` | Marketing hooks library | Copywriting |
| `content_templates.json` | Pattern-specific prompts | **Underutilized** |

### Pattern-Based Generation

Each landing page follows one of 6 patterns:

1. **Best X for Y** (Bottom-funnel, comparison-heavy)
2. **X vs Y** (Mid-funnel, feature comparison)
3. **How to Use X for Y** (Mid-funnel, tutorial)
4. **X for Y** (Top-funnel, solution-focused)
5. **Is X Good for Y?** (Top-funnel, educational)
6. **Best Alternative to X for Y** (Bottom-funnel, competitive)

## Data Flow

### Input → Output Pipeline

```
Input Variables
├── competitor (e.g., "Asana")
├── audience (e.g., "marketing teams")
├── platform (e.g., "Mac")
└── pattern_id (e.g., "best_x_for_y")
         │
         ↓
    [Strategist creates ContentBlueprint]
         │
         ↓
    [Research agents gather data]
         │
         ↓
    [Content agents generate sections]
         │
         ↓
    [Optimization agents refine]
         │
         ↓
    PageOutput JSON
    ├── SEO metadata
    ├── Hero section
    ├── Problem/solution
    ├── Comparison table
    ├── FAQ (JSON)
    ├── Schema markup
    └── Quality metrics
```

## Quality Control

### Multi-Layer Validation

1. **Agent-level**: Each agent validates its own output
2. **Quality Control Agent**: Final comprehensive review
3. **Test Framework** (`test_single_page.py`): Manual quality testing
4. **Batch Validation**: Phased rollout catches issues early

### Quality Metrics

- Uniqueness check (no generic templates)
- SEO score (meta, structure, keywords)
- Conversion focus (CTAs, value props)
- Factual accuracy (citations required)
- Brand consistency (tone, messaging)

## Scalability Design

### Current Capacity
- 10 specialized agents
- Parallel research execution
- Batch processing with state management
- API rate limiting considerations (Gemini API)

### Scaling Considerations
1. **Agent Pool**: Currently singleton agents, could be pooled
2. **Caching**: Research cache per session (could persist)
3. **API Costs**: Gemini API usage (free tier: 60 RPM)
4. **Output Storage**: Local JSON files (could use database)

## Technology Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.x |
| AI Model | Google Gemini 1.5 Pro/Flash |
| Architecture | Multi-agent system |
| Data Structures | Dataclasses, JSON |
| Dependencies | google-generativeai, pandas, python-dotenv |

## Extension Points

### Adding New Agents

1. Create agent class extending `BaseAgent` or `ResearchAgent`
2. Implement `execute(message)` method
3. Register in `AgentManager.__init__()` (pseo_orchestrator.py)
4. Update blueprint requirements in Strategist

### Adding New Patterns

1. Add pattern to `config/patterns.json`
2. Add pattern-specific prompts to `config/content_templates.json`
3. Update Strategist agent pattern handling
4. Test with `test_single_page.py`

### Adding New Content Sections

1. Update `PageOutput` dataclass in `agent_framework.py`
2. Create dedicated agent or extend Copywriting agent
3. Update orchestration pipeline
4. Add to blueprint requirements

## Error Handling Strategy

1. **Agent failures**: Return `status: "failed"` with error details
2. **Partial failures**: Return `status: "partial"` with available data
3. **Missing data**: Graceful degradation (e.g., skip optional sections)
4. **API errors**: Retry logic with exponential backoff
5. **Validation failures**: Quality Control agent flags issues

## Performance Characteristics

### Timing (Single Page)
- Simple generation (System 1): ~10-30 seconds
- Multi-agent generation (System 2): ~60-120 seconds
  - Research phase: 20-40s (parallel)
  - Content generation: 30-60s (sequential)
  - Optimization: 10-20s

### Resource Usage
- Memory: ~100-200 MB per page generation
- API calls: 5-10 per page (multi-agent mode)
- Storage: ~5-15 KB per page output (JSON)

## Future Architecture Considerations

### Potential Enhancements
1. **True parallelization**: Async/await for agents
2. **Agent communication bus**: Message queue (RabbitMQ, Redis)
3. **Persistent storage**: Database for pages, research cache
4. **Web interface**: Frontend for configuration and monitoring
5. **A/B testing**: Multiple variants per page
6. **Real-time web research**: Live competitor/market data
7. **Multi-language support**: i18n for global markets

## Related Documentation

- **[AGENTS.md](AGENTS.md)**: Detailed agent specifications
- **[README.md](README.md)**: Project overview and setup
- **[START_HERE.md](START_HERE.md)**: Quick start guide
- **[TESTING_GUIDE.md](TESTING_GUIDE.md)**: Quality testing procedures
