"""
Constants for HuggingFace models, organized by size and capabilities
"""

# Small models (< 7B parameters)
SMALL_MODELS = {
    "MISTRAL_7B": {
        "id": "mistralai/Mistral-7B-Instruct-v0.2",
        "parameters": "7B",
        "context_window": 8192,
        "description": "Efficient 7B model with strong performance",
    },
    "PHI_2": {
        "id": "microsoft/phi-2",
        "parameters": "2.7B",
        "context_window": 2048,
        "description": "Small but powerful 2.7B model from Microsoft",
    },
    "GEMMA_2B": {
        "id": "google/gemma-2b-it",
        "parameters": "2B",
        "context_window": 8192,
        "description": "Google's 2B instruction-tuned model",
    },
}

# Medium models (7-30B parameters)
MEDIUM_MODELS = {
    "LLAMA2_13B": {
        "id": "meta-llama/Llama-2-13b-chat-hf",
        "parameters": "13B",
        "context_window": 4096,
        "description": "Meta's 13B chat model with good performance",
        "requires_approval": True,
    },
    "DEEPSEEK_CODER_INSTRUCT_7B": {
        "id": "deepseek-ai/deepseek-coder-7b-instruct-v1.5",
        "parameters": "7B",
        "context_window": 16384,
        "description": "Specialized coding model with long context window",
    },
    "MIXTRAL_8x7B": {
        "id": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "parameters": "46.7B (MoE)",
        "context_window": 32768,
        "description": "Mixture of Experts model with 8 experts of 7B each",
    },
}

# Large models (>30B parameters)
LARGE_MODELS = {
    "LLAMA2_70B": {
        "id": "meta-llama/Llama-2-70b-chat-hf",
        "parameters": "70B",
        "context_window": 4096,
        "description": "Meta's largest chat model with strong performance",
        "requires_approval": True,
    },
    "DEEPSEEK_67B": {
        "id": "deepseek-ai/deepseek-llm-67b-chat",
        "parameters": "67B",
        "context_window": 4096,
        "description": "Large chat model from DeepSeek",
        "requires_approval": True,
    },
}

# Usage and pricing information
USAGE_INFO = """
HuggingFace Inference API Pricing:

Free Tier:
- Limited to 30K input tokens per month (~100-150 queries)
- Rate limited to ~1 request per minute
- Some models require special approval (Llama-2, etc.)

Starter Plan ($9/month):
- 1.5M tokens per month
- Higher rate limits
- Priority access

Details may change - check the official pricing at:
https://huggingface.co/pricing
"""