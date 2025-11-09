#!/usr/bin/env python3
"""
Schema Markup Agent
Generates structured data (Schema.org JSON-LD) for SEO rich snippets
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_framework import BaseAgent, AgentMessage, AgentResponse
import google.generativeai as genai
import time
import json
from datetime import datetime


class SchemaMarkupAgent(BaseAgent):
    """Generates Schema.org structured data for SEO"""

    def __init__(self, model=None):
        super().__init__(
            name="Schema_Markup_Agent",
            role="Structured Data & Schema Specialist",
            model=model
        )
        if model:
            self.genai_model = genai.GenerativeModel(model)
        else:
            self.genai_model = genai.GenerativeModel('gemini-2.0-flash-exp')

    def execute(self, message: AgentMessage) -> AgentResponse:
        """Generate schema markup for landing page"""
        start_time = time.time()
        self.log_message(message)

        task = message.task
        pattern_id = task.get('pattern_id', '')
        page_data = task.get('page_data', {})
        faqs = task.get('faqs', [])
        meta = task.get('meta', {})

        # Generate appropriate schemas based on pattern
        schemas = self._generate_schemas(
            pattern_id=pattern_id,
            page_data=page_data,
            faqs=faqs,
            meta=meta
        )

        execution_time = time.time() - start_time

        return self.create_response(
            message,
            status="completed",
            data={'schemas': schemas},
            execution_time=execution_time,
            confidence=0.95
        )

    def _generate_schemas(self, pattern_id: str, page_data: dict,
                         faqs: list, meta: dict) -> list:
        """Generate all appropriate schema types for this page"""

        schemas = []

        # 1. ALWAYS: Organization Schema (for brand)
        schemas.append(self._get_organization_schema())

        # 2. ALWAYS: WebPage Schema (basic page info)
        schemas.append(self._get_webpage_schema(page_data, meta))

        # 3. FAQ Schema (if FAQs exist)
        if faqs and len(faqs) > 0:
            schemas.append(self._get_faq_schema(faqs))

        # 4. Pattern-specific schemas
        if pattern_id in ['1', '4']:  # Comparison, Alternative
            # Product comparison schema
            schemas.append(self._get_product_schema(pattern_id, page_data))

        elif pattern_id == '2':  # Best Tool
            # SoftwareApplication with AggregateRating
            schemas.append(self._get_software_application_schema(page_data))

        elif pattern_id == '5':  # Review
            # Review schema with rating
            schemas.append(self._get_review_schema(page_data))

        # 5. Breadcrumb Schema (for all pages)
        schemas.append(self._get_breadcrumb_schema(page_data))

        print(f"  ✓ Generated {len(schemas)} schema types")
        return schemas

    def _get_organization_schema(self) -> dict:
        """Generate Organization schema for Sozee"""
        return {
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": "Sozee",
            "url": "https://sozee.ai",
            "logo": "https://sozee.ai/logo.png",
            "description": "AI-powered content generation platform built specifically for creators. Custom LORA training, 1-click TikTok cloning, and complete SFW/NSFW support.",
            "sameAs": [
                "https://twitter.com/sozee_ai",
                "https://www.linkedin.com/company/sozee-ai"
            ],
            "foundingDate": "2024",
            "areaServed": "Worldwide",
            "contactPoint": {
                "@type": "ContactPoint",
                "contactType": "Customer Support",
                "url": "https://sozee.ai/contact"
            }
        }

    def _get_webpage_schema(self, page_data: dict, meta: dict) -> dict:
        """Generate WebPage schema"""
        h1 = page_data.get('hero', {}).get('h1', 'Sozee AI Content Studio')
        description = meta.get('meta_description', '')

        return {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": h1,
            "description": description,
            "url": "https://sozee.ai/[page-slug]",  # Will be replaced by WordPress
            "datePublished": datetime.now().strftime("%Y-%m-%d"),
            "dateModified": datetime.now().strftime("%Y-%m-%d"),
            "inLanguage": "en-US",
            "publisher": {
                "@type": "Organization",
                "name": "Sozee"
            }
        }

    def _get_faq_schema(self, faqs: list) -> dict:
        """Generate FAQPage schema from FAQ data"""

        faq_entities = []
        for faq in faqs[:10]:  # Limit to 10 FAQs for schema
            faq_entities.append({
                "@type": "Question",
                "name": faq.get('question', ''),
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": faq.get('answer', '')
                }
            })

        return {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": faq_entities
        }

    def _get_product_schema(self, pattern_id: str, page_data: dict) -> dict:
        """Generate Product schema with comparison info"""

        h1 = page_data.get('hero', {}).get('h1', 'Sozee AI Content Studio')

        return {
            "@context": "https://schema.org",
            "@type": "Product",
            "name": "Sozee AI Content Studio",
            "description": "AI-powered content generation platform with custom LORA training, 1-click TikTok cloning, and NSFW support built for creators.",
            "brand": {
                "@type": "Brand",
                "name": "Sozee"
            },
            "offers": {
                "@type": "AggregateOffer",
                "lowPrice": "15",
                "highPrice": "33",
                "priceCurrency": "USD",
                "priceSpecification": {
                    "@type": "UnitPriceSpecification",
                    "price": "15.00",
                    "priceCurrency": "USD",
                    "unitText": "WEEK"
                },
                "availability": "https://schema.org/InStock",
                "url": "https://sozee.ai/pricing"
            },
            "aggregateRating": {
                "@type": "AggregateRating",
                "ratingValue": "4.8",
                "reviewCount": "250",
                "bestRating": "5",
                "worstRating": "1"
            }
        }

    def _get_software_application_schema(self, page_data: dict) -> dict:
        """Generate SoftwareApplication schema for 'Best Tool' pages"""

        return {
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": "Sozee AI Content Studio",
            "applicationCategory": "BusinessApplication",
            "operatingSystem": "Web-based",
            "offers": {
                "@type": "Offer",
                "price": "15.00",
                "priceCurrency": "USD",
                "priceSpecification": {
                    "@type": "UnitPriceSpecification",
                    "price": "15.00",
                    "priceCurrency": "USD",
                    "unitText": "WEEK"
                }
            },
            "aggregateRating": {
                "@type": "AggregateRating",
                "ratingValue": "4.8",
                "reviewCount": "250",
                "bestRating": "5"
            },
            "featureList": [
                "Custom LORA training in 30 minutes",
                "1-click TikTok cloning",
                "SFW and NSFW content support",
                "Hyper-realistic AI generation",
                "Built for OnlyFans and creator platforms",
                "30-second content generation"
            ]
        }

    def _get_review_schema(self, page_data: dict) -> dict:
        """Generate Review schema for review pages"""

        h1 = page_data.get('hero', {}).get('h1', 'Sozee Review')

        return {
            "@context": "https://schema.org",
            "@type": "Review",
            "itemReviewed": {
                "@type": "SoftwareApplication",
                "name": "Sozee AI Content Studio",
                "applicationCategory": "BusinessApplication"
            },
            "reviewRating": {
                "@type": "Rating",
                "ratingValue": "4.8",
                "bestRating": "5",
                "worstRating": "1"
            },
            "author": {
                "@type": "Organization",
                "name": "Sozee Review Team"
            },
            "reviewBody": page_data.get('problem', '')[:500],  # First 500 chars
            "datePublished": datetime.now().strftime("%Y-%m-%d")
        }

    def _get_breadcrumb_schema(self, page_data: dict) -> dict:
        """Generate BreadcrumbList schema"""

        h1 = page_data.get('hero', {}).get('h1', 'Sozee')

        return {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": 1,
                    "name": "Home",
                    "item": "https://sozee.ai"
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": h1,
                    "item": "https://sozee.ai/[page-slug]"  # Will be replaced
                }
            ]
        }

    def _format_schemas_for_wordpress(self, schemas: list) -> str:
        """Format schemas as JSON-LD for WordPress insertion"""

        # Combine all schemas into single JSON-LD script block
        formatted = '<script type="application/ld+json">\n'

        if len(schemas) == 1:
            formatted += json.dumps(schemas[0], indent=2)
        else:
            # Use @graph to combine multiple schemas
            formatted += json.dumps({
                "@context": "https://schema.org",
                "@graph": schemas
            }, indent=2)

        formatted += '\n</script>'

        return formatted
