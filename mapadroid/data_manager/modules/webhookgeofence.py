from .resource import Resource


class WebhookGeofence(Resource):
    table = 'settings_webhookgeofence'
    name_field = 'webhook_id'
    primary_key = 'webhookgeofence_id'
    search_field = 'webhookgeofence_id'
    configuration = {
        "fields": {
            "geofence_id": {
                "settings": {
                    "type": "geofenceselect",
                    "require": True,
                    "empty": None,
                    "description": "Geofeeeeeeeeeeeeence",
                    "expected": int,
                    "uri": True,
                    "data_source": "geofence",
                    "uri_source": "api_geofence"
                }
            },
            "kind": {
                "settings": {
                    "type": "option",
                    "values": ["include", "exclude"],
                    "require": True,
                    "description": "Set this geofence to either be included or excluded",
                    "expected": str
                }
            },
        }
    }
