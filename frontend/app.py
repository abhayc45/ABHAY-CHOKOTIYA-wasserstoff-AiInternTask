import streamlit as st
import requests
import pandas as pd
import time

# --- Configuration ---
import os

# --- Configuration ---
# Use the Replit environment variable for the backend URL if it exists
BACKEND_URL = os.environ.get("REPLIT_BACKEND_URL", "http://localhost:8000")

# --- Helper Functions ---
def get_document_list():
    """Fetches the list of documents from the backend."""
    try:
        response = requests.get(f"{BACKEND_URL}/documents/")
        if response.status_code == 200:
            return response.json().get("documents", [])
        else:
            st.error(f"Failed to fetch document list: {response.text}")
            return []
    except requests.exceptions.ConnectionError:
        st.error("Connection to backend failed. Is the backend server running?")
        return []

# --- Streamlit UI ---
st.set_page_config(page_title="Document Chatbot", layout="wide")

st.title("📄 Document Research & Theme Identification Chatbot")
st.markdown("Upload your documents, ask questions, and get synthesized answers with precise citations.")

# --- Main Layout ---
col1, col2 = st.columns([1, 2])

with col1:
    st.header("📚 Knowledge Base")

    # Document Upload Section
    with st.expander("➕ Upload New Documents", expanded=True):
        uploaded_files = st.file_uploader(
            "Upload PDFs, text files, or images",
            type=['pdf', 'txt', 'png', 'jpg', 'jpeg', 'jjpg'],
            accept_multiple_files=True
        )
        if st.button("Process Uploaded Files"):
            if uploaded_files:
                with st.spinner("Processing files... This may take a moment."):
                    for uploaded_file in uploaded_files:
                        files = {'file': (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                        try:
                            response = requests.post(f"{BACKEND_URL}/uploadfile/", files=files)
                            if response.status_code == 200:
                                st.success(f"✅ Successfully processed and indexed {uploaded_file.name}")
                            else:
                                st.error(f"❌ Failed to process {uploaded_file.name}: {response.json().get('detail', 'Unknown error')}")
                        except requests.exceptions.RequestException as e:
                            st.error(f"❌ An error occurred while uploading {uploaded_file.name}: {e}")
                # Refresh the document list after upload
                st.rerun()
            else:
                st.warning("Please select files to upload first.")

    # Display Document List
    st.subheader("Uploaded Documents")
    doc_list = get_document_list()
    
    # Add a multi-select for filtering documents
    selected_docs = st.multiselect(
        "Filter documents for your query (optional):",
        options=doc_list,
        default=doc_list  # Default to all documents being selected
    )

with col2:
    st.header("💬 Ask a Question")
    
    query_text = st.text_area("Enter your question here:", height=100)
    
    if st.button("Get Answer"):
        if not query_text:
            st.warning("Please enter a question.")
        elif not selected_docs:
            st.warning("Please select at least one document to query.")
        else:
            with st.spinner("Searching documents and synthesizing answer..."):
                try:
                    # Prepare the request payload
                    payload = {
                        "text": query_text,
                        "documents": selected_docs
                    }
                    response = requests.post(f"{BACKEND_URL}/query/", json=payload)
                    
                    if response.status_code == 200:
                        results = response.json()
                        
                        st.subheader("💡 Synthesized Answer & Themes")
                        st.markdown("---")
                        st.markdown(results.get("summary", {}).get("summary", "No summary could be generated."))
                        st.markdown("---")
                        
                        st.subheader("📖 Relevant Document Excerpts")
                        relevant_docs = results.get("relevant_docs", [])
                        if relevant_docs:
                            # Create a DataFrame for better display
                            citation_data = []
                            for doc in relevant_docs:
                                # The payload is flat, so we access keys directly from the doc object
                                citation_data.append({
                                    "Source": doc.get("source", "N/A"),
                                    "Page": doc.get("page", "N/A"),
                                    "Content": doc.get("content", "N/A")
                                })
                            df = pd.DataFrame(citation_data)
                            st.dataframe(df)
                        else:
                            st.info("No specific document excerpts were found to be highly relevant in the selected documents.")
                            
                    else:
                        st.error(f"Error from server: {response.json().get('detail', 'Unknown error')}")
                except requests.exceptions.RequestException as e:
                    st.error(f"An error occurred while querying: {e}")