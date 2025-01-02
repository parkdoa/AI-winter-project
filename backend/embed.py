import os
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from langchain_upstage import UpstageDocumentParseLoader, UpstageEmbeddings
from pinecone import Pinecone, ServerlessSpec

# Load environment variables
load_dotenv()

# Initialize Upstage embeddings
embedding_upstage = UpstageEmbeddings(model="embedding-query")

# Get Pinecone API key from environment variables
pinecone_api_key = os.environ.get("PINECONE_API_KEY")
pc = Pinecone(api_key=pinecone_api_key)

# Define index name and document path
index_name = "economy-words"
pdf_path = "econony_words_700page_2020.pdf"

# Create new index if not exists
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=4096,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )

# Load and parse the document
document_parse_loader = UpstageDocumentParseLoader(
    pdf_path,
    output_format='html',  # Specify output format
    coordinates=False       # Do not include OCR coordinates
)

docs = document_parse_loader.load()

# Split the document into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,  # Define chunk size
    chunk_overlap=100 # Define overlap
)

splits = text_splitter.split_documents(docs)

# Embed the chunks into Pinecone vector store
PineconeVectorStore.from_documents(
    splits, embedding_upstage, index_name=index_name
)

print("end")
