import mysql.connector
from typing import Optional, List
from .resource import Resource
from mapadroid.utils.logging import get_logger, LoggerEnums


logger = get_logger(LoggerEnums.data_manager)


class Webhook(Resource):
    table = 'settings_webhook'
    name_field = 'url'
    primary_key = 'webhook_id'
    search_field = 'url'
    configuration = {
        "fields": {
            "url": {
                "settings": {
                    "type": "text",
                    "require": True,
                    "description": "Webhook url. Must start with http / https",
                    "expected": str
                }
            },
            "active": {
                "settings": {
                    "type": "option",
                    "values": [True, False],
                    "empty": True,
                    "require": False,
                    "description": "Activate / deactivate sending data to this url",
                    "expected": bool
                }
            },
            "mon": {
                "settings": {
                    "type": "option",
                    "values": [True, False],
                    "empty": True,
                    "require": False,
                    "description": "Send mons to webhook receiver",
                    "expected": bool
                }
            },
            "raid": {
                "settings": {
                    "type": "option",
                    "values": [True, False],
                    "empty": True,
                    "require": False,
                    "description": "Send raids to webhook receiver",
                    "expected": bool
                }
            },
            "gym": {
                "settings": {
                    "type": "option",
                    "values": [True, False],
                    "empty": True,
                    "require": False,
                    "description": "Send gyms to webhook receiver",
                    "expected": bool
                }
            },
            "quest": {
                "settings": {
                    "type": "option",
                    "values": [True, False],
                    "empty": True,
                    "require": False,
                    "description": "Send quests to webhok receiver",
                    "expected": bool
                }
            },
            "weather": {
                "settings": {
                    "type": "option",
                    "values": [True, False],
                    "empty": True,
                    "require": False,
                    "description": "Send weather to webhook receiver",
                    "expected": bool
                }
            },
            "webhookgeofences": {
                "settings": {
                    "type": "list",
                    "require": False,
                    "empty": [],
                    "description": "List of webhook geofences that include or exclude data (default: empty List)",
                    "expected": list,
                    "data_source": "webhookgeofence",
                    "uri_source": "api_webhookgeofence"
                }
            }
        }
    }

    def _load(self) -> None:
        super()._load()
        query = "SELECT `webhookgeofence_id` " \
                "FROM `settings_webhook_to_webhookgeofence` " \
                "WHERE `webhook_id` = %s"
        geofences = self._dbc.autofetch_column(query, args=(self.identifier))
        self._data['fields']['webhookgeofences'] = geofences

    def save(self, force_insert: Optional[bool] = False, ignore_issues: Optional[List[str]] = []) -> int:
        self.presave_validation(ignore_issues=ignore_issues)
        core_data = self.get_core()
        del core_data["webhookgeofences"]

        super().save(core_data, force_insert=force_insert, ignore_issues=ignore_issues)

        del_data = {
            'webhook_id': self.identifier
        }
        self._dbc.autoexec_delete('settings_webhook_to_webhookgeofence', del_data)
        print(self._data['fields'])
        for _, webhookgeofence_id in enumerate(self._data['fields']['webhookgeofences']):
            data = {
                'webhook_id': self.identifier,
                'webhookgeofence_id': webhookgeofence_id,
            }
            try:
                self._dbc.autoexec_insert('settings_webhook_to_webhookgeofence', data)
            except mysql.connector.Error:
                logger.info('Duplicate webhookgeofence {} detected for webhook {}', webhookgeofence_id, self.identifier,)
        return self.identifier
