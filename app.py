import os

import llama_index
from llama_index.readers.web import SimpleWebPageReader
from dotenv import load_dotenv
import logging
import sys

import chainlit as cl

from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings
from llama_index.core import set_global_handler

from etl.extractor import extract_urls_from_local, extract_urls_from_sitemap
from etl.loader import create_index


def setup():
    load_dotenv()

    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

    set_global_handler("wandb", run_args={"project": "aie-final-project-zooPalAi"})
    wandb_callback = llama_index.core.global_handler

    # from llama_index.embeddings.huggingface import HuggingFaceEmbedding
    Settings.llm = OpenAI(temperature=0.1, model="gpt-3.5-turbo")
    Settings.embed_model = OpenAIEmbedding(
        model="text-embedding-3-small")  # HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

    return wandb_callback


wandb_callback = setup()
if os.getenv('EXECUTE_INITIAL_LOAD') is not None and os.getenv('EXECUTE_INITIAL_LOAD') is True:
    full_web_urls = extract_urls_from_sitemap() if os.getenv('Env', 'local') == 'local' else extract_urls_from_local()
    urls = [url for url in full_web_urls]
    loader = SimpleWebPageReader()
    documents = loader.load_data(urls)
else:
    documents = None

index = create_index(documents, wandb_callback, os.getenv('ENV'))

query_engine = index.as_query_engine()


@cl.on_chat_start
async def start_chat():
    cl.user_session.set("wandb_callback", wandb_callback)
    cl.user_session.set("query_engine", query_engine)


@cl.on_message
async def main(message: cl.Message):
    qa_prompt_tmpl_str = f"""
        You are a helpful assistant who always speaks in a pleasant tone! Be very kind, respectful and pet friendly.
        Responds to customer queries with a step-by-step guide using context information.

        Given the context and query your duty will be find the better products for the user. 
        Add some context to the response based on the question and the products found or the zooplus website.

        If you find products for the question attach the name of the product and its http link."
        If you don't find any product for the question, please attach the link https://www.zooplus.com.
        Add some context to the response based on the question and the products found or the zooplus website.
        Be pet friendly and helpful to the user.
    Query: {message.content}
    Answer: \
    """
    Settings.callback_manager = cl.user_session.get("wandb_callback")
    query_engine = cl.user_session.get("query_engine")

    response = query_engine.query(qa_prompt_tmpl_str)

    response_message = cl.Message(content="")
    for token in response.response:
        await response_message.stream_token(token=token)

    await response_message.send()
