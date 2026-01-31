import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app_environment import AppEnvironment
from env import env

# PostgreSQL
engine = create_engine(
    f"postgresql://{env.DB_USER}:{env.DB_PASSWORD}@{env.DB_HOST}:{env.DB_PORT}/{env.DB_NAME}",
    pool_pre_ping=True,
    pool_recycle=1800,
)

# Redis
redis_client = redis.Redis(
    host=env.REDIS_HOST,
    port=env.REDIS_PORT,
    password=None if AppEnvironment.is_local_env(env.APP_ENV) else env.REDIS_PASSWORD,
    decode_responses=False,
)

# Session
Session = sessionmaker(bind=engine)