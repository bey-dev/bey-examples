import argparse
import os

import requests
from dotenv import load_dotenv

API_URL = "https://api.bey.dev/v1"


def main(api_key: str, agent_id: str) -> None:
    calls_response = requests.get(
        f"{API_URL}/calls",
        headers={"x-api-key": api_key},
    )

    if calls_response.status_code != 200:
        print(
            f"Error fetching calls: {calls_response.status_code} - {calls_response.text}"
        )
        exit(1)

    calls = calls_response.json()["data"]
    for call in calls:
        if call["agent_id"] != agent_id:
            continue

        call_id = call["id"]
        call_started_at = call["started_at"]
        call_ended_at = call["ended_at"]

        print(f"=== Call {call_id} ===")
        print(f"Started at: {call_started_at}")
        print(f"Ended at: {call_ended_at}")

        messages_response = requests.get(
            f"{API_URL}/calls/{call_id}/messages",
            headers={"x-api-key": api_key},
        )
        if messages_response.status_code != 200:
            print(
                f"Error fetching messages for call {call_id}: "
                f"{messages_response.status_code} - {messages_response.text}"
            )
            continue

        print("Messages:")
        for message in messages_response.json():
            print(f"[{message['sent_at']}] {message['sender']}:")
            print(f"{message['message']}")


if __name__ == "__main__":
    load_dotenv()
    if (api_key := os.getenv("BEY_API_KEY")) is None:
        raise ValueError("Please set the BEY_API_KEY environment variable in .env")

    parser = argparse.ArgumentParser(
        description="Fetch calls for a specific agent from the Beyond Presence API."
    )
    parser.add_argument(
        "--agent-id",
        type=str,
        help="Agent ID to fetch calls for.",
        required=True,
    )
    args = parser.parse_args()

    main(api_key=api_key, agent_id=args.agent_id)
