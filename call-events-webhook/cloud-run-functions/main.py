from datetime import datetime
from typing import Any

from flask import Request, Response

# We validate the webhook from the browser, so we need CORS headers
# In the future, we will remove this requirement
CORS_HEADER = {"Access-Control-Allow-Origin": "*"}


def webhook(request: Request) -> Response:
    # Ref: https://cloud.google.com/functions/docs/samples/functions-http-cors#functions_http_cors-python
    if request.method == "OPTIONS":
        return Response(
            status=204,
            headers=CORS_HEADER
            | {
                "Access-Control-Allow-Methods": "POST",
                "Access-Control-Allow-Headers": "Content-Type",
            },
        )

    if request.method != "POST":
        return Response(
            status=405,
            response=(
                f"Only POST requests are accepted, instead got: {request.method}"
            ),
        )

    json_body = request.get_json()

    event_type = json_body["event_type"]

    match event_type:
        case "message":
            return handle_message(json_body)
        case "call_ended":
            return handle_call_ended(json_body)
        case "test":  # sent when validating the webhook
            return Response(status=200, headers=CORS_HEADER)
        case _:
            return Response(status=400, response="Unknown event type")


def handle_message(json_body: dict[str, Any]) -> Response:
    # Ref: https://docs.bey.dev/webhooks/testing#testing-message-events
    call_id = json_body["call_id"]

    message = json_body["message"]
    sender = message["sender"]
    text = message["message"]
    sent_at = datetime.fromisoformat(message["sent_at"])

    call_data = json_body["call_data"]
    user_name = call_data["userName"]
    agent_id = call_data["agentId"]

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

    return Response(status=200, headers=CORS_HEADER)


def handle_call_ended(json_body: dict[str, Any]) -> Response:
    # Ref: https://docs.bey.dev/webhooks/testing#testing-call-ended-events
    call_id = json_body["call_id"]

    evaluation = json_body["evaluation"]
    topic = evaluation["topic"]
    user_sentiment = evaluation["user_sentiment"]
    duration_minutes = float(evaluation["duration_minutes"])
    messages_count = int(evaluation["messages_count"])

    user_name = json_body["user_name"]

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

    return Response(status=200, headers=CORS_HEADER)
