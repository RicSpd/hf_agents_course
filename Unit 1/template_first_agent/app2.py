import os
import datetime
import requests
import pytz
import yaml
from dotenv import load_dotenv, find_dotenv
from smolagents import CodeAgent, DuckDuckGoSearchTool, HfApiModel, load_tool, tool, AzureOpenAIServerModel
from tools.final_answer import FinalAnswerTool
import streamlit as st

load_dotenv(find_dotenv())


@tool
def multiplicator(a: float, b: float)-> str:
    """A tool that has two numbers as input and returns their product.
    Args:
        a: integer or decimal number
        b: integer or decimal number
    """
    try:
        return str(a * b)
    except Exception as e:
        return f"Error multiply the two inputs: {str(e)}"

@tool
def get_current_time_in_timezone(timezone: str) -> str:
    """A tool that fetches the current local time in a specified timezone.
    Args:
        timezone: A string representing a valid timezone (e.g., 'America/New_York').
    """
    try:
        # Create timezone object
        tz = pytz.timezone(timezone)
        # Get current time in that timezone
        local_time = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        return f"The current local time in {timezone} is: {local_time}"
    except Exception as e:
        return f"Error fetching time for timezone '{timezone}': {str(e)}"


final_answer = FinalAnswerTool()

# If the agent does not answer, the model is overloaded, please use another model or the following Hugging Face Endpoint that also contains qwen2.5 coder:
# model_id='https://pflgm2locj2t89co.us-east-1.aws.endpoints.huggingface.cloud' 

# model = HfApiModel(
#     max_tokens=2096,
#     temperature=0.5,
#     model_id='Qwen/Qwen2.5-Coder-32B-Instruct',# it is possible that this model may be overloaded
#     custom_role_conversions=None,
# )

# OpenAI deployment
model = AzureOpenAIServerModel(
    model_id=os.getenv("AZURE_OPENAI_MODEL"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("OPENAI_API_VERSION")    
)

# Import tool from Hub
image_generation_tool = load_tool("agents-course/text-to-image", trust_remote_code=True)

with open("prompts.yaml", 'r') as stream:
    prompt_templates = yaml.safe_load(stream)
    
agent = CodeAgent(
    model=model,
    tools=[final_answer, image_generation_tool, multiplicator, get_current_time_in_timezone], ## add your tools here (don't remove final answer)
    max_steps=6,
    verbosity_level=1,
    grammar=None,
    planning_interval=None,
    name=None,
    description=None,
    prompt_templates=prompt_templates
)

if os.getenv('ENV') == 'local':

    def submit():
        st.session_state.user_input = st.session_state.question_box
        st.session_state.question_box = ""

    st.title("Chat with Riccardo's agent!")

    # Initialize session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Input from user
    user_input = st.text_input("Ask a question: ", key="question_box", on_change=submit)

    # Display the response from the AI agent
    if user_input:
        response = agent.run(user_input)
        st.session_state.chat_history.append({"question": user_input, "response": response})
        # st.session_state.user_input = ""   # Clear the input text box

    # Display chat history
    for chat in st.session_state.chat_history:
        st.write("You: " + str(chat["question"]))
        st.write("AI Agent: " + str(chat["response"]))

else:
    GradioUI(agent).launch()