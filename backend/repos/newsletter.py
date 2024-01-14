# -*- coding: utf-8 -*-
import requests

from backend.exceptions import AlreadySubscribed

from ..config import get_config


class NewsletterRepo:
    def subscribe(self, email, first_name, last_name, status="pending"):
        req = requests.post(
            f"https://{get_config().MAILCHIMP_API_SERVER}.api.mailchimp.com/3.0/lists/{get_config().MAILCHIMP_LIST_ID}/members",
            auth=("key", get_config().MAILCHIMP_API_KEY),
            headers={"content-type": "application/json"},
            json={
                "email_address": email,
                "status": status,
                "merge_fields": {"FNAME": first_name, "LNAME": last_name},
            },
        )
        res = req.json()
        if not req.ok:
            if res.get("title") == "Member Exists":
                raise AlreadySubscribed
            raise Exception(res.get("title", "An error occured!"))
        return req.json()
