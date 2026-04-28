import json
import logging
from aiokafka import AIOKafkaProducer
from src.infrastructure.config.settings import settings

logger = logging.getLogger(__name__)


class KafkaProducer:
    def __init__(self):
        self._producer: AIOKafkaProducer | None = None

    async def initialize(self):
        try:
            self._producer = AIOKafkaProducer(
                bootstrap_servers=settings.kafka_servers,
                value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8'),
                compression_type='gzip',
                max_request_size=1048576,
                acks='all',
                retries=3,
            )
            await self._producer.start()
            logger.info("Kafka producer connected successfully")
        except Exception as e:
            logger.error(f"Failed to connect Kafka producer: {e}")
            raise

    async def close(self):
        if self._producer:
            await self._producer.flush()
            await self._producer.stop()
            self._producer = None
            logger.info("Kafka producer closed")

    async def send_event(
            self,
            topic: str,
            event: dict,
            key: str | None = None,
    ) -> bool:
        try:
            if key:
                key_bytes = key.encode('utf-8')
            else:
                key_bytes = None

            await self._producer.send_and_wait(
                topic=topic,
                value=event,
                key=key_bytes,
            )
            logger.debug(f"Event sent to {topic}: {event}")
            return True
        except Exception as e:
            logger.error(f"Failed to send event to {topic}: {e}")
            return False


kafka_producer = KafkaProducer()
