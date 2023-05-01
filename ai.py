# load api key from .env file
import os
import openai
import pandas as pd
from pdf_writer import text_to_pdf
from typing import List, Optional
from dotenv import load_dotenv



load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_prompt(prompt: str) -> str:
    """Generate a prompt using the OpenAI API

    Parameters
    ----------
    prompt : str
    """
    # Capitalize the prompt
    return prompt.capitalize()


def get_gpt_text_completion(prompt: str, max_tokens: int = 100) -> str:
    """Get a response from the GPT-3 API

    Parameters
    ----------
        prompt : str

    Returns
    -------
        response : str
    """
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=generate_prompt(prompt),
        max_tokens=max_tokens,
        temperature=0.6
    )
    return response["choices"][0]["text"]


def get_gpt_chat_completion(messages: List[dict]) -> Optional[str]:
    """Get a response from the GPT-3 API

    Parameters
    ----------
        messages : List[dict]
            The messages to send to the API

    Returns
    -------
        Optional[str]
            The response from the API
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages)
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def generate_metadata(df: pd.DataFrame) -> str:
    """Generate metadata for the data

    Parameters
    ----------
        df : pd.DataFrame
            The data to generate metadata for
    """
    

if __name__ == "__main__":
    # Example usage
    # 1 - Analysis: What type of analysis can I perform for this data?
    # 2 - Visualization: What type of visualization can I perform for this data?
    # 3 - Prediction: What type of prediction can I perform for this data?
    # 4 - Classification: What type of classification can I perform for this data?
    df = pd.read_parquet("transactions.parquet")

    content = f"Give basics statistics for this data: {df}"
    messages = [
        {"role": "user", "content": f"{content}"},

    ]
    response = get_gpt_chat_completion(messages)
    output_file = "output.pdf"
    section_title = "Statistics"
    text_to_pdf(response, output_file, section_title, is_append=True)
