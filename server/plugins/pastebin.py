import json
import traceback

from server.entities.resource_types import ResourceType

# Import Celery task needed to do the real work
from tasks.tasks import pastebin_task

# Which resources are this plugin able to work with
RESOURCE_TARGET = [
    ResourceType.IPv4,
    ResourceType.DOMAIN,
    ResourceType.EMAIL,
    ResourceType.HASH,
    ResourceType.URL,
    ResourceType.USERNAME,
]

# Plugin Metadata {a description, if target is actively reached and name}
PLUGIN_DESCRIPTION = "Use Google Search API to retrieve 'pastebin.com' results"
PLUGIN_API_KEY = True
PLUGIN_IS_ACTIVE = False
PLUGIN_NAME = "pastebin"
PLUGIN_AUTOSTART = False
PLUGIN_DISABLE = False

# This is the engine for pastebin, other sites should be created in control panel (GMAIL ACCOUNT REQUIRED)
SEARCH_ENGINE = "002161999705497793957:w2bsgwyai92"


class Plugin:
    description = PLUGIN_DESCRIPTION
    is_active = PLUGIN_IS_ACTIVE
    name = PLUGIN_NAME
    api_key = PLUGIN_API_KEY
    api_doc = "https://pastebin.com/doc_scraping_api"
    autostart = PLUGIN_AUTOSTART

    def __init__(self, resource, project_id):
        self.project_id = project_id
        self.resource = resource

    def do(self):
        resource_type = self.resource.get_type()

        target = self.resource.get_data()["canonical_name"]

        # Canonical data of hashes is its short form so we have to get long hash instead
        if resource_type == ResourceType.HASH:
            target = self.resource.get_data()["hash"]

        try:
            to_task = {
                "target": target,
                "resource_id": self.resource.get_id_as_string(),
                "project_id": self.project_id,
                "resource_type": resource_type.value,
                "plugin_name": Plugin.name,
                "search_engine": SEARCH_ENGINE,
            }
            pastebin_task.delay(**to_task)

        except Exception as e:
            tb1 = traceback.TracebackException.from_exception(e)
            print("".join(tb1.format()))
