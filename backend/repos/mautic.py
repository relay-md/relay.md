import requests
from requests import Session
from ..config import get_config


class MauticAPI(object):
    def __init__(self):
        config = get_config()
        self.url = config.MAUTIC_API_BASE_URL
        self.session = Session()
        self.session.auth = (config.MAUTIC_API_USERNAME, config.MAUTIC_API_PASSWORD)

    def _process_req(self, req):
        req.raise_for_status()
        return req.json()

    def post(self, api: str, payload: dict):
        req = self.session.post(f"{self.url}/api/{api}", json=payload)
        return self._process_req(req)

    def get(self, api: str):
        print((f"{self.url}/api/{api}"))
        req = self.session.get(f"{self.url}/api/{api}")
        return self._process_req(req)


class MauticRepo(MauticAPI):
    pass
