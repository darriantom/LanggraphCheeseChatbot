import streamlit as st
import os
from datetime import date

from langchain_core.messages import AIMessage,HumanMessage
from src.LanggraphCheese.ui.uiconfigfile import Config

REASONING_TOGGLE_KEY = "reasoning_toggle_state"

class LoadStreamlitUI:
    def __init__(self):
        self.config =  Config() # config
        self.user_controls = {}

    def initialize_session(self):
        return {
        "current_step": "requirements",
        "requirements": "",
        "user_stories": "",
        "po_feedback": "",
        "generated_code": "",
        "review_feedback": "",
        "decision": None
    }
  


    def load_streamlit_ui(self):
        st.markdown("""
            <div style='text-align: center; padding: 20px;'>
                <h1>🧀 CheeseBot Assistant</h1>
                <p style='font-size: 1.2em; color: #666;'>Your AI-powered Cheese Expert</p>
            </div>
            """, unsafe_allow_html=True)
        st.session_state.timeframe = ''
        st.session_state.IsFetchButtonClicked = False
        st.session_state.IsSDLC = False

        if REASONING_TOGGLE_KEY not in st.session_state:
            st.session_state[REASONING_TOGGLE_KEY] = True # Default: Show reasoning

        with st.sidebar:
            # Get options from config
            st.divider()
            st.subheader("🧀 About CheeseBot")
            st.markdown("""
            **CheeseBot** is your AI-powered cheese expert assistant that helps you with:
            
            - 🔍 Cheese recommendations
            - 📚 Cheese knowledge and facts
            - 🍷 Wine and food pairings
            - 🧪 Cheese characteristics
            - 💡 Serving suggestions
            
            _Built with LangGraph and OpenAI_
            """)
            st.divider()
            model_options = self.config.get_model_options()
            selected_model = st.selectbox("Select Model", model_options)

            # Initialize chat history and previous model if not present
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = []
            if "prev_model" not in st.session_state:
                st.session_state.prev_model = selected_model

            # If the model has changed, clear chat history
            if selected_model != st.session_state.prev_model:
                st.session_state.chat_history = []
                st.session_state.prev_model = selected_model

            st.checkbox(
                "Show Reasoning Steps", 
                key=REASONING_TOGGLE_KEY
            )
            

            self.user_controls["selected_model"] = selected_model
            self.user_controls["show_reasoning"] = st.session_state[REASONING_TOGGLE_KEY]

            if "state" not in st.session_state:
                st.session_state.state = self.initialize_session()

        return self.user_controls