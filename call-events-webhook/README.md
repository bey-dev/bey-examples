# Beyond Presence Call Events Webhook

Receive and process call events with Beyond Presence webhooks and Google Cloud Run functions.

## Requirements

You'll need a [Beyond Presence](https://app.bey.chat) account and [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) installed.

## Setup

### Deploy the Webhook

Deploy the webhook to Google Cloud Functions:

```sh
gcloud functions deploy call-events-webhook \
  --runtime 'python310' \
  --source 'cloud-run-functions' \
  --entry-point 'webhook' \
  --trigger-http \
  --allow-unauthenticated
```

After deployment, copy the trigger URL from the output and [configure it as your webhook endpoint](https://docs.bey.dev/webhooks/overview#introduction) in your Beyond Presence dashboard.

## Event Handling

The webhook processes three types of events:
- **Message**: triggered when messages are sent during calls
- **Call ended**: triggered when call sessions end with evaluation data
- **Test**: used for webhook validation during setup

## Usage

Once deployed and configured, the webhook automatically receives events from Beyond Presence calls managed by your agents.
Event data is logged to [Cloud Functions logs](https://cloud.google.com/run/docs/monitoring-overview).

Customize the event handlers in `main.py` to store data, send notifications, or trigger other processes.

## Documentation

- [Beyond Presence Webhooks](https://docs.bey.dev/webhooks)
- [Cloud Run Functions](https://cloud.google.com/functions)
