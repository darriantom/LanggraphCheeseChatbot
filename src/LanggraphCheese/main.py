import streamlit as st
import json
from src.LanggraphCheese.UserInterface.streamlitUserInterface.load_InterfaceUI import LoadStreamlitUI
from src.LanggraphCheese.model.model import OpenAiModel
from src.LanggraphCheese.graph.graph_builder import GraphBuilder
from src.LanggraphCheese.UserInterface.streamlitUserInterface.display_result import DisplayResultStreamlit

# MAIN Function START
def show_langgraph_diagram():
    st.sidebar.subheader("🔄 Process Flow")
    st.sidebar.graphviz_chart('''
    digraph LangGraph {
        rankdir=TB;
        node [fontname="Arial", fontsize=12, shape=rect, style="rounded,filled", margin=0.2];
        edge [fontname="Arial", fontsize=10, penwidth=1.5];
        
        // Node styles
        START [shape=circle, style=filled, color="#4CAF50", fontcolor=white, label="Start"];
        END [shape=circle, style=filled, color="#F44336", fontcolor=white, label="End"];
        Reasoning_node [fillcolor="#2196F3", fontcolor=white, label="Reasoning_node"];
        Gen_sql_query_node [fillcolor="#9C27B0", fontcolor=white, label="Generate SQL"];
        sql_search_node [fillcolor="#00BCD4", fontcolor=white, label="SQL Search"];
        vector_search_node [fillcolor="#FF9800", fontcolor=white, label="Vector Search"];
        Data_retrieval_node [fillcolor="#3F51B5", fontcolor=white, label="Data Retrieval"];
        human_assistance_node [fillcolor="#8BC34A", fontcolor=white, label="Human Assistance"];
        generate_response_node [fillcolor="#009688", fontcolor=white, label="Generate Response"];
        
        // Edge styling
        START -> human_assistance_node [color="#4CAF50"];
        Reasoning_node -> Gen_sql_query_node [label="MySQL", color="#9C27B0"];
        Reasoning_node -> vector_search_node [label="VectorDB", color="#FF9800"];
        Gen_sql_query_node -> sql_search_node [color="#00BCD4"];
        sql_search_node -> Data_retrieval_node [color="#3F51B5"];
        vector_search_node -> Data_retrieval_node [color="#3F51B5"];
        Data_retrieval_node -> generate_response_node [label="Ready", color="#009688"];
        human_assistance_node -> START [color="#2196F3"];
        human_assistance_node -> Reasoning_node [color="#2196F3"];
        generate_response_node -> END [color="#F44336"];
        
        // Graph attributes
        graph [pad="0.5", nodesep="0.8", ranksep="0.8"];
    }
''')

def load_langgraph_cheese_app():
    """
    Loads and runs the LangGraph AgenticAI application with Streamlit UI.
    This function initializes the UI, handles user input, configures the LLM model,
    sets up the graph based on the selected use case, and displays the output while 
    implementing exception handling for robustness.
    """
   
    # Load UI
    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()
    
    
    show_langgraph_diagram()
    if not user_input:
        st.error("Error: Failed to load user input from the UI.")
        return
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            
    # Text input for user message
    if st.session_state.IsFetchButtonClicked:
        user_message = st.session_state.timeframe 
    else :
        user_message = st.chat_input("Enter your message:")

    if user_message:
        # try:
            # Configure LLM
        obj_model_config = OpenAiModel(user_controls_input=user_input)
        model = obj_model_config.get_model()
        
        if not model:
            st.error("Error: OpenAI model could not be initialized.")
            return

        # Initialize and set up the graph based on use case

        ### Graph Builder
        graph_builder=GraphBuilder(model)

        # try:
        graph = graph_builder.setup_graph()
        print(user_input['show_reasoning'])
        DisplayResultStreamlit(graph,user_message, user_input['show_reasoning']).display_result_on_ui()
            # except Exception as e:
            #     st.error(f"Error: Graph setup failed - {e}")
            #     print(e)
            #     return
            

        # except Exception as e:
        #         raise ValueError(f"Error Occurred with Exception : {e}")