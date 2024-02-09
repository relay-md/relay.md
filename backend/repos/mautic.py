# -*- coding: utf-8 -*-

from requests import Session

from ..config import get_config


class MauticAPI(object):
    def __init__(self):
        config = get_config()
        self.url = config.MAUTIC_API_BASE_URL
        self.session = Session()
        self.session.auth = (config.MAUTIC_API_USERNAME, config.MAUTIC_API_PASSWORD)

    @property
    def enabled(self) -> bool:
        return bool(self.url)

    def _process_req(self, req) -> dict:
        req.raise_for_status()
        return req.json()

    def post(self, api: str, payload: dict) -> dict:
        if not self.enabled:
            return {}
        req = self.session.post(f"{self.url}/api/{api}", json=payload)
        return self._process_req(req)

    def patch(self, api: str, payload: dict) -> dict:
        if not self.enabled:
            return {}
        req = self.session.patch(f"{self.url}/api/{api}", json=payload)
        return self._process_req(req)

    def get(self, api: str, params=dict()) -> dict:
        if not self.enabled:
            return {}
        req = self.session.get(f"{self.url}/api/{api}", params=params)
        return self._process_req(req)


class MauticRepo(MauticAPI):
    def add_contact(
        self,
        email,
        **kwargs,
    ):
        email = email.lower()
        contact = self.post(
            "contacts/new",
            dict(
                email=email,
                # TODO: might want to update this field
                # lastActive="Y-m-d H:m:i"
                # If true, then empty values are set to fields. Otherwise empty values are skipped
                overwriteWithBlank=True,
                **kwargs,
            ),
        )

        # add to segement
        mautic_segment = get_config().MAUTIC_USER_SEGMENT_ID
        if mautic_segment:
            self.post(
                f"segments/{mautic_segment}/contact/{contact['contact']['id']}/add", {}
            )

        return contact

    def update_contact(self, email, **kwargs):
        email = email.lower()
        params = dict(col="email", expr="eq", val=email)
        contacts: dict = self.get("contacts", params=params)
        contact = list(contacts.get("contacts", {}).keys())
        if not contact:
            return self.add_contact(email, **kwargs)
        return self.patch(f"contacts/{contact[0]}/edit", kwargs)
