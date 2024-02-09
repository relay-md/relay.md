# -*- coding: utf-8 -*-
from typing import Optional

import requests

from ..config import get_config


class NewsletterRepo:
    def subscribe(
        self,
        email,
        first_name: Optional[str] = "",
        last_name: Optional[str] = "",
        status="pending",
    ):
        req = requests.post(
            f"{get_config().MAUTIC_API_BASE_URL}/form/submit",
            data={
                "mauticform[email]": email.lower(),
                "mauticform[formId]": get_config().MAUTIC_NEWSLETTER_FORM_ID,
            },
        )
        return req.text
