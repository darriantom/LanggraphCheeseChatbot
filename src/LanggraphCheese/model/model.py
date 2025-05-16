import os
import streamlit as st
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

class OpenAiModel:
    def __init__(self,user_controls_input):
        self.user_controls_input=user_controls_input

    def get_model(self):
        try:
            load_dotenv()
            selected_model=self.user_controls_input['selected_model']

            model = init_chat_model(
                model=selected_model,  # Format: "provider:model_name"
                temperature=0.7
            )

        except Exception as e:
            raise ValueError(f"Error Occurred with Exception : {e}")
        return model