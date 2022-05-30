import os

from src.app.connected_query_handler import ConnectedQueryHandler
from src.domain.events.store import EventStore
from src.domain.model.connection_repository import ConnectionRepository
from src.domain.model.developers_repository import DevelopersRepository
from src.github.user_retriever import GithubUserRetriever
from src.persistence.developers_repository import ExternalDevelopersRepository
from src.persistence.event_sourced_connection_repository import (
    EventSourcedConnectionRepository,
)
from src.persistence.events.csv_event_store import CSVEventStore
from src.twitter.user_retriever import TwitterUsersRetriever


def twitter_retriever() -> TwitterUsersRetriever:
    return TwitterUsersRetriever(api_token=os.environ["JAT_TWITTER_API_TOKEN"])


def github_retriever() -> GithubUserRetriever:
    return GithubUserRetriever(api_token=os.environ["JAT_GITHUB_API_TOKEN"])


def developers_repository() -> DevelopersRepository:
    return ExternalDevelopersRepository(twitter_retriever(), github_retriever())


def event_store() -> EventStore:
    return CSVEventStore("data/events.csv")


def connection_repository() -> ConnectionRepository:
    return EventSourcedConnectionRepository(event_store=event_store())


def create_connection_query_handler() -> ConnectedQueryHandler:
    return ConnectedQueryHandler(
        developers_repository=developers_repository(),
        connection_repository=connection_repository(),
    )
