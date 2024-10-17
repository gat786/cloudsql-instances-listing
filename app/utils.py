import os
import logging

logger = logging.getLogger(__name__)

def create_dir_if_not_exists(dir_path: str):
  """
  Create a directory if it does not exist
  :param dir_path: Path to the directory
  """
  if not os.path.exists(dir_path):
    logger.debug(f"Creating directory: {dir_path}")    
    os.makedirs(dir_path) 
  else:
    logger.debug(f"Directory already exists: {dir_path}")
