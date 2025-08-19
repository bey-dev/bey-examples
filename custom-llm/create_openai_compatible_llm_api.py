import argparse
import os

import requests
from dotenv import load_dotenv

BEY_API_URL = "https://api.bey.dev/v1"


def main(
    bey_api_key: str,
    llm_api_name: str,
    llm_api_key: str,
    llm_api_url: str,
) -> None:
    response = requests.post(
        f"{BEY_API_URL}/external-api",
        headers={"x-api-key": bey_api_key},
        json={
            "name": llm_api_name,
            "type": "openai_compatible_llm",
            "url": llm_api_url,
            "api_key": llm_api_key,
        },
    )

    if response.status_code != 201:
        print(
            f"Error creating LLM API Configuration: {response.status_code} - {response.text}"
        )
        exit(1)

    llm_api_data = response.json()
    llm_api_name = llm_api_data["name"]
    llm_api_id = llm_api_data["id"]

    print("Created LLM API Configuration!")
    print(f"Name: {llm_api_name}")
    print(f"ID: {llm_api_id}")


if __name__ == "__main__":
    load_dotenv()
    if (bey_api_key := os.getenv("BEY_API_KEY")) is None:
        raise ValueError("Please set the BEY_API_KEY environment variable in .env")

    parser = argparse.ArgumentParser(
        description="Create external API configuration for your Text Generation Inference."
    )
    parser.add_argument(
        "--llm-api-name",
        type=str,
        help="Name of the LLM API.",
        required=True,
    )
    parser.add_argument(
        "--llm-api-url",
        type=str,
        help="URL of the LLM API.",
        required=True,
    )
    parser.add_argument(
        "--llm-api-key",
        type=str,
        help="API key for the LLM API.",
        required=True,
    )
    args = parser.parse_args()

    main(
        bey_api_key=bey_api_key,
        llm_api_name=args.llm_api_name,
        llm_api_key=args.llm_api_key,
        llm_api_url=args.llm_api_url,
    )
