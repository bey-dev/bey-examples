import argparse
import os
from typing import Optional

import requests
from dotenv import load_dotenv

SYSTEM_PROMPT_TEMPLATE = """\
You are an interviewer for candidates applyine to a role.
You ask three relevant questions and then end the conversation.

This is the role to interview for: {role_name}
Role description: {role_description}
The name of the candidate is: {candidate_name}
"""

EGE_STOCK_AVATAR_ID = "b9be11b8-89fb-4227-8f86-4a881393cbdb"
API_URL = "https://api.bey.dev/v1"


def main(
    api_key: str,
    role_name: str,
    role_description: str,
    candidate_name: str,
    avatar_id: Optional[str],
) -> None:
    response = requests.post(
        f"{API_URL}/agent",
        headers={"x-api-key": api_key},
        json={
            "name": f"{role_name} Interviewer for {candidate_name}",
            "system_prompt": SYSTEM_PROMPT_TEMPLATE.format(
                role_name=role_name,
                role_description=role_description,
                candidate_name=candidate_name,
            ),
            "greeting": (
                f"Hello {candidate_name}, how are you doing? "
                "Are you ready for the interview?"
            ),
            "avatar_id": avatar_id if avatar_id is not None else EGE_STOCK_AVATAR_ID,
            # ---
            # Uncomment the following lines to customize the avatar further
            # "language": "es",
            # "max_session_length_minutes": 10,
            # "capabilities": ["webcam_vision"],
        },
    )

    if response.status_code != 201:
        print(f"Error creating agent: {response.status_code} - {response.text}")
        exit(1)

    agent_data = response.json()
    agent_name = agent_data["name"]
    agent_id = agent_data["id"]

    print(f"Created agent '{agent_name}' with ID: {agent_id}")
    print(f"Link to agent call: https://bey.chat/{agent_id}")


if __name__ == "__main__":
    load_dotenv()
    if (api_key := os.getenv("BEY_API_KEY")) is None:
        raise ValueError("Please set the BEY_API_KEY environment variable in .env")

    parser = argparse.ArgumentParser(
        description="Create a end-to-end Bey avatar agent for interviews."
    )
    parser.add_argument(
        "--role-name",
        type=str,
        help="Name the role to interview for.",
        required=True,
    )
    parser.add_argument(
        "--role-description",
        type=str,
        help="Description of the role to interview for.",
        required=True,
    )
    parser.add_argument(
        "--candidate-name",
        type=str,
        help="Name of the candidate to interview.",
        required=True,
    )
    parser.add_argument(
        "--avatar-id", type=str, help="Avatar ID to use.", default=EGE_STOCK_AVATAR_ID
    )
    args = parser.parse_args()

    main(
        api_key=api_key,
        role_name=args.role_name,
        role_description=args.role_description,
        candidate_name=args.candidate_name,
        avatar_id=args.avatar_id,
    )
