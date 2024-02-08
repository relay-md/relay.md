# -*- coding: utf-8 -*-
from ..models.stripe import StripeCustomer, StripeSubscription
from .base import DatabaseAbstractRepository


class StripeCustomerRepo(DatabaseAbstractRepository):
    ORM_Model = StripeCustomer


class StripeSubscriptionRepo(DatabaseAbstractRepository):
    ORM_Model = StripeSubscription
