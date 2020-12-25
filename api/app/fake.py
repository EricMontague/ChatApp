"""This file contains a class that uses the faker package for
inserted fake data into the database.
"""


import random
from faker import Faker
from app.clients import dynamodb_client
from app.repositories import dynamodb_repository
from app.dynamodb import (
    UserMapper, 
    UsernameMapper, 
    UserEmailMapper,
    CommunityMapper,
    CommunityNameMapper,
    CommunityMembershipMapper
)
from app.models.factories import UserFactory, CommunityFactory
from app.models import UserEmail, Username, CommunityName, CommunityMembership, CommunityTopic
from app.dynamodb.constants import PrimaryKeyPrefix


user_mapper = UserMapper()
username_mapper = UsernameMapper()
user_email_mapper = UserEmailMapper()
community_mapper = CommunityMapper()
community_name_mapper = CommunityNameMapper()
community_membership_mapper = CommunityMembershipMapper()


TOPICS = [topic for topic in CommunityTopic]
LOCATIONS = [
    {"city" : "New York", "state": "New York", "country": "United States"},
    {"city" : "Philadelphia", "state": "Pennsylvania", "country": "United States"},
    {"city" : "Chicago", "state": "Illinois", "country": "United States"},
    {"city" : "San Francisco", "state": "California", "country": "United States"},
    {"city" : "Miami", "state": "Florida", "country": "United States"}
]


class FakeDataGenerator:
    """Class to generate fake data for the application."""

    def __init__(self, num_users=25, num_communities=25):
        self._faker = Faker()
        self.num_users = num_users
        self.num_communities = num_communities

    def add_users(self):
        """Add fake user data to the database."""
        remaining_users = self.num_users
        while remaining_users > 0:
            requests = []
            user_data = self._generate_fake_user_data()
            user = UserFactory.create_user(user_data)
            user_email = UserEmail(user.id, user.email)
            username = Username(user.id, user.username)
            requests.append(
                (
                    "PutRequest", 
                    user_mapper.serialize_from_model(
                        user, 
                        additional_attributes={"USERS_GSI_SK": user.username}
                    )
                )
            )
            requests.append(("PutRequest", user_email_mapper.serialize_from_model(user_email)))
            requests.append(("PutRequest", username_mapper.serialize_from_model(username)))
            dynamodb_client.batch_write_items(requests)
            remaining_users -= 1

    def add_notifications(self):
        """Add fake notification data to the database."""
        pass

    def add_chat_requests(self):
        """Add fake chat request data to the database."""
        pass

    def add_communities(self):
        """Add fake community data to the database."""
        results = dynamodb_repository.get_users(25)
        users = results["models"]
        remaining_communities = self.num_communities
        while remaining_communities > 0:
            requests = []
            community_data = self._generate_fake_community_data()
            community = CommunityFactory.create_community(community_data)
            community_name = CommunityName(community.id, community.name)
            community_membership = CommunityMembership(
                community.id, 
                random.choice(users).id, 
                is_founder=True
            )
            additional_attributes={
                "COMMUNITY_BY_TOPIC_GSI_PK": PrimaryKeyPrefix.TOPIC + community.topic.name,
                "COMMUNITY_BY_TOPIC_GSI_SK": PrimaryKeyPrefix.COMMUNITY + community.id,
                "COMMUNITY_BY_LOCATION_GSI_PK": PrimaryKeyPrefix.COUNTRY + community.location.country,
                "COMMUNITY_BY_LOCATION_GSI_SK": (
                    PrimaryKeyPrefix.STATE + community.location.state 
                    + PrimaryKeyPrefix.CITY + community.location.city
                )
            }
            requests.append(
                (
                    "PutRequest",
                    community_mapper.serialize_from_model(
                        community, additional_attributes=additional_attributes

                    )
                )
            )
            requests.append(
                (
                    "PutRequest",
                    community_membership_mapper.serialize_from_model(community_membership)
                )
            )
            requests.append(("PutRequest", community_name_mapper.serialize_from_model(community_name)))
            dynamodb_client.batch_write_items(requests)
            remaining_communities -= 1

    def add_group_chats(self):
        """Add fake group chat data to the database."""
        pass

    def add_private_chats(self):
        """Add fake private chat data to the database."""
        pass

    def _generate_fake_community_data(self):
        """Return fake community data as a dictionary."""
        fake_community_data = {
            "name": self._faker.name(),
            "description": self._faker.paragraph()[:280],
            "topic": random.choice(TOPICS),
            "location": random.choices(LOCATIONS)
        }
        return fake_community_data

    def _generate_fake_user_data(self):
        """Return fake user data as a dictionary."""
        name = self._faker.name()
        fake_user_data = {
            "name": name,
            "username": name + "123",
            "email": self._faker.email(),
            "password": "password",
            "location": {
                "city": self._faker.city(),
                "state": self._faker.state(),
                "country": "United States"
            }
        }
        return fake_user_data