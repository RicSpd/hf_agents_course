#####   NOT WORKING due to I don't know   #####

import os
import asyncio
from dotenv import load_dotenv, find_dotenv
from llama_index.core.agent.workflow import AgentWorkflow, ReActAgent
from llama_index.llms.azure_openai import AzureOpenAI

load_dotenv(find_dotenv())


llm = AzureOpenAI(
    model=os.getenv("AZURE_OPENAI_MODEL"),
    engine=os.getenv("AZURE_OPENAI_MODEL"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("OPENAI_API_VERSION"),
    max_tokens=8000
)


# Define some tools
async def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

async def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


# we can pass functions directly without FunctionTool -- the fn/docstring are parsed for the name/description
multiply_agent = ReActAgent(
    name="multiply_agent",
    description="Is able to multiply two integers",
    system_prompt="A helpful assistant that can use a tool to multiply numbers.",
    tools=[multiply],
    llm=llm,
)

addition_agent = ReActAgent(
    name="add_agent",
    description="Is able to add two integers",
    system_prompt="A helpful assistant that can use a tool to add numbers.",
    tools=[add],
    llm=llm,
)


# Create the workflow
workflow = AgentWorkflow(
    agents=[multiply_agent, addition_agent],
    root_agent="multiply_agent",
)


# Define an async function to run the workflow
async def run_workflow():
    if os.getenv('ENV') == 'local':
        message = input('Ask something to your agent: ')
        response = await workflow.run(user_msg=message)
        print(response)


# Run the async function using asyncio
if __name__ == "__main__":
    asyncio.run(run_workflow())