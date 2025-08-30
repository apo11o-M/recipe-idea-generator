import streamlit as st
from st_chat_message import message
from openai import OpenAI
import copy
import uuid

# Create a chat feature where the user can type in messages
# and the screen will display chatgpt's response

clear_btn = st.button("Clear Chat History")
if clear_btn and "chat_history" in st.session_state:
    st.session_state["chat_history"] = []

with open(".env", "r") as file:
    open_ai_api_key = file.read()

client = OpenAI(
    api_key=open_ai_api_key
)

system_prompt = "The user will input some ingredients and some restraints & limitations, please suggest 3 to 5 different dishes from the list of ingredients the user entered and these dishes should meet the conditions the user provided."

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [
        {"role": "system", "content": system_prompt}
    ]

# Display all chat messages on the screen
for chat_message in st.session_state["chat_history"]:
    if chat_message["role"] == "user" and chat_message["content"] != "":
        message(chat_message["content"], is_user=True, key=str(uuid.uuid4()))

    elif chat_message["role"] == "assistant":
        message(chat_message["content"], key=str(uuid.uuid4()))

    else:
        continue

# User sending messages & receiving response from chatgpt
with st.form("input"):
    user_message = st.text_area("Enter your ingredients")

    col_1, col_2 = st.columns([1, 1])

    with col_1:
        check_microwave = st.checkbox("Use Microwave", key="micro", value=True)
        check_oven = st.checkbox("Use Oven", key="oven", value=True)

    with col_2:
        check_stove = st.checkbox("Use Stove", key="stove", value=True)
        check_knife = st.checkbox("Use Knife", key="knife", value=True)

    
    submit_btn = st.form_submit_button("Submit")

    if submit_btn and user_message != "":

        # Add the limitations into our user message as text
        full_message = user_message
        if check_microwave:
            full_message += "(The user puts microwave as an available equiptment)"
        if check_oven:
            full_message += "(The user puts oven as an available equiptment)"
        if check_stove:
            full_message += "(The user puts stove as an available equiptment)"
        if check_knife:
            full_message += "(The user puts a knife as an available tool)"

        # append user message to chat history
        st.session_state["chat_history"].append(
            {"role": "user", "content": user_message}
        )

        # send the message to OpenAI
        send_list = copy.deepcopy(st.session_state["chat_history"])
        send_list[-1]["content"] = full_message
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=send_list
        )

        chatgpt_message = response.choices[0].message.content
        
        # append assistant message to chat history
        st.session_state["chat_history"].append(
            {"role": "assistant", "content": chatgpt_message}
        )

        # refresh our screen
        st.rerun()
