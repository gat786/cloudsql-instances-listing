import setup
import google.auth.exceptions
from googleapiclient import discovery
import json
import httplib2
import google.auth
import logging
import utils
from typing import List

http                  = httplib2.Http()
credentials, project  = google.auth.default()
logger                = logging.getLogger(__name__)

def get_instances(project_id: str):
  # Construct the service object for the interacting with the Cloud SQL Admin API.
  try:
    service = discovery.build(
      'sqladmin', 
      'v1beta4',
      credentials=credentials
    )
  except google.auth.exceptions.RefreshError as e:
    logger.exception("Credentials are expired, Please run `gcloud auth application-default login` to refresh the credentials")
    return

  req = service.instances().list(project=project_id)
  resp = req.execute()
  output_file = f"{setup.output_dir}/instances.json"
  utils.create_dir_if_not_exists(setup.output_dir)  
  with open(output_file, "w") as f:
    f.write(json.dumps(resp, indent=2))

def print_relevant_info(output_file: str = f"{setup.output_dir}/instances.json"):
  cloudsql_info = None
  with open(output_file, "r") as f:
    cloudsql_info = json.load(f)
  if cloudsql_info is None:
    logger.error("No information found")
    return

  instance_map = {}
  if "items" in cloudsql_info:
    items = cloudsql_info["items"]
    for item in items:
      instance_name   = item["name"]
      instance_tier   = item["settings"]["tier"]
      instance_region = item["region"]
      
      if instance_tier in instance_map.keys():
        instance_map[instance_tier].append(instance_name)
      else:
        instance_map[instance_tier] = [instance_name]
    for tier, instances in instance_map.items():
      logger.info(f"{tier}: {len(instances)}")
  else:
    logger.error("No items found in the root of the JSON")

if __name__ == "__main__":
  # get_instances(project_id=project)
  print_relevant_info()
