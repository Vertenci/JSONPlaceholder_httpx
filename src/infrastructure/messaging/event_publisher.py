import logging
from src.application.events.user_events import (
    UserCreatedEvent,
    UserUpdatedEvent,
    UserDeletedEvent,
)
from src.application.events.profile_events import ProfileUpdatedEvent
from src.infrastructure.messaging.kafka_producer import kafka_producer
from src.infrastructure.config.settings import settings

logger = logging.getLogger(__name__)


class EventPublisher:
    @staticmethod
    async def publish_user_created(
            user_id: int,
            email: str,
            username: str
    ):
        event = UserCreatedEvent.create(user_id, email, username)

        await EventPublisher._publish_cache_invalidation(
            f"user:{user_id}",
            f"users:list:*"
        )

        await kafka_producer.send_event(
            topic=settings.KAFKA_USER_EVENTS_TOPIC,
            event={
                "type": event.event_type,
                "user_id": event.user_id,
                "timestamp": event.timestamp.isoformat(),
                "data": event.data,
            },
            key=str(user_id),
        )

    @staticmethod
    async def publish_user_updated(user_id: int, changes: dict):
        event = UserUpdatedEvent.create(user_id, changes)

        await EventPublisher._publish_cache_invalidation(
            f"user:{user_id}",
            f"users:list:*"
        )

        await kafka_producer.send_event(
            topic=settings.KAFKA_USER_EVENTS_TOPIC,
            event={
                "type": event.event_type,
                "user_id": event.user_id,
                "timestamp": event.timestamp.isoformat(),
                "data": event.data,
            },
            key=str(user_id),
        )

    @staticmethod
    async def publish_user_deleted(user_id: int):
        event = UserDeletedEvent.create(user_id)

        await EventPublisher._publish_cache_invalidation(
            f"user:{user_id}",
            f"profile:{user_id}",
            f"users:list:*"
        )

        await kafka_producer.send_event(
            topic=settings.KAFKA_USER_EVENTS_TOPIC,
            event={
                "type": event.event_type,
                "user_id": event.user_id,
                "timestamp": event.timestamp.isoformat(),
                "data": event.data,
            },
            key=str(user_id),
        )

    @staticmethod
    async def publish_profile_updated(user_id: int, changes: dict):
        event = ProfileUpdatedEvent.create(user_id, changes)

        await EventPublisher._publish_cache_invalidation(
            f"profile:{user_id}"
        )

        await kafka_producer.send_event(
            topic=settings.KAFKA_PROFILE_EVENTS_TOPIC,
            event={
                "type": event.event_type,
                "user_id": event.user_id,
                "timestamp": event.timestamp.isoformat(),
                "data": event.data,
            },
            key=str(user_id),
        )

    @staticmethod
    async def _publish_cache_invalidation(*patterns: str):
        await kafka_producer.send_event(
            topic="cache-invalidation",
            event={
                "type": "cache.invalidate",
                "patterns": patterns,
                "timestamp": "now",
            },
        )


event_publisher = EventPublisher()
