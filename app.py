import streamlit as st
import requests

# Rasa REST API endpoint
RASA_URL = "http://localhost:5005/webhooks/rest/webhook"



st.set_page_config(page_title="Healthcare Chatbot", page_icon="💬", layout="centered")

st.title("💬 Healthcare Assistant Chatbot")
st.write("Talk to your AI assistant. Select an option or type your query.")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "bot", "content": "Hello! I’m your healthcare assistant. How can I help you today?"}]

# Function to send message to Rasa
def get_bot_response(user_message):
    response = requests.post(
        RASA_URL,
        json={"sender": "user", "message": user_message}
    )
    if response.status_code == 200:
        messages = response.json()
        if messages:
            return messages[0].get("text", "")
    return "Sorry, I didn’t get that. Can you rephrase?"

# Chat display
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"🧑 **You:** {msg['content']}")
    else:
        st.markdown(f"🤖 **Bot:** {msg['content']}")

# Options as buttons
st.write("### Quick Options")
col1, col2, col3 = st.columns(3)

if col1.button("🩺 Symptom Check"):
    user_input = "symptom_check"
    bot_reply = get_bot_response(user_input)
    st.session_state.messages.append({"role": "user", "content": "I want to check my symptoms"})
    st.session_state.messages.append({"role": "bot", "content": bot_reply})
    st.rerun()

if col2.button("💡 Health Tips"):
    user_input = "ask_tips"
    bot_reply = get_bot_response(user_input)
    st.session_state.messages.append({"role": "user", "content": "Give me health tips"})
    st.session_state.messages.append({"role": "bot", "content": bot_reply})
    st.rerun()

if col3.button("😊 Cheer Me Up"):
    user_input = "mood_unhappy"
    bot_reply = get_bot_response(user_input)
    st.session_state.messages.append({"role": "user", "content": "I'm feeling sad"})
    st.session_state.messages.append({"role": "bot", "content": bot_reply})
    st.rerun()

# Text input for free chat
user_message = st.text_input("💬 Type your message here:", key="input")

if st.button("Send"):
    if user_message.strip() != "":
        st.session_state.messages.append({"role": "user", "content": user_message})
        bot_reply = get_bot_response(user_message)
        st.session_state.messages.append({"role": "bot", "content": bot_reply})
        st.rerun()


