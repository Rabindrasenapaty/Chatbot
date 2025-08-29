from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_groq import ChatGroq
from  langgraph.graph.message import add_messages
import re
from langgraph.checkpoint.memory import MemorySaver

from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Fetch API key
api_key = os.getenv("GROQ_API_KEY")

model = ChatGroq(api_key=api_key, model="gemma2-9b-it")


class ChatState(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]

def chat_node(state: ChatState):

    # take user query from state
    messages = state['messages']

    # send to llm
    response = model.invoke(messages)

    # response store state
    return {'messages': [response]}






checkpointer=MemorySaver()

graph = StateGraph(ChatState)

# add nodes
graph.add_node('chat_node', chat_node)

graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

chatbot = graph.compile(checkpointer=checkpointer)

# CONFIG={'configurable':{'thread_id':'thread_1'}}
# response=chatbot.invoke(
#     {'messages':[HumanMessage(content='Hi my name i snitish')]},
#     config=CONFIG
# )
# print(chatbot.get_state(config=CONFIG).values['messages'])