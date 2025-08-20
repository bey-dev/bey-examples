FROM ghcr.io/huggingface/text-generation-inference:3.2.3

# Small model to speed up downloads for this example
ENV MODEL_ID Qwen/Qwen2.5-0.5B-Instruct

# Maintain consistent HF model cache location between build and runtime
ENV HUGGINGFACE_HUB_CACHE /data

# Pre-download model during build for faster deployment.
# Trade longer build time for significantly faster startup and serving.
# See: https://cloud.google.com/run/docs/configuring/services/gpu-best-practices#loading-storing-models-tradeoff
#
# Note: `text-generation-server download-weights` is also a thing.
# Ref: https://huggingface.co/docs/text-generation-inference/en/basic_tutorials/using_cli#using-tgi-cli
# But it does not download required files like tokenizer.
# Since we want to avoid HF rate limiting problems at runtime, we download the
# entire repo with a custom script instead.
COPY download_repo .
RUN ./download_repo

# Now that everything is downloaded, we can set HF hub to offline mode
# Ref: https://huggingface.co/docs/huggingface_hub/en/package_reference/environment_variables#hfhuboffline
ENV HF_HUB_OFFLINE 1

# PORT injected by Cloud Run matches HF TGI's expected variable
# Ref: https://cloud.google.com/run/docs/configuring/services/environment-variables#reserved
# Ref: https://huggingface.co/docs/text-generation-inference/main/en/reference/launcher#port
