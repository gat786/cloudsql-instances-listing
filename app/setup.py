import logging
import dotenv
import os

dotenv.load_dotenv()
logging.basicConfig(
  level=logging.DEBUG
)

output_dir = os.getenv("OUTPUT_DIR", "outputs")
