import streamlit as st
from backend import chatbot
from langchain_core.messages import HumanMessage
import re
import uuid

#**************************8utility functions****************************************8
def generate_thread_id():
    thread_id=uuid.uuid4()
    return thread_id



def clean_response(text):
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()


def reset_chat():
    thread_id=generate_thread_id()
    st.session_state['thread_id']=thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history']=[]

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)


def load_conversation(thread_id):
    state = chatbot.get_state(config={"configurable": {"thread_id": thread_id}})
    values = getattr(state, "values", {}) or {}
    return values.get("messages", [])

# *****************************Session setup******************************************

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads']=[]

add_thread(st.session_state['thread_id'])

#*****************************Sidebar UI************************************
st.sidebar.title('Langgraph Chatbot')
if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.header('My Conversations')

for thread_id in st.session_state['chat_threads'][::-1]:
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id']=thread_id
        messages=load_conversation(thread_id)

        temp_messages=[]

        for msg in messages:
            if isinstance(msg,HumanMessage):
                role='user'
            else:
                role='assistant'
            temp_messages.append({'role':role,'content':msg.content})

        st.session_state['message_history']=temp_messages





# config for checkpointer (must have thread_id)
config = {"configurable": {"thread_id": st.session_state['thread_id']}}

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




    
