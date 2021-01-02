"""This module contains models to represent various types of
chats in the application.
"""


from dataclasses import dataclass
from datetime import datetime
from abc import ABC
from app.exceptions import (
    ChatCapacityReachedException,
    ChatMemberNotFoundException,
    ChatMessageNotFoundException,
    ChatRequestNotFoundException,
)


class Chat(ABC):
    """Abstract base class that represents a chat."""

    def __init__(self, id, name, description):
        self._id = id
        self.name = name
        self.description = description
        self._messages = {}
        self._members = {}

    @property
    def members(self):
        """Return a list of the chat's members."""
        return [member for member in self._members.values()]

    def post_message(self, message):
        """Add a message to the chat's list of messages."""
        self._messages[message.id] = message
        return True

    def edit_message(self, message_id, new_content):
        """Edit a message in the chat."""
        if not self.has_message(message_id):
            raise ChatMessageNotFoundException(
                "The specified message could not be found"
            )
        self._messages[message_id].edit(new_content)

    def delete_message(self, message_id):
        """Delete the given message from the chat."""
        if not self.has_message(message_id):
            raise ChatMessageNotFoundException(
                "The specified message could not be found"
            )
        self._messages.pop(message_id)

    def has_message(self, message_id):
        """Return True if a message with the given id exists
        in the chat, otherwise return False.
        """
        return message_id in self._messages

    def react_to_message(self, message_id, reaction):
        """Add a reaction to the given message."""
        if not self.has_message(message_id):
            raise ChatMessageNotFoundException(
                "The specified message could not be found"
            )
        self._messages[message_id].add_reaction(reaction)

    @property
    def id(self):
        """Return the chat id."""
        return self._id

    @property
    def messages(self):
        """Return a list of the chat's messages sorted
        from most recent to least recent.
        """
        return sorted(self._messages, key=lambda m: m.timestamp)


class PrivateChat(Chat):
    """Class to represent a private chat between two users"""

    CAPACITY = 2

    def __init__(self, id, primary_user, secondary_user):
        self._id = id
        self._primary_user = primary_user
        self._secondary_user = secondary_user

    @property
    def id(self):
        """Return the chat's id."""
        return self._id

    def __repr__(self):
        """Return a representatino of a private chat."""
        return "PrivateChat(id=%r, primary_user=%r, secondary_user=%r)" % (
            self._id,
            self._primary_user,
            self._secondary_user,
        )


class GroupChat(Chat):
    """Class to represent a group chat between one or more users
    in a specific community
    """

    def __init__(self, id, community_id, name, description, capacity):
        super().__init__(id, name, description)
        self._capacity = capacity
        self._community_id = community_id

    @property
    def community_id(self):
        """Return the id of the community the group chat belongs to."""
        return self._community_id

    def add_member(self, member):
        """Add a member to the group chat."""
        self._members[member.id] = member

    def remove_member(self, member_id):
        """Remove a member with the given id from the group chat."""
        if not self.is_member(member_id):
            raise ChatMemberNotFoundException(
                "The given user is not a member of this chat"
            )
        self._members.pop(member_id)

    def is_member(self, user_id):
        """Return True if there is a user with the given id
        in the group chat, otherwise return False.
        """
        return user_id in self._members

    def __repr__(self):
        """Return a representation of a group chat."""
        return (
            "GroupChat(id=%r, community_id=%r, name=%r, description=%r, capacity=%r)"
            % (
                self._id,
                self._community_id,
                self.name,
                self.description,
                self._capacity,
            )
        )


@dataclass(frozen=True)
class PrivateChatMember:
    """Class to represent the relationship between a private chat and 
    a user who is a member of that private chat.
    """

    private_chat_id: str
    user_id: str
    other_user_id: str
    created_at: datetime = datetime.now()


@dataclass(frozen=True)
class GroupChatMember:
    """Class to represent the relationship between a private chat and 
    a user who is a member of that private chat.
    """

    group_chat_id: str
    user_id: str
    created_at: datetime = datetime.now()

