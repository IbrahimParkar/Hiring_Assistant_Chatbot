import requests
import re
from dotenv import load_dotenv
import os
from prompt import *
import json
from datetime import datetime


load_dotenv()
HF_API_KEY = os.getenv("HF_KEY")
API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}


def save_interview_to_file(data, folder="Profiles"):
    if not os.path.exists(folder):
        os.makedirs(folder)

    filename = f"{folder}/{data['Name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print(f"Interview saved to {filename}")


# Validation Helpers
def is_valid_email(email):
    pattern = r"^(?!.*\.\.)[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def is_valid_contact_number(number):
    pattern = r"^\+?\d{10,15}$"
    return bool(re.match(pattern, number))


# Text Cleaning
# Function to clean input
def clean_input(user_input):
    return ", ".join([line.strip() for line in user_input.splitlines() if line.strip()])


# Function to clean user's response (removes line spaces)
def clean_response(user_response):
    return re.sub(r"\s+", " ", user_response.strip())


# Extract only the first 3 lines of the response for relevance check
def get_first_n_lines(text, n=2):
    lines = text.strip().splitlines()
    return "\n".join(lines[:n]) if lines else text.strip()


# Hugging Face API Calls
def query(payload):
    try:
        print("API Request Payload:", payload)  # Debugging print
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        result = response.json()
        print("Raw API Response:", result)  # Debugging print

        if isinstance(result, list) and result and 'generated_text' in result[0]:
            generated_text = result[0]['generated_text'].strip()
            print("Extracted Generated Text:", generated_text)  # Debugging print

            # Extract the actual question after the last newline
            extracted_question = generated_text.split("\n")[-1].strip()
            print("Final Extracted Question:", extracted_question)  # Debugging print

            return extracted_question if extracted_question else "Error: No valid question generated."
        else:
            return "Error: Unexpected API response format."
    except requests.exceptions.RequestException as e:
        print(f"API Request Error: {e}")
        return f"API Error: {e}"


# Function to summarize user's response
def summarize_text(text):
    summarizer_api = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}

    try:
        response = requests.post(summarizer_api, headers=headers, json={"inputs": text})
        response.raise_for_status()
        result = response.json()
        summary = result[0]["summary_text"].strip()
        print("Summary:", summary)  # Debug
        return summary
    except Exception as e:
        print(f"Summarization error: {e}")
        return text  # fallback


# Relevance Check Helpers
def extract_verdict_only(full_response, prompt_text):
    # Remove the prompt from the full response
    response_only = full_response.replace(prompt_text, "").strip()

    # Go through each line from the bottom up
    for line in reversed(response_only.splitlines()):
        verdict = line.strip().lower()

        # Clean verdict to just 'yes' or 'no' if it includes extra stuff
        if "yes" or "is relevant" in verdict:
            return "yes"
        elif "no" or "is not relevant" in verdict:
            return "no"

    return "invalid"


# Function to check if the response is relevant to the question (Fallback Mechanism)
def is_response_relevant(question, answer):
    relevance_prompt = response_relevance_prompt(question, answer)
    response_text = query({"inputs": relevance_prompt})
    print("Raw Response:", response_text)  # for debugging
    verdict = extract_verdict_only(response_text,relevance_prompt)
    return verdict == "yes"


# Generic field relevance check
def is_field_relevant(field_name, value):
    prompt1 = field_relevance_prompt(field_name, value)
    response = query({"inputs": prompt1})
    verdict = extract_verdict_only(response,prompt1)
    return verdict == "yes"
