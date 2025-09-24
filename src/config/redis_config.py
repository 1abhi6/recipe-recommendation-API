import os
from dotenv import load_dotenv
import redis


load_dotenv()

class RedisClient:
    def __init__(self):
        self.host = os.getenv("REDIS_HOST")
        self.port = int(os.getenv("REDIS_PORT"))
        self.username="default"
        self.password = os.getenv("REDIS_PASSWORD")
        
        self.client = redis.Redis(
            host=self.host,
            port=self.port,
            password=self.password,
            username=self.username,
            decode_responses=True
        )

    def get_client(self):
        return self.client

redis_client = RedisClient().get_client()