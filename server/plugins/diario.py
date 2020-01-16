import traceback

from server.entities.resource_types import ResourceType

# Import Celery task needed to do the real work
from tasks.tasks import diario_task

# Which resources are this plugin able to work with
RESOURCE_TARGET = [ResourceType.HASH]

# Plugin Metadata {a description, if target is actively reached and name}
PLUGIN_DESCRIPTION = "Scans and analyzes pdf and office documents in a static way keeping users content private"
PLUGIN_API_KEY = True
PLUGIN_IS_ACTIVE = False
PLUGIN_NAME = "diario"
PLUGIN_AUTOSTART = False
PLUGIN_DISABLE = False


class Plugin:
    description = PLUGIN_DESCRIPTION
    is_active = PLUGIN_IS_ACTIVE
    name = PLUGIN_NAME
    api_key = PLUGIN_API_KEY
    api_doc = "https://diario.e-paths.com"
    autostart = PLUGIN_AUTOSTART

    def __init__(self, resource, project_id):
        self.project_id = project_id
        self.resource = resource

    def do(self):
        resource_type = self.resource.get_type()

        try:
            to_task = {
                "hash": self.resource.get_data()["hash"],
                "resource_id": self.resource.get_id_as_string(),
                "project_id": self.project_id,
                "resource_type": resource_type.value,
                "plugin_name": Plugin.name,
            }
            diario_task.delay(**to_task)

        except Exception as e:
            tb1 = traceback.TracebackException.from_exception(e)
            print("".join(tb1.format()))
