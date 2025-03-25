import getpass
import os
import nest_asyncio
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

#Function to securely get and set environment variables
def set_env_securely(var_name, prompt):
  value = getpass.getpass(prompt)
  os.environ[var_name] = value

set_env_securely("OPENAI_API_KEY", "Enter your OpenAI API key: ")

# Apply nest_asyncio patch to allow nested event loops in jupyter notebooks
#else it will throw error as already an jupyter event loop is running
nest_asyncio.apply()

model = OpenAIModel("gpt-4o")

agent = Agent(
    model,
    system_prompt="You are a helpful customer support agent. Be concise and friendly",
)

# Basic agent example
response = basic_agent.run_sync("How can I track my order #6879? ")

print(response.data)
print(response.all_messages())
print(response.cost())

response2 = basic_agent.run_sync(
  user_prompt="What was my previous question"
  message_history=response.new_messages(),
)

print(response2.data)