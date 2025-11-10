#!/usr/bin/env python3
"""
Configuration Loading Utilities
Centralized configuration loading to avoid duplication across modules
"""

import os
import json
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


def load_config(config_dir: str = 'config') -> Dict[str, Any]:
    """
    Load all configuration files from the config directory

    Args:
        config_dir: Path to config directory (default: 'config')

    Returns:
        Dictionary with all loaded configurations:
        {
            'patterns': {...},
            'variables': {...},
            'viral_hooks': {...},
            'content_templates': {...},
            'section_templates': {...}
        }

    Raises:
        FileNotFoundError: If config directory or required files don't exist
        ValueError: If JSON is invalid or required keys are missing
    """

    if not os.path.exists(config_dir):
        raise FileNotFoundError(f"Config directory not found: {config_dir}")

    config = {}
    required_files = ['patterns', 'variables', 'viral_hooks', 'content_templates', 'section_templates']

    for config_name in required_files:
        config_path = os.path.join(config_dir, f'{config_name}.json')

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config[config_name] = json.load(f)
                logger.info(f"✓ Loaded {config_name}.json")
        except FileNotFoundError:
            logger.warning(f"⚠️  Config file not found: {config_path}")
            config[config_name] = {}
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {config_path}: {e}")
        except Exception as e:
            raise RuntimeError(f"Error loading {config_path}: {e}")

    return config


def load_patterns(config_dir: str = 'config') -> Dict[str, Any]:
    """
    Load patterns configuration

    Args:
        config_dir: Path to config directory

    Returns:
        Patterns configuration dictionary
    """
    config_path = os.path.join(config_dir, 'patterns.json')

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            patterns = json.load(f)

        # Validate structure
        if 'patterns' not in patterns:
            raise ValueError("patterns.json must contain 'patterns' key")

        return patterns

    except FileNotFoundError:
        raise FileNotFoundError(f"Patterns config not found: {config_path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in patterns.json: {e}")


def load_variables(config_dir: str = 'config') -> Dict[str, Any]:
    """
    Load variables configuration

    Args:
        config_dir: Path to config directory

    Returns:
        Variables configuration dictionary
    """
    config_path = os.path.join(config_dir, 'variables.json')

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            variables = json.load(f)

        return variables

    except FileNotFoundError:
        raise FileNotFoundError(f"Variables config not found: {config_path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in variables.json: {e}")


def safe_json_parse(text: str) -> Dict[str, Any]:
    """
    Safely parse JSON from AI response, handling markdown code blocks

    Args:
        text: Text containing JSON (possibly wrapped in markdown)

    Returns:
        Parsed JSON as dictionary

    Raises:
        json.JSONDecodeError: If JSON is invalid after cleanup

    Example:
        >>> safe_json_parse('```json\\n{"key": "value"}\\n```')
        {'key': 'value'}
    """

    # Remove leading/trailing whitespace
    text = text.strip()

    # Remove markdown code blocks
    if text.startswith('```json'):
        text = text.split('```json', 1)[1]
    elif text.startswith('```'):
        text = text.split('```', 1)[1]

    if text.endswith('```'):
        text = text.rsplit('```', 1)[0]

    # Clean up again after removing code blocks
    text = text.strip()

    # Parse JSON
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON: {e}")
        logger.error(f"Text content: {text[:200]}...")
        raise


def validate_api_key(api_key: str) -> bool:
    """
    Validate API key format and warn about test keys

    Args:
        api_key: API key to validate

    Returns:
        True if key appears valid

    Raises:
        ValueError: If key format is invalid
    """

    if not api_key or len(api_key) < 20:
        raise ValueError("Invalid API key format: key is too short or empty")

    if api_key.startswith('test_') or api_key == 'mock_api_key':
        logger.warning("⚠️  Using test/mock API key - API calls will not work in production")

    # Don't log the actual key for security
    logger.info(f"✓ API key validated (length: {len(api_key)} chars)")

    return True


def get_pattern_by_id(pattern_id: str, patterns_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get pattern by ID with proper type handling and validation

    Args:
        pattern_id: Pattern ID (string or int)
        patterns_config: Patterns configuration dictionary

    Returns:
        Pattern dictionary

    Raises:
        ValueError: If pattern not found
    """

    patterns_list = patterns_config.get('patterns', [])

    # Convert pattern_id to string for comparison
    pattern_id_str = str(pattern_id)

    for pattern in patterns_list:
        if str(pattern.get('id')) == pattern_id_str:
            return pattern

    # Pattern not found
    available_ids = [p.get('id') for p in patterns_list]
    raise ValueError(
        f"Pattern ID '{pattern_id}' not found in pattern library. "
        f"Available pattern IDs: {available_ids}"
    )


def validate_pattern_variables(pattern: Dict[str, Any], provided_variables: Dict[str, Any]) -> bool:
    """
    Validate that all required variables for a pattern are provided

    Args:
        pattern: Pattern configuration dictionary
        provided_variables: Variables provided for page generation

    Returns:
        True if all required variables are present

    Raises:
        ValueError: If required variables are missing
    """

    required_vars = pattern.get('variables', [])
    provided_keys = set(provided_variables.keys())
    required_keys = set(required_vars)

    missing_vars = required_keys - provided_keys

    if missing_vars:
        raise ValueError(
            f"Missing required variables for pattern '{pattern.get('name')}': {missing_vars}. "
            f"Required: {required_keys}, Provided: {provided_keys}"
        )

    return True
