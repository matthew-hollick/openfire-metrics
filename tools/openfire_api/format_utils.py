#!/usr/bin/env python3
"""
Shared formatting utilities for OpenFire tools

# Copyright 2025 Ignite Realtime Community
# Licensed under the Apache License, Version 2.0
# SPDX-License-Identifier: Apache-2.0
"""

import json
from typing import Any, Dict, List


def format_as_json(data: Any, indent: int = 2) -> str:
    """
    Format data as JSON string.
    
    Args:
        data: Data to format
        indent: JSON indentation level
        
    Returns:
        str: Formatted JSON string
    """
    return json.dumps(data, indent=indent, sort_keys=True, default=str)


def format_as_text(data: Any, title: str = "Data") -> str:
    """
    Format data as text string.
    
    Args:
        data: Data to format
        title: Title for the data
        
    Returns:
        str: Formatted text string
    """
    if isinstance(data, dict):
        return _format_dict_as_text(data, title)
    elif isinstance(data, list):
        return _format_list_as_text(data, title)
    else:
        return f"{title}: {data}"


def _format_dict_as_text(data: Dict, title: str) -> str:
    """
    Format dictionary as text string.
    
    Args:
        data: Dictionary to format
        title: Title for the data
        
    Returns:
        str: Formatted text string
    """
    lines = [f"{title}:"]
    for key, value in data.items():
        if isinstance(value, (dict, list)):
            lines.append(f"  {key}:")
            lines.append(_indent_text(format_as_text(value), 4))
        else:
            lines.append(f"  {key}: {value}")
    return "\n".join(lines)


def _format_list_as_text(data: List, title: str) -> str:
    """
    Format list as text string.
    
    Args:
        data: List to format
        title: Title for the data
        
    Returns:
        str: Formatted text string
    """
    if not data:
        return f"{title}: None"
    
    lines = [f"{title} ({len(data)} items):" if title else f"({len(data)} items):"]
    for i, item in enumerate(data):
        if isinstance(item, (dict, list)):
            lines.append(f"  [{i}]:")
            lines.append(_indent_text(format_as_text(item), 4))
        else:
            lines.append(f"  [{i}]: {item}")
    return "\n".join(lines)


def _indent_text(text: str, spaces: int = 2) -> str:
    """
    Indent text lines.
    
    Args:
        text: Text to indent
        spaces: Number of spaces to indent
        
    Returns:
        str: Indented text
    """
    indent = " " * spaces
    return "\n".join(indent + line if line else line for line in text.split("\n"))
