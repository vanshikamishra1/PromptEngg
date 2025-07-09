import streamlit as st
from serpapi import GoogleSearch

st.set_page_config(page_title="Prompt App", layout="centered")
st.title("Prompt Engineering Fundamentals")

API_KEY = st.secrets["SERP_API_KEY"]

task = st.selectbox("Select Prompt Task", [
    "Classification",
    "Summarization",
    "Few-shot Reasoning",
    "Tool-calling (JSON Output)",
    "Chain-of-Thought"
])

user_prompt = st.text_area("Enter your prompt")

def fetch_snippet(prompt):
    params = {
        "engine": "google",
        "q": prompt,
        "api_key": API_KEY
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    snippets = [r.get("snippet", "") for r in results.get("organic_results", [])]
    return "\n".join(snippets[:2]) or "No result."

def run_classification(text):
    if "good" in text or "best" in text:
        return "Classified as: Positive"
    elif "bad" in text or "worst" in text:
        return "Classified as: Negative"
    else:
        return "Classified as: Neutral"

def run_summarization(text):
    return "Summary: " + text.split(".")[0] + "..."

def run_fewshot(prompt):
    return f"Q: What is the capital of France?\nA: Paris\nQ: {prompt}\nA: [Answer]"

def run_toolcalling(prompt):
    return f'{{ "action": "search", "query": "{prompt}" }}'

def run_chain_of_thought(prompt):
    return f"Step 1: Received '{prompt}'.\nStep 2: Retrieved results.\nStep 3: Analyzed.\nStep 4: Answered."

if st.button("Run Prompt"):
    if not user_prompt.strip():
        st.warning("Enter a prompt.")
    else:
        web_context = fetch_snippet(user_prompt)
        st.subheader("Web Snippet")
        st.code(web_context)

        st.subheader("Output")
        if task == "Classification":
            st.code(run_classification(web_context))
        elif task == "Summarization":
            st.code(run_summarization(web_context))
        elif task == "Few-shot Reasoning":
            st.code(run_fewshot(user_prompt))
        elif task == "Tool-calling (JSON Output)":
            st.code(run_toolcalling(user_prompt))
        elif task == "Chain-of-Thought":
            st.code(run_chain_of_thought(user_prompt))
