# gradio-website-qa
A A Gradio interface that accepts a website address and a dropdown to select an LLM. It uses the LLM's retrieval capabilities to extract relevant information from the website and answer questions about the website using the selected LLM.

## Setup Instructions

1. **Clone the repository**:
   ```
   git clone https://github.com/mikeurl/gradio-website-qa.git
   cd gradio-website-qa
   ```

2. **Install the required dependencies**:
   ```
   pip install gradio beautifulsoup4 requests
   ```

3. **Set up the LLM API key**:
   - Open the `config.py` file.
   - Replace `your_llm_api_key_here` with your actual LLM API key.

4. **Run the application**:
   ```
   python app.py
   ```

5. **Use the Gradio interface**:
   - Open the provided URL in your browser.
   Enter the website URL, select the LLM, and ask a question. The application will use the LLM's retrieval capabilities to extract relevant information from the website and provide an answer using the selected LLM.swer using th

The chatbot maintains conversation history, allowing it to provide context-aware responses based on previous interactions. This enhances the conversational experience and ensures more relevant and accurate answers.e selected LLM.
