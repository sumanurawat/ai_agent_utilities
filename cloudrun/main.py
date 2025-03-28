"""
# LLM Cloud Run Service
# =====================

## Overview
This Flask application provides a RESTful API for Large Language Model (LLM) inference
using the Hugging Face Inference API. It can be deployed to Google Cloud Run to create
a scalable, serverless LLM service that proxies requests to Hugging Face models.

## Features
- Serves LLM responses via a simple REST API
- Supports various models from Hugging Face
- Handles chat-style conversations with proper formatting
- Includes CORS support for web applications
- Provides health check and model listing endpoints

## Requirements
- Python 3.8+
- Flask
- Requests
- Flask-CORS
- python-dotenv

## Environment Variables
- `HUGGINGFACE_API_KEY`: Your Hugging Face API key (required)
- `PORT`: Port to run the server on (default: 8080)

"""



import os
import datetime
import logging
import requests
import json
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS

# Load environment variables from .env file (if present)
load_dotenv()

# Import model constants
from model_constants import SMALL_MODELS, MEDIUM_MODELS, LARGE_MODELS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
# Default model to use
DEFAULT_MODEL = SMALL_MODELS["MISTRAL_7B"]["id"]

def generate_hf_response(prompt, model_id=None, api_key=None, max_tokens=512, temperature=0.7):
    """
    Generate a response from HuggingFace Inference API
    
    Args:
        prompt: The prompt to send
        model_id: HuggingFace model ID
        api_key: HuggingFace API key
        max_tokens: Maximum number of tokens to generate
        temperature: Temperature for sampling
        
    Returns:
        Generated text response
    """
    # Get API key from parameter, env var, or default
    api_key = api_key or os.environ.get("HUGGINGFACE_API_KEY")
    if not api_key:
        raise ValueError("No Hugging Face API key provided")
        
    # Use provided model or default
    model_id = model_id or DEFAULT_MODEL
    
    # API URL for the specified model
    api_url = f"https://api-inference.huggingface.co/models/{model_id}"
    
    # Set up headers with API key
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Set up payload with parameters
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": max_tokens,
            "temperature": temperature,
            "top_k": 50,
            "top_p": 0.95,
            "do_sample": True,
            "return_full_text": False
        }
    }
    
    # Check if this is a chat-style prompt
    is_chat_format = "User:" in prompt and "Assistant:" in prompt
    
    if is_chat_format:
        # Format for instruction-tuned models like Mistral
        formatted_prompt = f"<s>[INST] {prompt.strip()} [/INST]</s>"
        payload["inputs"] = formatted_prompt
    else:
        payload["inputs"] = prompt
    
    # Make request to HuggingFace API
    try:
        logger.info(f"Sending request to {model_id}")
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()  # Raise exception for error status codes
        
        result = response.json()
        
        # Extract generated text from response (handle various response formats)
        if isinstance(result, list) and len(result) > 0:
            if "generated_text" in result[0]:
                return result[0]["generated_text"]
            else:
                return str(result[0])
        elif isinstance(result, dict) and "generated_text" in result:
            return result["generated_text"]
        else:
            return str(result)
            
    except Exception as e:
        logger.error(f"Error calling HuggingFace API: {str(e)}")
        raise

@app.route("/", methods=["GET"])
def hello_world():
    """Simple Hello World route with query parameter support."""
    name = request.args.get("name", os.environ.get("NAME", "World"))
    return f"Hello {name}!"

@app.route("/models", methods=["GET"])
def list_models():
    """Return a list of available models"""
    return jsonify({
        "small_models": SMALL_MODELS,
        "medium_models": MEDIUM_MODELS,
        "large_models": LARGE_MODELS
    })

@app.route("/generate", methods=["POST"])
def generate():
    """Use HuggingFace model to generate a response."""
    # Parse the request
    data = request.get_json(silent=True) or {}
    prompt = data.get("prompt", "")
    model_id = data.get("model_id", None)
    max_tokens = data.get("max_tokens", 512)
    temperature = data.get("temperature", 0.7)
    
    if not prompt:
        return jsonify({"error": "Missing 'prompt' in request"}), 400
        
    try:
        # Add more detailed DEBUG logs
        logger.info(f"Received prompt: {prompt[:50]}...")  # Show start of prompt
        logger.info(f"Using model: {model_id or DEFAULT_MODEL}")
        logger.info(f"API Key valid: {api_key is not None and len(api_key) > 10}")  # Check if API key exists
        
        # Check if API key is available
        api_key = os.environ.get("HUGGINGFACE_API_KEY")
        if not api_key:
            logger.error("No Hugging Face API key found in environment variables")
            return jsonify({"error": "API key not configured"}), 500
            
        # Generate response with explicit logging
        try:
            logger.info("Calling Hugging Face API...")
            response = generate_hf_response(
                prompt=prompt,
                model_id=model_id,
                api_key=api_key,
                max_tokens=max_tokens,
                temperature=temperature
            )
            logger.info(f"API Response received, length: {len(response)}")
            logger.info(f"API Response: {response}")
        except Exception as inner_e:
            logger.error(f"Error in generate_hf_response: {str(inner_e)}")
            raise
        
        # Return the response
        return jsonify({
            "response": response,
            "model": model_id or DEFAULT_MODEL,
            "timestamp": datetime.datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/health")
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "default_model": DEFAULT_MODEL
    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

# chat_llm_endpoint.py
import requests
import os
from typing import List, Dict, Optional

class ChatSession:
    def __init__(self, api_url: str, api_key: Optional[str] = None):
        """Initialize a chat session"""
        self.api_url = api_url
        self.api_key = api_key
        self.conversation_history = []  # Stores the entire conversation
    
    def add_message(self, role: str, content: str):
        """Add a message to the conversation history"""
        self.conversation_history.append({"role": role, "content": content})
    
    def format_prompt(self) -> str:
        """Format the conversation history as a prompt for the LLM"""
        formatted_prompt = ""
        for message in self.conversation_history:
            if message["role"] == "user":
                formatted_prompt += f"User: {message['content']}\n"
            else:  # assistant
                formatted_prompt += f"Assistant: {message['content']}\n"
        
        # Add the final assistant prompt marker
        formatted_prompt += "Assistant:"
        return formatted_prompt
    
    def send_message(self, message: str, model_id: Optional[str] = None) -> str:
        """Send a message and get a response"""
        # Add user message to history
        self.add_message("user", message)
        
        # Prepare the API request
        headers = {
            "Content-Type": "application/json"
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        # Format the entire conversation as context
        prompt = self.format_prompt()
        
        # Send request to API
        payload = {
            "prompt": prompt,
            "model_id": model_id,
            "max_tokens": 512,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/generate", 
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            result = response.json()
            
            # Extract just the assistant's response
            assistant_response = result.get("response", "").strip()
            
            # Add the assistant's response to history
            self.add_message("assistant", assistant_response)
            
            return assistant_response
            
        except Exception as e:
            print(f"Error: {e}")
            return f"Sorry, I encountered an error: {str(e)}"

# Example usage
if __name__ == "__main__":
    from utils import get_cloudrun_url
    
    # Initialize chat session
    chat = ChatSession(api_url=get_cloudrun_url())
    
    print("Chat with the AI (type 'exit' to quit)")
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit", "q"]:
            break
            
        response = chat.send_message(user_input)
        print(f"\nAI: {response}")