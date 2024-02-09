# -*- coding: utf-8 -*-
import logging
from typing import Optional

from requests import Session

from ..config import get_config
from ..models.billing import PersonalInformation, Subscription
from ..models.user import User

log = logging.getLogger(__name__)


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
        if str(req.status_code)[0] != 2:
            # log.error(req.text)
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
            self.add_contact_to_segment(contact["contact"]["id"], mautic_segment)

        return contact

    def find_contact(self, email) -> Optional[dict]:
        params = dict(col="email", expr="eq", val=email)
        contacts: dict = self.get("contacts", params=params)
        contact_ids = list(contacts.get("contacts", {}).keys())
        if contact_ids:
            return contacts["contacts"].get(contact_ids[0])

    def find_contact_from_user(self, user: User) -> Optional[dict]:
        params = dict(col="user_id", expr="eq", val=str(user.id))
        contacts: dict = self.get("contacts", params=params)
        contact_ids = list(contacts.get("contacts", {}).keys())
        if contact_ids:
            return contacts["contacts"].get(contact_ids[0])

    def update_contact(self, email, **kwargs):
        email = email.lower()
        contact = self.find_contact(email)
        if not contact:
            return self.add_contact(email, **kwargs)
        return self.patch(f"contacts/{contact['id']}/edit", kwargs)

    def process_user(self, user: User):
        firstname, *_, lastname = user.name.split(" ")
        return self.update_contact(
            user.email, firstname=firstname, lastname=lastname, user_id=str(user.id)
        )

    def process_person(self, person: PersonalInformation):
        self.update_contact(
            person.user.email,
            city=person.city,
            country_code=person.country_code,
            address1=person.address_line1,
            address2=person.address_line2,
            zipcode=person.zip,
            state_str=person.state,
            phone=person.phone_country_code + person.phone_number,
        )

    def process_subscription(self, subscription: Subscription):
        if not get_config().MAUTIC_SUBSCRIPTION_SEGMENT_ID:
            return
        contact = self.find_contact_from_user(subscription.user)
        if not contact:
            log.warning(
                f"No contact found in mautic for user {subscription.user.username}"
            )
            return
        if subscription.active:
            self.add_contact_to_segment(
                contact, get_config().MAUTIC_SUBSCRIPTION_SEGMENT_ID
            )
        else:
            self.remove_contact_to_segment(
                contact, get_config().MAUTIC_SUBSCRIPTION_SEGMENT_ID
            )

    def add_contact_to_segment(self, contact, segment_id):
        self.post(f"segments/{segment_id}/contact/{contact['id']}/add", {})

    def remove_contact_to_segment(self, contact: dict, segment_id):
        self.post(f"segments/{segment_id}/contact/{contact['id']}/remove", {})
