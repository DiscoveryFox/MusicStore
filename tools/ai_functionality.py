import os

import dotenv
from openai import OpenAI

dotenv.load_dotenv()


def get_song_name(filename: str):
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
            {"role": "user", "content": filename},
        ],
    )

    return completion.choices[0].message.content


def extract_instruments_from_pdf_raw_response(filepath: str) -> str:
    ...
    # Logic to extract the instrument from the file. Using the pdf2gpt or any other api for pdf's
    return "Trumpet"


def extract_instruments(filepath: str) -> str:
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Please extract the instrument based on this answer. Only return the name of the instrument. No more text.",
            },
            {"role": "user", "content": filepath},
        ],
    )
    return completion.choices[0].message.content
