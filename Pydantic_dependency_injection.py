"""
This code demonstrates how to use dependencies and context in agents
Core concepts:
- Define complex data models with Pydantic
- Inject runtime dependencies
- Use dynamic system prompts
"""
from typing import Dict, List, Optional
from pydantic import BaseModel
from pydantic_ai.models.openai import OpenAIModel

model=OpenAIModel("gpt-4o")
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

)