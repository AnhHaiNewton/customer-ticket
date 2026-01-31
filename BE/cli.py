import os
import subprocess

import typer
from dotenv import dotenv_values
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists, drop_database

from app_environment import AppEnvironment

cli = typer.Typer()


def get_db_url(app_env: AppEnvironment) -> str:
    """Get database URL based on environment"""
    if AppEnvironment.is_test_env(app_env):
        configs = {**dotenv_values(".env.test")}
    else:
        configs = {**dotenv_values(".env")}
    
    return f"postgresql://{configs['DB_USER']}:{configs['DB_PASSWORD']}@{configs['DB_HOST']}:{configs['DB_PORT']}/{configs['DB_NAME']}"


@cli.command()
def server(app_env: AppEnvironment):
    """Run the FastAPI server"""
    env = os.environ.copy()
    env["APP_ENV"] = app_env.value

    if AppEnvironment.is_local_env(app_env):
        subprocess.run(["fastapi", "dev", "app.py"], env=env)
    else:
        subprocess.run(["fastapi", "run", "app.py", "--port", "8000"], env=env)


@cli.command()
def worker(app_env: AppEnvironment):
    """Run the background worker"""
    env = os.environ.copy()
    env["APP_ENV"] = app_env.value
    subprocess.run(["python", "-m", "services.ticket_worker"], env=env)


@cli.command()
def dbcreate(app_env: AppEnvironment):
    """Create database"""
    db_url = get_db_url(app_env)
    db_engine = create_engine(db_url)
    
    if not database_exists(db_engine.url):
        create_database(db_engine.url)
        print(f"Database created: {app_env.value}")
    else:
        print(f"Database already exists: {app_env.value}")


@cli.command()
def dbdrop(app_env: AppEnvironment):
    """Drop database"""
    db_url = get_db_url(app_env)
    db_engine = create_engine(db_url)
    
    if database_exists(db_engine.url):
        drop_database(db_engine.url)
        print(f"Database dropped: {app_env.value}")
    else:
        print(f"Database does not exist: {app_env.value}")


@cli.command()
def dbmigrate(app_env: AppEnvironment):
    """Run migrations"""
    env = os.environ.copy()
    env["APP_ENV"] = app_env.value
    subprocess.run(["alembic", "upgrade", "head"], env=env)


@cli.command()
def dbrollback(app_env: AppEnvironment, steps: int = 1):
    """Rollback migrations"""
    env = os.environ.copy()
    env["APP_ENV"] = app_env.value
    subprocess.run(["alembic", "downgrade", f"-{steps}"], env=env)


@cli.command()
def dbrevision(message: str):
    """Create new migration"""
    subprocess.run(["alembic", "revision", "--autogenerate", "-m", message])


if __name__ == "__main__":
    cli()