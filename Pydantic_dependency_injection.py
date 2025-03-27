"""
This code demonstrates how to use dependencies and context in agents
Core concepts:
- Define complex data models with Pydantic
- Inject runtime dependencies
- Use dynamic system prompts
"""
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai import Agent, ModelRetry, RunContext, Tool
from utils.markdown import to_markdown

model=OpenAIModel("gpt-4o")

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

# Define a simple agent that uses the defined schemas for order and customerdetaills

agent2= Agent(
    model=model,
    result_type=ResponseModel,
    deps_type=CustomerDetails,
    retries=3,
    system_prompt=(
        "You are an intelligent customer support agent."
        "Analyse queries carefully and provide structured responses."
        "Always greet the customer and provide a helpful response."
    ),

)

#for adding new customer
@agent2.system_prompt
async def add_customer_name(ctx: RunContext[CustomerDetails]) -> str:
    return f"Customer details: {to_markdown(ctx.deps)}"

customer = CustomerDetails(
    customer_id="1",
    name="John Doe",
    email="john@doe.com",
    orders=[
        Order(order_id="1234", status="shipped", items=["Green shawl", "Blue salwar"])
            ], 
)

response = agent2.run_sync(user_prompt="What did I order", deps=customer)

response.all_messages()
print(response.data.model_dump_json(indent=2))

print(
    "Customer Details:\n"
    f"Name: {customer.name}\n"
    f"Email: {customer.email}\n"
    "Response Details:\n"
    f"{response.data.response}\n\n"
    "Status:\n"
    f"Followup required: {response.data.follow_up_required}\n"
    f"Needs escalation: {response.data.needs_escalation}\n"


)

"""
Agent with tools
This example shows how to enhance agents with custom tools.
Key concepts:
- Creating and registering tools - tool/toolplain
- Accessing context in tools
"""


shipping_info_db: Dict[str, str] = {
    "12345": "shipped on 26/03/2025",
    "67890": "out for delivery",
}