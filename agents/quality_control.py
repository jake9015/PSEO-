#!/usr/bin/env python3
"""
Quality Control Agent
Validates content quality, accuracy, and brand consistency
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_framework import BaseAgent, AgentMessage, AgentResponse
import google.generativeai as genai
import time
import json
import re


class QualityControlAgent(BaseAgent):
    """Content quality assurance specialist"""

    def __init__(self, model=None):
        super().__init__(
            name="Quality_Control_Agent",
            role="Content Quality Assurance Specialist",
            model=model
        )
        if model:
            self.genai_model = genai.GenerativeModel(model)
        else:
            self.genai_model = genai.GenerativeModel('gemini-2.0-flash-exp')

    def execute(self, message: AgentMessage) -> AgentResponse:
        """Review and validate page content"""
        start_time = time.time()
        self.log_message(message)

        page_data = message.context.get('page_data', {})

        # Run quality checks
        quality_report = self._run_quality_checks(page_data)

        execution_time = time.time() - start_time

        # Determine overall status
        status = "completed" if quality_report['overall_score'] >= 0.7 else "failed"

        return self.create_response(
            message,
            status=status,
            data=quality_report,
            execution_time=execution_time,
            confidence=quality_report['overall_score']
        )

    def _run_quality_checks(self, page_data: dict) -> dict:
        """Execute comprehensive quality validation"""

        checks = {
            'seo_validation': self._check_seo_metadata(page_data),
            'content_completeness': self._check_content_completeness(page_data),
            'brand_voice': self._check_brand_voice(page_data),
            'factual_accuracy': self._check_factual_accuracy(page_data),
            'uniqueness': self._check_uniqueness(page_data),
            'technical_validation': self._check_technical_requirements(page_data)
        }

        # Calculate scores
        scores = [check['score'] for check in checks.values()]
        overall_score = sum(scores) / len(scores)

        # Collect all issues
        all_issues = []
        all_warnings = []
        for check_name, check_result in checks.items():
            all_issues.extend(check_result.get('errors', []))
            all_warnings.extend(check_result.get('warnings', []))

        # Determine approval
        approval_status = "APPROVED" if overall_score >= 0.8 and len(all_issues) == 0 else \
                         "APPROVED_WITH_WARNINGS" if overall_score >= 0.7 else \
                         "REJECTED"

        print(f"\n  📊 Quality Control Report:")
        print(f"    Overall Score: {overall_score:.2f}")
        print(f"    Status: {approval_status}")
        print(f"    Issues: {len(all_issues)}, Warnings: {len(all_warnings)}")

        return {
            'overall_score': overall_score,
            'approval_status': approval_status,
            'checks': checks,
            'issues': all_issues,
            'warnings': all_warnings,
            'recommendations': self._generate_recommendations(checks, all_issues, all_warnings)
        }

    def _check_seo_metadata(self, page_data: dict) -> dict:
        """Validate SEO elements"""
        errors = []
        warnings = []
        score = 1.0

        meta_title = page_data.get('meta_title', '')
        meta_desc = page_data.get('meta_description', '')

        # Meta title validation
        if not meta_title:
            errors.append("Missing meta_title")
            score -= 0.3
        elif len(meta_title) < 50 or len(meta_title) > 60:
            warnings.append(f"Meta title length {len(meta_title)} chars (should be 50-60)")
            score -= 0.1
        if meta_title and 'Sozee' not in meta_title:
            warnings.append("Meta title missing 'Sozee' brand mention")
            score -= 0.05

        # Meta description validation
        if not meta_desc:
            errors.append("Missing meta_description")
            score -= 0.3
        elif len(meta_desc) < 150 or len(meta_desc) > 160:
            warnings.append(f"Meta description length {len(meta_desc)} chars (should be 150-160)")
            score -= 0.1

        # URL slug validation
        url_slug = page_data.get('url_slug', '')
        if not url_slug:
            errors.append("Missing URL slug")
            score -= 0.2
        elif ' ' in url_slug or url_slug != url_slug.lower():
            errors.append("URL slug contains spaces or uppercase")
            score -= 0.15

        return {
            'score': max(0, score),
            'errors': errors,
            'warnings': warnings
        }

    def _check_content_completeness(self, page_data: dict) -> dict:
        """Validate all required content sections exist"""
        errors = []
        warnings = []
        score = 1.0

        required_fields = [
            'post_title',
            'hero_section',
            'problem_agitation',
            'solution_overview',
            'final_cta'
        ]

        for field in required_fields:
            if not page_data.get(field):
                errors.append(f"Missing required field: {field}")
                score -= 0.2

        # Check hero section structure
        hero = page_data.get('hero_section', {})
        if isinstance(hero, dict):
            if not hero.get('h1'):
                errors.append("Hero section missing H1")
                score -= 0.15
            if not hero.get('subtitle'):
                warnings.append("Hero section missing subtitle")
                score -= 0.05
        else:
            errors.append("Hero section is not a dictionary")
            score -= 0.2

        # Check content length
        problem = page_data.get('problem_agitation', '')
        if len(problem) < 200:
            warnings.append("Problem section seems too short")
            score -= 0.05

        solution = page_data.get('solution_overview', '')
        if len(solution) < 150:
            warnings.append("Solution section seems too short")
            score -= 0.05

        return {
            'score': max(0, score),
            'errors': errors,
            'warnings': warnings
        }

    def _check_brand_voice(self, page_data: dict) -> dict:
        """Validate brand voice and tone"""
        errors = []
        warnings = []
        score = 1.0

        # Combine all text content
        text_content = self._extract_all_text(page_data)

        # Check for required brand mentions
        if 'Sozee' not in text_content:
            errors.append("Content missing 'Sozee' brand mention")
            score -= 0.3

        # Check for key value props
        value_props = ['LORA', 'training', 'AI', 'content']
        missing_props = [prop for prop in value_props if prop.lower() not in text_content.lower()]
        if len(missing_props) > 2:
            warnings.append(f"Missing key value propositions: {', '.join(missing_props)}")
            score -= 0.1

        # Check tone (basic sentiment check)
        if text_content:
            negative_words = ['cannot', 'impossible', "won't work", 'failure', 'terrible']
            neg_count = sum(1 for word in negative_words if word in text_content.lower())
            if neg_count > 3:
                warnings.append("Content may be overly negative")
                score -= 0.1

        return {
            'score': max(0, score),
            'errors': errors,
            'warnings': warnings
        }

    def _check_factual_accuracy(self, page_data: dict) -> dict:
        """Check for obvious factual errors or hallucinations"""
        errors = []
        warnings = []
        score = 1.0

        text_content = self._extract_all_text(page_data)

        # Check for common hallucinations
        hallucination_patterns = [
            (r'\$\d+,\d+\+', 'Specific pricing claims that may be inaccurate'),
            (r'\d{2,}%\s*(increase|decrease|more|less)', 'Specific percentage claims without source'),
            (r'(guaranteed|promise|never|always)\s+\w+', 'Absolute claims that may be too strong')
        ]

        for pattern, warning_msg in hallucination_patterns:
            if re.search(pattern, text_content, re.IGNORECASE):
                warnings.append(warning_msg)
                score -= 0.05

        # Check competitor mentions match variables
        competitor = page_data.get('pseo_variables', {}).get('competitor', '')
        if competitor and competitor not in text_content:
            pattern_id = page_data.get('pattern_id', '')
            if pattern_id in ['1', '4', '5']:  # Competitor patterns
                warnings.append(f"Competitor '{competitor}' not mentioned in content")
                score -= 0.1

        return {
            'score': max(0, score),
            'errors': errors,
            'warnings': warnings
        }

    def _check_uniqueness(self, page_data: dict) -> dict:
        """Check for template-itis and repetitive language"""
        warnings = []
        score = 1.0

        text_content = self._extract_all_text(page_data)

        # Check for over-used phrases
        overused_phrases = [
            'revolutionize', 'game-changer', 'cutting-edge',
            'state-of-the-art', 'best-in-class', 'industry-leading'
        ]

        phrase_count = sum(text_content.lower().count(phrase) for phrase in overused_phrases)
        if phrase_count > 3:
            warnings.append("Content uses too many generic marketing phrases")
            score -= 0.1

        # Check for repetitive sentence structures
        sentences = re.split(r'[.!?]+', text_content)
        if len(sentences) > 5:
            starts = [s.strip().split()[0].lower() for s in sentences if s.strip()]
            if starts:
                most_common = max(set(starts), key=starts.count)
                if starts.count(most_common) > len(starts) * 0.3:
                    warnings.append(f"Too many sentences start with '{most_common}'")
                    score -= 0.1

        return {
            'score': max(0, score),
            'errors': [],
            'warnings': warnings
        }

    def _check_technical_requirements(self, page_data: dict) -> dict:
        """Validate technical requirements"""
        errors = []
        warnings = []
        score = 1.0

        # Check JSON structure validity
        try:
            comparison_table = page_data.get('comparison_table_json', [])
            if comparison_table and not isinstance(comparison_table, list):
                errors.append("comparison_table_json is not a list")
                score -= 0.2
        except:
            errors.append("comparison_table_json is invalid")
            score -= 0.2

        try:
            faqs = page_data.get('faq_json', [])
            if faqs and not isinstance(faqs, list):
                errors.append("faq_json is not a list")
                score -= 0.2
        except:
            errors.append("faq_json is invalid")
            score -= 0.2

        # Check for broken markdown
        problem = page_data.get('problem_agitation', '')
        if problem:
            if problem.count('#') > 0 and problem.count('\n') == 0:
                warnings.append("Markdown formatting may be broken")
                score -= 0.05

        return {
            'score': max(0, score),
            'errors': errors,
            'warnings': warnings
        }

    def _extract_all_text(self, page_data: dict) -> str:
        """Extract all text content from page data"""
        texts = []

        # Hero
        hero = page_data.get('hero_section', {})
        if isinstance(hero, dict):
            texts.append(hero.get('h1', ''))
            texts.append(hero.get('subtitle', ''))

        # Content sections
        texts.append(page_data.get('problem_agitation', ''))
        texts.append(page_data.get('solution_overview', ''))
        texts.append(page_data.get('final_cta', ''))
        texts.append(page_data.get('meta_description', ''))

        return ' '.join(texts)

    def _generate_recommendations(self, checks: dict, issues: list, warnings: list) -> list:
        """Generate actionable recommendations"""
        recommendations = []

        # SEO recommendations
        if checks['seo_validation']['score'] < 0.8:
            recommendations.append("Review and optimize SEO metadata (title, description, URL)")

        # Content recommendations
        if checks['content_completeness']['score'] < 0.8:
            recommendations.append("Add missing content sections or expand existing ones")

        # Brand voice recommendations
        if checks['brand_voice']['score'] < 0.8:
            recommendations.append("Strengthen brand voice and value proposition messaging")

        # Uniqueness recommendations
        if checks['uniqueness']['score'] < 0.9:
            recommendations.append("Reduce generic marketing language and vary sentence structure")

        # Priority fixes
        if issues:
            recommendations.insert(0, f"FIX CRITICAL ISSUES: {', '.join(issues[:3])}")

        return recommendations
