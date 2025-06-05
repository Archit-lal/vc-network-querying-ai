import streamlit as st
from src.agent import get_agent
from dotenv import load_dotenv

def main_ui():
    load_dotenv()
    st.markdown("<style>div.block-container{max-width:800px;margin:auto;padding-top:3rem} .stApp{background-color:white;color:#333333} h1{text-align:center;color:#FF6B35 !important} h2,h3{color:#333333 !important} .stTextArea textarea{border:2px solid #FF6B35} .stButton button{background-color:#FF6B35;color:white} .stMarkdown p{color:#333333 !important} div[data-testid='stText']{color:#333333 !important}</style>", unsafe_allow_html=True)
    st.title("SpringBank Network")
    query = st.text_area("Ask a question about your network:", placeholder="Who are the top 20 finance executives in my network")
    if st.button("Submit") and query.strip():
        agent_executor = get_agent()
        with st.spinner("Thinking..."):
            result = agent_executor.invoke({"input": query})
        st.subheader("Result")
        st.write(result["output"] if "output" in result else result)
