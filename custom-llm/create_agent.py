import argparse
import os

import requests
from dotenv import load_dotenv

BEY_API_URL = "https://api.bey.dev/v1"


def main(
    bey_api_key: str,
    llm_api_id: str,
    llm_model: str,
    llm_temperature: float,
) -> None:
    llm_api_response = requests.get(
        f"{BEY_API_URL}/external-api/{llm_api_id}",
        headers={"x-api-key": bey_api_key},
    )

    if llm_api_response.status_code != 200:
        print(
            "Error retrieving LLM API Configuration: "
            f"{llm_api_response.status_code} - {llm_api_response.text}"
        )
        exit(1)

    llm_api_data = llm_api_response.json()
    llm_api_name = llm_api_data["name"]
    llm_api_id = llm_api_data["id"]

    agent_response = requests.post(
        f"{BEY_API_URL}/agent",
        headers={"x-api-key": bey_api_key},
        json={
            "name": f"Demo Agent for Custom LLM {llm_api_name}",
            "avatar_id": "b5bebaf9-ae80-4e43-b97f-4506136ed926",  # Nelly from https://docs.bey.dev/avatars/default
            "system_prompt": "You are a helpful assistant.",
            "greeting": "Hello! How can I help you today?",
            "llm": {
                "type": "openai_compatible",
                "api_id": llm_api_id,
                "model": llm_model,
                "temperature": llm_temperature,
            },
        },
    )

    agent_data = agent_response.json()
    agent_name = agent_data["name"]
    agent_id = agent_data["id"]

    print("Created agent!")
    print(f"Name: {agent_name}")
    print(f"ID: {agent_id}")
    print(f"Call link: https://bey.chat/{agent_id}")


if __name__ == "__main__":
    load_dotenv()
    if (bey_api_key := os.getenv("BEY_API_KEY")) is None:
        raise ValueError("Please set the BEY_API_KEY environment variable in .env")

    parser = argparse.ArgumentParser(description="Create an agent using a custom LLM.")
    parser.add_argument(
        "--llm-api-id",
        type=str,
        help="The ID of the external LLM API configuration to use.",
        required=True,
    )
    parser.add_argument(
        "--llm-model",
        type=str,
        help="The LLM to use for the agent.",
        required=True,
    )
    parser.add_argument(
        "--llm-temperature",
        type=str,
        help="The temperature for the LLM model.",
        required=True,
    )
    args = parser.parse_args()

    main(
        bey_api_key=bey_api_key,
        llm_api_id=args.llm_api_id,
        llm_model=args.llm_model,
        llm_temperature=args.llm_temperature,
    )
