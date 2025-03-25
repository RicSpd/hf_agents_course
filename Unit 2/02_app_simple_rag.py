import os
from dotenv import load_dotenv, find_dotenv
from smolagents import CodeAgent, DuckDuckGoSearchTool, HfApiModel

load_dotenv(find_dotenv())


# Initialize the search tool
search_tool = DuckDuckGoSearchTool()

# Initialize the model
model = HfApiModel()

agent = CodeAgent(
    model=model,
    tools=[search_tool],
)

if os.getenv('ENV') == 'local':
    message = input('Ask something to your agent: ')
    # agent.run("Search for luxury superhero-themed party ideas, including decorations, entertainment, and catering.")
    result = agent.run(message)
    result