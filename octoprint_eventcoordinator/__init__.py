# coding=utf-8

import octoprint.plugin
import octoprint.events


class EventcoordinatorPlugin(octoprint.plugin.SettingsPlugin,
    octoprint.plugin.AssetPlugin,
    octoprint.plugin.TemplatePlugin
):

    ##~~ SettingsPlugin mixin

    def on_settings_load(self):
        my_settings = {"availableEvents": octoprint.events.all_events(), "subscriptions": []}
        events = self._settings.global_get(["events"])
        if events:
            my_settings["subscriptions"] = events["subscriptions"]
        return my_settings

    def on_settings_save(self, data):
        self._settings.global_set(["events", "subscriptions"], data.get("subscriptions", []))

    ##~~ AssetPlugin mixin

    def get_assets(self):
        return {
            "js": ["js/eventcoordinator.js"]
        }

    ##~~ Softwareupdate hook

    def get_update_information(self):
        return {
            "eventcoordinator": {
                "displayName": "Event Coordinator",
                "displayVersion": self._plugin_version,

                # version check: github repository
                "type": "github_release",
                "user": "jneilliii",
                "repo": "OctoPrint-EventCoordinator",
                "current": self._plugin_version,

                # update method: pip
                "pip": "https://github.com/jneilliii/OctoPrint-EventCoordinator/archive/{target_version}.zip",
            }
        }


__plugin_name__ = "Event Coordinator"
__plugin_pythoncompat__ = ">=3,<4" # only python 3

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = EventcoordinatorPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
