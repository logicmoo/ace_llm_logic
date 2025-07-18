
FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y git build-essential
COPY . /app
RUN pip install .
ENV OPENAI_API_KEY=replace-me-or-set-at-runtime
CMD ["python", "-m", "ace_llm_logic"]
