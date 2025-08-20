# Beyond Presence End-to-End Agent

Create end-to-end agents and retrieve call data using the Beyond Presence API.

## Requirements

You'll need a [Beyond Presence](https://app.bey.chat) account.

## Setup

### Environment

Copy `.env.template` to `.env`, then add your Beyond Presence API key.
See the [Beyond Presence docs](https://docs.bey.dev/api-key#creating-and-managing-api-keys) for instructions on generating and managing keys.

### Install

Requires Python 3.8 or higher. Install dependencies with:

```sh
pip install -r requirements.txt
```

Note: While this example use Python, the integration is simply HTTP calls to our API and can be implemented in any language or framework (curl, TypeScript, etc.).

### Usage

### Create an Agent

Use `create.py` to generate an interview agent for a specific role and candidate:

```sh
python create.py \
  --role-name 'Data Scientist' \
  --role-description 'Responsible for analyzing data to extract insights.' \
  --candidate-name 'Alice'
```

This creates a new agent with a custom interview prompt, then prints the agent ID and a call link.
To embed the agent in your product, see the [Beyond Presence docs](https://docs.bey.dev/integration/end-to-end#embed-your-agent).

You can optionally pass a custom `--avatar-id`.

### Fetch Agent Calls

Use `fetch_calls.py` to retrieve calls and transcripts for a given agent:

```sh
python fetch_calls.py --agent-id YOUR_AGENT_ID
```

This prints the transcript for each call.

To process agent events as they are generated, implement a webhook.
See the [webhook example](../call-events-webhook) for reference.

## Documentation

- [Beyond Presence End-to-End Integration](https://docs.bey.dev/integration/end-to-end)
- [Beyond Presence API Reference](https://docs.bey.dev/api-reference)
