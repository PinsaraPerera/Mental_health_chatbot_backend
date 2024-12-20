from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_community.llms import CTransformers

from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationBufferMemory
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from pathlib import Path

from langchain_core.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    PromptTemplate,
    ChatPromptTemplate,
)
from langchain.callbacks.base import BaseCallbackHandler
import logging
from typing import Any, Dict, List


# Configure logging
logging.basicConfig(level=logging.INFO)
_log = logging.getLogger(__name__)

# Add file handler
file_handler = logging.FileHandler("app.log")
file_handler.setLevel(logging.INFO)

# Create a logging format
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

# Add the handlers to the logger
_log.addHandler(file_handler)

DB_FAISS_PATH = Path("vectorstores", "db_faiss")
embeddings = OpenAIEmbeddings()
db = FAISS.load_local(DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)

system_template = """
You are a psychological counselor. As a counselor, you are expected to provide empathetic, informative, and responsible responses to patients.
Your role is to offer general guidance on coping strategies and resources, and to encourage seeking professional help when necessary. 
Avoid diagnosing or providing specific medical advice.

Context : 
{context}

Respond to the user without any formatting.
Use the above information as a reference to offer the best possible advice to the user.
Do not include chat history, question, or context in your response. Only provide the counselor's response, referring to past conversations for context.
"""

human_template = """
chat history : 
{chat_history}

question :
{question}
"""


def set_custom_prompt():
    """
    Prompt template for QA retrieval for each vectorstore
    """

    system_message_template = SystemMessagePromptTemplate.from_template(system_template)
    human_message_template = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_template, human_message_template]
    )

    return chat_prompt


def load_llm():
    llm = ChatOpenAI(model="gpt-3.5-turbo", verbose=True)
    return llm


def get_context_from_vector_db(query):

    docs_with_scores = db.similarity_search_with_score(query, k=4)

    # Sort results by score (lower is better) and select top 2
    docs_with_scores.sort(key=lambda x: x[1])
    top_results = docs_with_scores[:2]

    if top_results:
        context = "\n".join(
            [result[0].page_content.replace("\n", " ") for result in top_results]
        )
        return context
    return ""


def debuggingLLM(data: dict):
    print("========debugging start==========\n\n")
    print(f"chat history: {data['chat_history']}\n\n")
    print(f"context: {data['context']}\n\n")
    print(f"question: {data['question']}\n\n")
    print(f"response: {data['response']}\n\n")


def llm_chain(llm, prompt):
    llm_chain = prompt | llm | StrOutputParser()
    return llm_chain


def qa_bot(prompt):
    llm = load_llm()
    chain = llm_chain(llm, prompt)
    return chain


class CustomHandler(BaseCallbackHandler):
    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> Any:
        formatted_prompts = "\n".join(prompts)
        _log.info(f"Prompt:\n{formatted_prompts}")


def final_result(query, chat_history):
    context = get_context_from_vector_db(query)
    prompt = set_custom_prompt()
    chain = qa_bot(prompt)
    input_data = {"chat_history": chat_history, "question": query, "context": context}

    # setup custom callback
    chain_response = chain.invoke(input_data, config={"callbacks": [CustomHandler()]})

    # debuggingLLM({"chat_history": chat_history, "question": query, "context": context, "response": chain_response})
    return chain_response
