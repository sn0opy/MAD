from .resourceHandler import ResourceHandler


class APIWebhook(ResourceHandler):
    component = 'webhook'
    description = 'Add/Update/Delete webhooks'
