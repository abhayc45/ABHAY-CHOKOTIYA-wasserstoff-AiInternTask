import google.generativeai as genai
from typing import List, Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_completion(prompt: str, model: str = "gemini-1.5-flash") -> str:
    """
    Generates a completion for a given prompt using the specified Gemini model.
    """
    try:
        model = genai.GenerativeModel(model)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""

def identify_themes_and_summarize(query: str, chunks: List[Dict[str, Any]]) -> Dict[str, str]:
    """
    Identifies themes and generates a synthesized summary from a list of document chunks,
    including precise citations.
    """
    # Prepare the context from the document chunks, including metadata for citation
    context = ""
    for i, chunk in enumerate(chunks):
        # The payload from Qdrant is flat, so we access metadata keys directly.
        context += f"Citation: [Source: {chunk.get('source', 'N/A')}, Page: {chunk.get('page', 'N/A')}, Chunk: {chunk.get('chunk', 'N/A')}]\n"
        context += f"Content: {chunk.get('content', '')}\n\n"

    # Create a detailed prompt for the language model
    prompt = f"""
    You are a research assistant. Your task is to answer a query based on the provided text chunks from multiple documents.

    Query: "{query}"

    Here are the relevant text chunks with their citations:
    ---
    {context}
    ---

    Based *only* on the provided text chunks, please perform the following:
    1.  **Identify Main Themes:** Analyze the content and identify the main themes that address the user's query.
    2.  **Synthesize a Comprehensive Answer:** Write a clear, synthesized answer that combines the information from the relevant chunks.
    3.  **Provide Inline Citations:** For every piece of information you use, you MUST include an inline citation that directly corresponds to the source chunk. For example: "The research indicates a significant trend [Source: report.pdf, Page: 5, Chunk: 2]."

    Structure your response as follows:

    **Synthesized Answer:**
    [Your comprehensive, chat-style answer with inline citations.]

    **Main Themes:**
    - [Theme 1]: [Brief description of the theme]
    - [Theme 2]: [Brief description of the theme]
    ...
    """

    # Get the response from the language model
    response_text = get_completion(prompt)

    # The LLM's response is expected to be well-structured.
    return {"summary": response_text}