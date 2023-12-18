import os

import dotenv
from openai import OpenAI

from . import pdf_extractor

dotenv.load_dotenv()


def get_song_name(filename: str):
    content: str = pdf_extractor.extract_text_from_pdf(filename, ai_ready=True)

    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Please extract only the name of the song. Answer only with the title of the song.",
            },
            {"role": "user", "content": content},
        ],
    )

    return completion.choices[0].message.content


def get_song_name_from_content(content: str):
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Please extract only the name of the song. Answer only with the title of the song.",
            },
            {"role": "user", "content": content},
        ],
    )

    return completion.choices[0].message.content


def extract_instruments_from_pdf_raw_response(filepath: str) -> str:
    ...
    # Logic to extract the instrument from the file. Using the pdf2gpt or any other api for pdf's
    return "Trumpet"


def extract_instruments(filename: str) -> str:
    content: str = pdf_extractor.extract_text_from_pdf(filename, ai_ready=True)

    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Please extract the instrument based on this answer. Only return the name of the instrument. No more text. If there are more than one instrument mentioned return 'Multiple Instruments'",
            },
            {"role": "user", "content": content},
        ],
    )
    return completion.choices[0].message.content


def extract_instruments_from_content(content: str) -> str:
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Please extract the instrument based on this answer. Only return the name of the instrument. No more text. If there are more than one instrument mentioned return 'Multiple Instruments'",
            },
            {"role": "user", "content": content},
        ],
    )
    return completion.choices[0].message.content
