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

## Usage

### Deploy LLM API (Optional)

The `deploy-tgi-cloud-run` script is optional.
Use it to deploy a [Text Generation Inference](https://huggingface.co/docs/text-generation-inference) service on Google Cloud Run if you don't have an existing OpenAI-compatible LLM API endpoint:

```sh
./deploy-tgi-cloud-run
```

This will prompt you for an API key and deploy the service.
The included model is small and basic, chosen for quick deployment to demonstrate the integration flow.

Grab a coffee while it runs - deployment takes around 10 minutes.

If you already have an OpenAI-compatible LLM API endpoint, skip to the next step.

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
