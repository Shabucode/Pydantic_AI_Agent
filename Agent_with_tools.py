"""
Agent with tools
This example shows how to enhance agents with custom tools.
Key concepts:
- Creating and registering tools - tool/toolplain
- Accessing context in tools
"""
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai import Agent, ModelRetry, RunContext, Tool
from utils.markdown import to_markdown


model = OpenAIModel('gpt-4')
shipping_info_db: Dict[str, str] = {
    "12345": "shipped on 26/03/2025",
    "67890": "out for delivery",
}

#Agent with structured output and dependencies
agent3 = Agent(
    model=model,

)