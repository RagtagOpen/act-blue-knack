from raven.contrib.django.client import DjangoClient as BaseDjangoClient


class DjangoClient(BaseDjangoClient):
    def get_data_from_request(self, request, *args, **kwargs):
        data = super(DjangoClient, self).get_data_from_request(
            request, *args, **kwargs)
        if data.get('request', {}).get('data'):
            del data['request']['data']
        return data
