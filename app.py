import gradio as gr
import requests
from bs4from database import store_content import BeautifulSoup


cont

def llm_api_call(api_key, model, prompt):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }
    data = {
        'model': model,
        'prompt': prompt,
        'max_tokens': 150,
        'temperature': 0.7,
    }
    response = requests.post('https://api.openai.com/v1/completions', headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['choices'][0]['text'].strip()
    else:
        return None
ext = []  # List to store conversation history#
Import LLM API libraries and config
# from config import LLM_API_KEY

def scrape_website(url, question):
    # Send the user's query to the LLM for retrieval
    # This requires using the LLM's API and the API key from config.py
    # For example:
    retrieved_content = llm_retr
        # Evaluate relevance using the LLM
    relevance_prompt = f"Assess the relevance of the following content for the query '{question}':\n{retrieved_content}"
    relevance_score = llm_api_call(LLM_API_KEY, llm, relevance_prompt)
    
    # Store content if relevant
    if relevance_score > 0.5:  # Assuming a threshold of 0.5 for relevance
        store_content(url, retrieved_content)
ieve(LLM_API_KEY, url, question)
    return retrieved_content

def answer_question(llm, question, website_content):

        # Append the current question to the context
    context.append({"question": question, "response": None})# Implement the logic to use the selected LLM to answer the question
    nswer
    # This will require using the LLM's API and the API key from config.py
    # For example:

        # Include context in the prompt sent to the LLM
    prompt = "\n".join([f"Q: {entry['question']}\nA: {entry['response']}" for entry in context if entry['response'] is not None])
    prompt += f"\nQ: {question}\nA: "
    response = llm_api_call(LLM_API_KEY, llm, prompt, website_content)

    # Append the response to the context
    context[-1]['response'] = responseresponse = llm_api_call(LLM_API_KEY, question, website_content)
    return response

llm_options = ["LLM1", "LLM2"]  # Replace with actual LLM options

interface = gr.Interface(
    fn=main,
    inputs=[
        gr.inputs.Textbox(label="Website URL"),
        gr.inputs.Dropdown(choices=llm_options, label="Select LLM"),
        gr.inputs.Textbox(label="Ask a question")
    ],
    outputs=gr.outputs.Textbox(label="Answer")
)

if __name__ == "__main__":
    interface.launch()
