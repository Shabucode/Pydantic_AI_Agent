"""
Agent with reflection and self correction
This example demonstrates advanced agent capabilities like self correction.
Key concepts:
- Implementing self correction
- Using model retries for automatic retries
- Decorator based tool registration
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

shipping_info_db: Dict[str, str] = (
    "#2378": "Shipped on 27/03/2025",
    "#4567": "Out for delivery",
)

customer = CustomerDetails(
    customer_id="1234",
    name="John Doe",
    email="johndoe@example.com",
)

agent4 = Agent(
    model=model,
    result_type=ResponseModel,
    deps_type=CustomerDetails,
    retries=3,
    system_prompt=(
        "You are an intelligent customer support agent"
        "Analyse queries carefully and provide structured response"
        "Use tools to look up relevant information"
        "Always greet customer and provide helpful response"
    ),
)

@agent4.system_prompt
async def get_shipping_status(order_id: str) -> str:
    """ Get the shipping status for the given order id"""
    shipping_status = shipping_info_db.get(order_id)
    if shipping_status is None:
        raise ModelRetry(
            f"No shipping information found"
        )
    return shipping_info_db[order_id]

