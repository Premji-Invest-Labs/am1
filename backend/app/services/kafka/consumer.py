import json
import asyncio
import logging
from datetime import datetime
import aiokafka
from app.schemas.kafka import KafkaTaskRequest

logger = logging.getLogger(__name__)


class KafkaConsumer:
    def __init__(self, bootstrap_servers, topic, group_id="background_processor"):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.group_id = group_id
        self.consumer = None
        self.running = False

    async def start(self):
        self.consumer = aiokafka.AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            auto_offset_reset="earliest",
            enable_auto_commit=False,
            value_deserializer=lambda m: json.loads(m.decode("utf-8"))
        )
        await self.consumer.start()
        logger.info(f"Kafka consumer started for topic {self.topic}")
        self.running = True

    async def stop(self):
        if self.consumer:
            self.running = False
            await self.consumer.stop()
            logger.info(f"Kafka consumer stopped for topic {self.topic}")

    async def process_job(self, job_data):
        """Process a job from the Kafka topic."""
        # Convert ISO datetime string back to datetime object
        job_data["created_at"] = datetime.fromisoformat(job_data["created_at"])
        job = KafkaTaskRequest(**job_data)

        logger.info(f"Processing job {job.id} of type {job.task_type}")

        try:
            # Implement your actual job processing logic here
            if job.task_type == "email":
                await self._process_email_job(job)
            elif job.task_type == "report":
                await self._process_report_job(job)
            else:
                logger.warning(f"Unknown job type: {job.task_type}")

            # Update job status to completed
            job.status = "completed"
            logger.info(f"KafkaTaskRequest {job.id} processed successfully")

        except Exception as e:
            # Update job status to failed
            job.status = "failed"
            logger.error(f"Error processing job {job.id}: {str(e)}")

        # In a real system, you might want to update a database with the job status
        return job

    async def _process_email_job(self, job):
        """Process an email job."""
        logger.info(f"Sending email: {job.payload.get('subject', 'No subject')}")
        # Simulate processing time
        await asyncio.sleep(2)

    async def _process_report_job(self, job):
        """Process a report generation job."""
        logger.info(f"Generating report: {job.payload.get('report_type', 'Unknown')}")
        # Simulate processing time
        await asyncio.sleep(5)

    async def consume(self):
        """Consume messages from the Kafka topic and process them."""
        if not self.consumer:
            raise RuntimeError("Consumer not started")

        try:
            async for message in self.consumer:
                if not self.running:
                    break

                logger.info(f"Received message from partition {message.partition} at offset {message.offset}")

                try:
                    # Process the job
                    job_data = message.value
                    await self.process_job(job_data)

                    # Commit the offset
                    await self.consumer.commit()

                except Exception as e:
                    logger.error(f"Error processing message: {str(e)}")

        except Exception as e:
            logger.error(f"Consumer error: {str(e)}")
            if self.running:
                # Attempt to restart the consumer
                await self.stop()
                await asyncio.sleep(5)
                await self.start()
                asyncio.create_task(self.consume())