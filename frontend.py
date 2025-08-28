import streamlit as st
from backend import chatbot
from langchain_core.messages import HumanMessage
import re

# config for checkpointer (must have thread_id)
config = {"configurable": {"thread_id": "thread_1"}}

def clean_response(text):
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

# loading past conversation
for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.text(message["content"])

user_input = st.chat_input("Type here")

if user_input:
    # Add user message
    st.session_state["message_history"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.text(user_input)

    # # ✅ FIX: store the response and pass config
    # response = chatbot.invoke(
    #     {"messages": [HumanMessage(content=user_input)]},
    #     config=config
    # )

    # # clean AI response
    # aimessage = clean_response(response["messages"][-1].content)

    # # Add AI message
    # st.session_state["message_history"].append({"role": "assistant", "content": aimessage})
    # with st.chat_message("assistant"):
    #     st.text(aimessage)


    # ✅ FIX: store the response and pass config
    with st.chat_message('assistant'):
        ai_message=st.write_stream(
            message_chunk.content for message_chunk,metadata in chatbot.stream(
            {"messages": [HumanMessage(content=user_input)]},
            config=config,
            stream_mode='messages'
    )
        )

   

    # Add AI message
    st.session_state["message_history"].append({"role": "assistant", "content": ai_message})




    
