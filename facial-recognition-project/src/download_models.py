import os
from transformers import pipeline

def download_models():
    # Define the cache directory
    cache_dir = 'AI'

    # Ensure the cache directory exists
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    # Load TinyBERT for sentiment analysis and emotion detection
    print("Downloading TinyBERT model...")
    tinybert = pipeline('sentiment-analysis', model='prajjwal1/bert-tiny', cache_dir=cache_dir)
    print("TinyBERT model downloaded and stored in 'AI' folder.")

    # Load GPT-Neo 125M for text generation
    print("Downloading GPT-Neo 125M model...")
    gpt_neo = pipeline('text-generation', model='EleutherAI/gpt-neo-125M', cache_dir=cache_dir)
    print("GPT-Neo 125M model downloaded and stored in 'AI' folder.")

if __name__ == "__main__":
    download_models()