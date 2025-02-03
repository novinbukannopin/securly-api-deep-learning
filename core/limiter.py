from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import REDIS_HOST, REDIS_PORT
from redis import Redis
from core.blacklist_loader import load_blocklist_to_redis
from config import BLOCKLIST_FILE

class LimiterService:
    def __init__(self, app):
        self.redis_host = REDIS_HOST
        self.redis_port = REDIS_PORT
        try:
            self.redis_client = Redis(host=self.redis_host, port=self.redis_port, db=0)
            self.redis_client.ping()
            print(f"Connected to Redis at {self.redis_host}:{self.redis_port}")

            # load_blocklist_to_redis(self.redis_client, BLOCKLIST_FILE)

        except Exception as e:
            raise RuntimeError(f"Failed to connect to Redis: {e}")

        self.limiter = Limiter(
            get_remote_address,
            app=app,
            storage_uri=f"redis://{self.redis_host}:{self.redis_port}"
        )

    def get_limiter(self):
        return self.limiter

    def get_redis_client(self):
        return self.redis_client


