import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from google.cloud import storage
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from pathlib import Path
from dotenv import load_dotenv
import tempfile

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
BUCKET_NAME = os.getenv("BUCKET_NAME")

DB_FAISS_PATH = Path("vectorstores", "db_faiss")
DATA_FOLDER = "data"

def download_from_gcs(bucket_name, data_folder, local_dir):
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    blobs = bucket.list_blobs(prefix=data_folder)
    for blob in blobs:
        if blob.name.endswith('.pdf'):
            local_path = os.path.join(local_dir, os.path.basename(blob.name))
            blob.download_to_filename(local_path)
            print(f"Downloaded {blob.name} to {local_path}")

def upload_to_gcs(bucket_name, source_folder):
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    for root, _, files in os.walk(source_folder):
        for file in files:
            file_path = os.path.join(root, file)
            blob = bucket.blob(file_path)
            blob.upload_from_filename(file_path)
            print(f"Uploaded {file_path} to {bucket_name}")

#create vector database
def create_vector_db(data_path):

    # Load the data
    loader = DirectoryLoader(data_path, glob='*.pdf', loader_cls=PyPDFLoader)
    documents = loader.load()
    # Split the data
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = splitter.split_documents(documents)
    # Load the embeddings
    embeddings = OpenAIEmbeddings()
    # Create the vector store
    vectorstore = FAISS.from_documents(texts, embeddings)
    # Ingest the data
    vectorstore.save_local(DB_FAISS_PATH)

if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as temp_dir:
        # download the data from the GCS bucket
        download_from_gcs(BUCKET_NAME, DATA_FOLDER, temp_dir)

        # load the data from the GCS bucket and create the vector database
        create_vector_db(temp_dir)