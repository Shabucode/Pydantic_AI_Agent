#Agent with structured, tyoe-safe responses
"""Core concepts
- Pydantic models to define response structure
- type validation and safety
- field desription for model better understanding
"""


import nest_asyncio
from pydantic import BaseModel, Field
from pydantic_ai import Agent, ModelRetry, RunContext, Tool
from pydantic_ai.models.openai import OpenAIModel
from utils.markdown import to_markdown

model=OpenAIModel("gpt-4o")
#define response model
class ResponseModel(BaseModel):
    """Structured response with metadata"""
    response: str
    needs_escalation: bool
    follow_up_required: bool
    sentiment:str = Field(description="Customer sentiment analysis")


agent1 = Agent(
    model=model,
    result_type=ResponseModel,
    system_prompt=(
        "You are an intelligent customer support agent."
        "Analyse queries carefully and provide structures responses."
    ),
)

response = agent1.run_syn("How can I track my order #6789?")
#dump the response in json format
print(response.data.model_dump_json(indent=2))
