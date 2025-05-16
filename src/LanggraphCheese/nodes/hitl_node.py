import streamlit as st
from src.LanggraphCheese.graph.graph_state import GraphState
from langchain_core.callbacks.manager import (
    dispatch_custom_event,
)
from langgraph.types import interrupt


class HITLNode:

    def get_human_feedback(self, state: GraphState) -> GraphState:
        print("get_human_feedback")
        st.session_state.current_feedback_state = True
        return interrupt(state.model_dump())  # or just interrupt(state)

