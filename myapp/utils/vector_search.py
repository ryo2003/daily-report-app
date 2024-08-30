import openai
import os
import sys
from dotenv import load_dotenv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '/app/utils/')))

load_dotenv()
OPENAI_API = os.getenv("API_KEY")

# Set up the OpenAI API configuration
openai.api_key = OPENAI_API

def create_embedding(contents, purpose):
    # Create an embedding using the OpenAI API
    text = contents + purpose
    response = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=text
    )
    
    # Extract the embedding from the response
    embedding = response['data'][0]['embedding']

    print('embedding', embedding)

    return embedding

# Example usage
text_input = "This is an example text"
embedding = create_embedding(text_input)
