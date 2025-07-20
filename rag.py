import time
import os
import re
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv() 

def get_answer_from_rag(question: str) -> str:
    start = time.time()

    endpoint = os.getenv("AZURE_INFERENCE_SDK_ENDPOINT")
    deployment_name = "DeepSeek-R1"

    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=DefaultAzureCredential(),
        credential_scopes=["https://cognitiveservices.azure.com/.default"]
    )

    print(f"[TIMER] Azure client ready in {time.time() - start:.2f} sec")

    t_llm = time.time()
    response = client.complete(
        messages=[
            SystemMessage(content="You are a helpful assistant."),
            UserMessage(content=question)
        ],
        max_tokens=2048,
        model=deployment_name,
    )
    print(f"[TIMER] Azure LLM response in {time.time() - t_llm:.2f} sec")

    raw_answer = response.choices[0].message.content
    cleaned_answer = re.sub(r'<think>.*?</think>', '', raw_answer, flags=re.DOTALL)

    print(f"[TIMER] Total RAG time: {time.time() - start:.2f} sec")
    return cleaned_answer.strip()
