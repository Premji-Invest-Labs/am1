import json
import uuid
import logging
from datetime import datetime
import aiokafka
from app.schemas.kafka import KafkaTaskRequest

logger = logging.getLogger(__name__)


class KafkaProducer:
    def __init__(self, bootstrap_servers):
        self.bootstrap_servers = bootstrap_servers
        self.producer = None

    async def start(self):
        self.producer = aiokafka.AIOKafkaProducer(
            bootstrap_servers=self.bootstrap_servers
        )
        await self.producer.start()
        logger.info("Kafka producer started")

    async def stop(self):
        if self.producer:
            await self.producer.stop()
            logger.info("Kafka producer stopped")

    async def send_job(self, job: KafkaTaskRequest, topic: str):
        if not self.producer:
            raise RuntimeError("Producer not started")

        # Convert the job to a JSON string
        job_data = job.model_dump()
        job_data["created_at"] = job_data["created_at"].isoformat()
        job_str = json.dumps(job_data)

        # Send the job to Kafka topic
        await self.producer.send_and_wait(
            topic=topic,
            value=job_str.encode("utf-8"),
            key=job.id.encode("utf-8")
        )

        logger.info(f"Job {job.task_id} sent to topic {topic}")
        return job