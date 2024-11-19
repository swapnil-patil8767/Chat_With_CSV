import streamlit as st
import os
import tempfile
import pandas as pd
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize the language model
llm = ChatGroq(
    temperature=0,
    groq_api_key=GROQ_API_KEY,
    model_name="llama-3.1-70b-versatile"
)

# Function to create agent with the given CSV file path
def create_agent_with_csv(csv_path):
    return create_csv_agent(llm, csv_path, verbose=True, allow_dangerous_code=True)

# Streamlit app
st.title("CSV Query Application 📊 ")

# Upload CSV file
uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type="csv")

# Store the uploaded file in a temporary location
if uploaded_file:
    # Create a temporary file to store the CSV
    temp_dir = tempfile.gettempdir()
    csv_path = os.path.join(temp_dir, "uploaded_file.csv")
    
    # Delete the previous file if it exists
    if os.path.exists(csv_path):
        os.remove(csv_path)
    
    # Save the new file
    with open(csv_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Load CSV file into DataFrame for preview
    df = pd.read_csv(csv_path)
    st.write("Preview of uploaded data:")
    st.dataframe(df.head())

    # Create agent with the new CSV path
    agent_executer = create_agent_with_csv(csv_path)

    # Input box for user question
    user_question = st.text_input("Ask a question about the data:")

    # Run query if a question is entered
    if user_question:
        result = agent_executer.invoke(user_question)
        try:
            output_value = result.get("output", "No output found")
            st.write("Answer:")
            st.write(output_value)
        except AttributeError:
            st.write("Unexpected response format.")
