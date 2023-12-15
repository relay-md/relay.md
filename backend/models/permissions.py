# -*- coding: utf-8 -*-
import enum

CAN_READ = 2**0
CAN_POST = 2**1
CAN_MODIFY = 2**2
CAN_CREATE_TOPICS = 2**3
CAN_INVITE = 2**4
CAN_JOIN = 2**5


class Permissions(enum.IntFlag):
    can_read = CAN_READ
    can_post = CAN_POST
    can_modify = CAN_MODIFY
    can_create_topics = CAN_CREATE_TOPICS
    can_invite = CAN_INVITE
    can_join = CAN_JOIN


class OwnerPermissions(enum.IntFlag):
    can_read = CAN_READ
    can_post = CAN_POST
    can_modify = CAN_MODIFY
    can_create_topics = CAN_CREATE_TOPICS
    can_invite = CAN_INVITE
    # can_join = CAN_JOIN


class MemberPermissions(enum.IntFlag):
    can_read = CAN_READ
    can_post = CAN_POST
    can_modify = CAN_MODIFY
    can_create_topics = CAN_CREATE_TOPICS
    can_invite = CAN_INVITE
    # can_join = CAN_JOIN


class PublicPermissions(enum.IntFlag):
    can_read = CAN_READ
    can_post = CAN_POST
    can_modify = CAN_MODIFY
    can_create_topics = CAN_CREATE_TOPICS
    # can_invite = CAN_INVITE
    can_join = CAN_JOIN
