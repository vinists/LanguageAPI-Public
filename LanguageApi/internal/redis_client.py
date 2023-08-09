from redis import asyncio as redis
import asyncio
import async_timeout
import os


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        if cls not in cls._instances:
            cls._instances[cls] = {}
        if key not in cls._instances[cls]:
            cls._instances[cls][key] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls][key]


class RedisClient(metaclass=Singleton):

    def __init__(self, db=0):
        self.pool = redis.ConnectionPool(host=os.environ["redish"], port=os.environ["redisp"], db=db)

    @property
    def conn(self):
        if not hasattr(self, '_conn'):
            self.get_connection()
        return self._conn

    def get_connection(self):
        self._conn = redis.Redis(connection_pool=self.pool)


class PubSub:
    STOPWORD = b"STOP"
    HANDSHAKE = b"HANDSHAKE"

    def __init__(self, channel_name: str):
        self._redis = RedisClient().conn
        self.channel_name = f"vc:{channel_name}"
        self.pubsub = self._redis.pubsub()
        self._stop_reading = False

    async def _reader(self, channel: redis.client.PubSub):
        while not self._stop_reading:
            try:
                async with async_timeout.timeout(1):
                    message = await channel.get_message(ignore_subscribe_messages=True)
                    if message is not None:
                        if message["data"] == self.STOPWORD:
                            print("(Reader) STOP")
                            yield "Disconnected"
                            break
                        elif message["data"] == self.HANDSHAKE:
                            continue
                        else:
                            yield message
                    await asyncio.sleep(0.01)
            except asyncio.TimeoutError:
                pass

    async def subscribe(self):
        async with self.pubsub as p:
            self._stop_reading = False
            await p.subscribe(self.channel_name)
            async for message in self._reader(p):
                yield message
            await p.unsubscribe(self.channel_name)

    async def unsubscribe(self):
        self._stop_reading = True
        await self.pubsub.unsubscribe(self.channel_name)

    async def handshake(self):
        return await self.publish("HANDSHAKE") > 0

    async def publish(self, message: object):
        return await self._redis.publish(self.channel_name, message)
