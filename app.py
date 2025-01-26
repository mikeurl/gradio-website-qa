import gradio as gr
import requests
from bs4 import BeautifulSoup
from database import store_content  # Ensure you have this module

# Function to call the LLM API
def llm_api_call(api_key, model, prompt, additional_context=""):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }
    data = {
        'model': model,
        'prompt': f"{prompt}\n{additional_context}",
        'max_tokens': 150,
        'temperature': 0.7,
    }
    response = requests.post('https://api.openai.com/v1/completions', headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['choices'][0]['text'].strip()
    else:
        return None

# Function to scrape a website and assess content relevance
def scrape_website(api_key, model, url, question):
    try:
        # Retrieve website content
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        retrieved_content = soup.get_text()

        # Evaluate relevance using the LLM
        relevance_prompt = f"Assess the relevance of the following content for the query '{question}':\n{retrieved_content}"
        relevance_score = float(llm_api_call(api_key, model, relevance_prompt))
        
        # Store content if relevant
        if relevance_score > 0.5:  # Threshold for relevance
            store_content(url, retrieved_content)

        return retrieved_content
    except Exception as e:
        return f"Error during scraping: {str(e)}"

# Function to answer a question using LLM
def answer_question(api_key, model, question, website_content, context):
    # Include previous context in the prompt
    prompt = "\n".join([f"Q: {entry['question']}\nA: {entry['response']}" for entry in context if entry['response']])
    prompt += f"\nQ: {question}\nA: "

    # Call LLM to generate an answer
    response = llm_api_call(api_key, model, prompt, additional_context=website_content)
    context.append({"question": question, "response": response})
    return response

# Main function for the Gradio interface
def main(url, llm, question):
    api_key = "YOUR_API_KEY"  # Replace with your actual API key
    context = []  # Initialize conversation history

    # Scrape website for content
    website_content = scrape_website(api_key, llm, url, question)
    if "Error" in website_content:
        return website_content  # Return error message if scraping fails

    # Answer the user's question
    answer = answer_question(api_key, llm, question, website_content, context)
    return answer

# Define LLM options
llm_options = ["LLM1", "LLM2"]  # Replace with actual LLM options

# Create Gradio interface
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
