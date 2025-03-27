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
#define response model
class ResponseModel(BaseModel):
    """Structured response with metadata"""
    response: str
    needs_escalation: bool
    follow_up_required: bool
    sentiment:str = Field(description="Customer sentiment analysis")

#DEfine order schema
#for inputs to llms as well for structured input
class Order(BaseModel):

    """Structure for order details"""
    order_id: str
    status: str
    items: List[str]

#Define Customer Schema
class CustomerDetails(BaseModel):
    """Structure for customer queries"""
    customer_id: str
    name: str
    email: str
    orders: Optional[List[Order]] = None

shipping_info_db: Dict[str, str] = {
    "12345": "shipped on 26/03/2025",
    "67890": "out for delivery",
}

def get_shipping_info(ctx: RunContext[CustomerDetails]) -> str:
    """Get customer shipping information"""
    return shipping_info_db[ctx.deps.orders[0].order_id]
#Agent with structured output and dependencies
agent3 = Agent(
    model=model,
    result_type=ResponseModel,
    deps_type=CustomerDetails,
    retries=3,
    system_prompt=(
        "You are an intelligent customer support agent."
        "Analyse queries carefully and provide structured responses."
        "Use tools to look up relevant information"
        "Always greet the customer and provide a helpful response."
    ),
    tools=[Tool(get_shipping_info, takes_ctx=True)]
)

@agent3.system_prompt
async def add_customer_name(ctx: RunContext[CustomerDetails]) -> str:
    return f"Customer details: {to_markdown(ctx.deps)}"

response = agent3.run_sync(
    user_prompt="What's the staus of my last order", deps=customer
)