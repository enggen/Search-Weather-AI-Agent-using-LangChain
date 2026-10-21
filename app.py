import os 
import certifi
import requests 
from dotenv import load_dotenv 

from langchain_openai import ChatOpenAI 
from langchain.tools import tool 
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.tools import tool
from langsmith import Client 

from langchain_classic.agents import create_react_agent, AgentExecutor 

import streamlit as st


# Load environment variables from .env file
os.environ["SSL_CERT_FILE"] = certifi.where()
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
WEATHERSTACK_API_KEY = os.getenv("WEATHERSTACK_API_KEY")

# Streamlit app configuration
st.set_page_config(
    page_title="Agentic AI Assistant", 
    page_icon=":robot_face:",
    layout="centered"
    )

st.title("🤖 Agentic AI Assistant")
st.markdown("Search + Weather AI Agent using LangChain")

# Search Tool
search_tool = TavilySearchResults(num_results=2)

# Weather Tool
@tool
def get_weather_data(city: str) -> str:
    """
    Fetch current weather information for a city.
    """

    url = (
        f"https://api.weatherstack.com/current?"
        f"access_key={WEATHERSTACK_API_KEY}&query={city}"
    )

    response = requests.get(url)

    data = response.json()

    if "current" not in data:
        return f"Could not fetch weather data for {city}"

    return (
        f"City: {city}\n"
        f"Temperature: {data['current']['temperature']}°C\n"
        f"Weather: {data['current']['weather_descriptions'][0]}\n"
        f"Humidity: {data['current']['humidity']}%"
    )

# LLM
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
    openai_api_key=OPENAI_API_KEY
)

# prompt
prompt = Client().pull_prompt("hwchase17/react", dangerously_pull_public_prompt=True)

# Tools 
tools = [search_tool, get_weather_data]

# Create Agent
agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

# Excutor
agent_executor = AgentExecutor(
    agent=agent, 
    tools=tools, 
    verbose=True,
    handle_parsing_errors=True
)

# ==========================================
# UI INPUT
# ==========================================

user_query = st.text_input(
    "Enter your query:",
    placeholder="Example: Find the capital of UK and current weather"
)

# ==========================================
# RUN AGENT
# ==========================================

if st.button("Run Agent"):

    if user_query:

        with st.spinner("Agent is thinking..."):

            try:
                response = agent_executor.invoke({
                    "input": user_query
                })

                st.success("Response Generated")

                st.markdown("## Final Response")
                st.write(response["output"])

            except Exception as e:
                st.error(f"Error: {str(e)}")

    else:
        st.warning("Please enter a query")