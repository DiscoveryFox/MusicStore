import os
import typing

import dotenv
import requests
from openai import OpenAI

from . import pdf_extractor

dotenv.load_dotenv()


def get_song_name(filename: str):
    content: str = pdf_extractor.extract_text_from_pdf(filename, ai_ready=True)

    return get_song_name_from_content(content)


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


def extract_instruments(
    filename: str, model: str = typing.Literal["gpt-3.5-turbo", "gpt-j"]
) -> str:
    content: str = pdf_extractor.extract_text_from_pdf(filename, ai_ready=True)

    return extract_instruments_from_content(content, model)


def extract_instruments_from_content(
    content: str, model: str = typing.Literal["gpt-3.5-turbo", "gpt-j"]
) -> str:
    match str(model).lower():
        case "gpt-3.5-turbo":
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
        case "gpt-j":
            file_content = content
            context = f"Please extract the instrument based on this answer. Only return the name of the instrument. No more text. If there are more than one instrument mentioned return 'Multiple Instruments'. This is the file: {file_content}"
            payload = {
                "context": context,
                "token_max_length": 4096,
                "temperature": 1.0,
                "top_p": 0.9,
            }

            print("Sending request")
            response = requests.post(
                "http://api.vicgalle.net:5000/docs#/default/generate_generate_post",
                params=payload,
            ).json()
            print("Request send")
            print(response)
            return response
