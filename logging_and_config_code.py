import os 
import logging
from openai import OpenAI
from dotenv import load_dotenv
from flask import Flask


# Configure logging with proper error handling
logging.basicConfig(
    level=logging.DEBUG,
    filename='app.log',
    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s'
)
logger = logging.getLogger(__name__)
load_dotenv()                                                # reads .env
# Initialize OpenAI client with error handling
try:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    client = OpenAI(api_key=api_key)
except Exception as e:
    logger.critical(f"Failed to initialize OpenAI client: {e}")
    raise

app = Flask(__name__)


if __name__ == "__main__":
    app.run(debug=True)
