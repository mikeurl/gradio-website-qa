import gradio as gr
import requests
from bs4 import BeautifulSoup
from database import store_content, retrieve_content

# Function to call an LLM API
def llm_api_call(api_key, model, prompt):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    data = {
        "model": model,
        "prompt": prompt,
        "max_tokens": 150,
        "temperature": 0.7,
    }
    response = requests.post("https://api.openai.com/v1/completions", headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["text"].strip()
    else:
        return f"Error: {response.status_code} - {response.text}"

# Function to scrape website content
def scrape_website(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        return soup.get_text()
    except Exception as e:
        return f"Error while scraping the website: {str(e)}"

# Function to answer questions based on website content
def answer_question(url, llm, question, api_key):
    # Check if cached content exists
    cached_content = retrieve_content(url)
    if cached_content:
        website_content = cached_content
    else:
        # Scrape website content if not cached
        website_content = scrape_website(url)
        if "Error" not in website_content:
            store_content(url, website_content)

    # Combine the website content and the question into the prompt
    prompt = f"Based on the following content:\n{website_content}\nAnswer the question: {question}"
    response = llm_api_call(api_key, llm, prompt)
    return response

# Define the Gradio interface function
def main(url, llm, question):
    api_key = "YOUR_API_KEY"  # Replace with your actual API key
    response = answer_question(url, llm, question, api_key)
    return response

# Define LLM options
llm_options = ["gpt-3.5-turbo", "davinci"]  # Replace with actual LLM options

# Create Gradio Interface using the latest syntax
with gr.Blocks() as interface:
    gr.Markdown("# Website QA Tool")
    gr.Markdown(
        "Scrape a website, analyze its content, and answer your question using a selected LLM model."
    )
    with gr.Row():
        url_input = gr.Textbox(label="Website URL", placeholder="Enter a website URL")
        llm_dropdown = gr.Dropdown(choices=llm_options, label="Select LLM")
        question_input = gr.Textbox(label="Ask a question", placeholder="Enter your question")
    answer_output = gr.Textbox(label="Answer")
    submit_button = gr.Button("Submit")

    submit_button.click(
        fn=main,
        inputs=[url_input, llm_dropdown, question_input],
        outputs=answer_output,
    )

# Launch the Gradio interface
if __name__ == "__main__":
    interface.launch()
