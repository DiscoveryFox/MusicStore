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
