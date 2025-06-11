from datetime import datetime
from typing import Any

from flask import Request, Response


def webhook(request: Request) -> Response:
    if request.method not in {"POST", "OPTIONS"}:
        return Response(
            status=405,
            response=f"Only POST requests are accepted, instead got: {request.method}",
        )

    # We validate the webhook from the browser, so we need CORS headers
    # In the future, we will remove this requirement
    # Ref: https://cloud.google.com/functions/docs/samples/functions-http-cors#functions_http_cors-python
    if request.method == "OPTIONS":
        return Response(
            status=204,
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST",
                "Access-Control-Allow-Headers": "Content-Type",
            },
        )

    json_body = request.get_json()

    event_type = json_body["event_type"]

    match event_type:
        case "test":  # sent when validating the webhook
            return Response(
                status=200,
                headers={"Access-Control-Allow-Origin": "*"},
            )
        case "message":
            return handle_message(json_body)
        case "call_ended":
            return handle_call_ended(json_body)
        case _:
            return Response(status=400, response=f"Unknown event type: {event_type}")


def handle_message(json_body: dict[str, Any]) -> Response:
    # For the most current JSON schema, visit:
    # https://docs.bey.dev/webhooks/overview#message-events
    call_id: str = json_body["call_id"]

    message: str = json_body["message"]
    sender: str = message["sender"]
    text: str = message["message"]
    sent_at = datetime.fromisoformat(message["sent_at"])

    call_data: dict[str, Any] = json_body["call_data"]
    user_name: str = call_data["userName"]
    agent_id: str = call_data["agentId"]

    print(
        f"Message received - "
        f"Call ID: {call_id}, "
        f"Sender: {sender}, "
        f"Text: {text}, "
        f"Sent At: {sent_at}, "
        f"User Name: {user_name}, "
        f"Agent ID: {agent_id}"
    )

    # do something with the message, e.g. process and store it

    return Response(status=200)


def handle_call_ended(json_body: dict[str, Any]) -> Response:
    # For the most current JSON schema, visit:
    # https://docs.bey.dev/webhooks/overview#call-ended-events
    call_id: str = json_body["call_id"]

    evaluation: dict[str, Any] = json_body["evaluation"]
    topic: str = evaluation["topic"]
    user_sentiment: str = evaluation["user_sentiment"]
    duration_minutes: float = evaluation["duration_minutes"]
    messages_count: int = evaluation["messages_count"]

    user_name: str = json_body["user_name"]

    print(
        "Call ended - "
        f"Call ID: {call_id}, "
        f"Topic: {topic}, "
        f"User Sentiment: {user_sentiment}, "
        f"Duration (minutes): {duration_minutes}, "
        f"Messages Count: {messages_count}, "
        f"User Name: {user_name}"
    )

    # do something with the call ended data, e.g. notify someone

    messages = json_body["messages"]
    for message in messages:
        sender = message["sender"]
        text = message["message"]
        sent_at = datetime.fromisoformat(message["sent_at"])

        print(
            f"Message from ended call {call_id} - "
            f"Sender: {sender}, "
            f"Text: {text}, "
            f"Sent At: {sent_at}"
        )

    return Response(status=200)
