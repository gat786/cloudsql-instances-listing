import google.auth.exceptions
from googleapiclient import discovery
import json
import httplib2
import google.auth
import logging

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
  with open("instances.json", "w") as f:
    f.write(json.dumps(resp, indent=2))

if __name__ == "__main__":
  get_instances(project_id=project)
