import os

from celery import Celery

queue = Celery(
    task_acks_late=True,
    broker=os.environ["REDIS_URL"],
    redis_max_connections=int(os.getenv("REDIS_MAX_CONN", 20)),
    include=[
        f"platforms.{platform.strip()}.tasks"
        for platform in os.environ["PLATFORMS"].split(",")
    ],
)
