import traceback

from server.entities.resource_types import ResourceType

# Import Celery task needed to do the real work
from tasks.tasks import phishtank_task

# Which resources are this plugin able to work with
RESOURCE_TARGET = [ResourceType.URL]

# Plugin Metadata {a description, if target is actively reached and name}
PLUGIN_DESCRIPTION = "Check in PhishTank if this URL is marked as a phishing"
PLUGIN_API_KEY = True
PLUGIN_IS_ACTIVE = False
PLUGIN_NAME = "phishtank"
PLUGIN_AUTOSTART = False
PLUGIN_DISABLE = False


class Plugin:
    description = PLUGIN_DESCRIPTION
    is_active = PLUGIN_IS_ACTIVE
    name = PLUGIN_NAME
    api_key = PLUGIN_API_KEY
    api_doc = "https://www.phishtank.com/api_info.php"
    autostart = PLUGIN_AUTOSTART

    def __init__(self, resource, project_id):
        self.project_id = project_id
        self.resource = resource

    def do(self):
        resource_type = self.resource.get_type()

        try:
            to_task = {
                "url": self.resource.get_data()["canonical_name"],
                "resource_id": self.resource.get_id_as_string(),
                "project_id": self.project_id,
                "resource_type": resource_type.value,
                "plugin_name": Plugin.name,
            }
            phishtank_task.delay(**to_task)

        except Exception as e:
            tb1 = traceback.TracebackException.from_exception(e)
            print("".join(tb1.format()))
