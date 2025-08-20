# Beyond Presence Custom LLM Integration

Create agents using your own OpenAI-compatible LLM API with the Beyond Presence platform.

## Requirements

You'll need a [Beyond Presence](https://app.bey.chat) account and an OpenAI-compatible LLM API endpoint.
If you need to deploy your own LLM API using the included script, you'll also need [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) installed.

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

## Usage

### Deploy LLM API (Optional)

**If you already have an OpenAI-compatible LLM API endpoint, skip to the next step.**

Otherwise, use the `deploy-tgi-cloud-run` script to deploy a [Text Generation Inference](https://huggingface.co/docs/text-generation-inference) service on Google Cloud Run:

```sh
./deploy-tgi-cloud-run
```

This will prompt you for an API key and deploy the service using [Qwen/Qwen2.5-0.5B-Instruct](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct) - a small model chosen for quick deployment.
Deployment takes around 10 minutes, so grab a coffee while it runs.

To use larger models, modify `tgi-docker/Dockerfile` and consider increasing the deploy timeout in `deploy-tgi-cloud-run` as build times will be longer.

Once deployed, consider sending a `curl` request to warm up the endpoint and spin up the Cloud Run instance before testing your agent:

```sh
curl -X POST 'https://your-llm-api.com/v1/chat/completions' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json' \
  -d '{"messages":[{"role":"user","content":"Wake up!"}]}'
```

### Configure LLM API

Use `create_openai_compatible_llm_api.py` to register your LLM API with Beyond Presence:

```sh
python create_openai_compatible_llm_api.py \
  --llm-api-name 'My Custom LLM' \
  --llm-api-url 'https://your-llm-api.com/v1' \
  --llm-api-key 'your-api-key'
```

This creates an LLM API configuration and prints the configuration ID.

### Create Agent

Use `create_agent.py` to create an agent using your custom LLM:

```sh
python create_agent.py \
  --llm-api-id 'your-llm-api-id' \
  --llm-model 'your-model-name' \
  --llm-temperature '0.7'
```

This creates a new agent with your custom LLM and prints the agent ID and call link.

Note: When using Text Generation Inference, the `--llm-model` parameter is ignored as the model is configured at the TGI service level. You can pass `tgi` as dummy value.
