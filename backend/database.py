from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime
from databases import Database

# Separate databases for URL shortener and authentication
SHORTENER_DATABASE_URL = "sqlite:///./shortener.db"
AUTH_DATABASE_URL = "sqlite:///./auth.db"

shortener_engine = create_engine(SHORTENER_DATABASE_URL, connect_args={"check_same_thread": False})
auth_engine = create_engine(AUTH_DATABASE_URL, connect_args={"check_same_thread": False})

shortener_metadata = MetaData()
auth_metadata = MetaData()

urls = Table(
    "urls",
    shortener_metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("original_url", String, nullable=False),
    Column("shortened_url", String, nullable=False, unique=True),
    Column("custom_alias", String, unique=True, nullable=True),
    Column("expiry_date", DateTime, nullable=True),
)

users = Table(
    "users",
    auth_metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("username", String, unique=True, nullable=False),
    Column("email", String, unique=True, nullable=False),
     Column("password", String, nullable=True),  # Normal login users will have passwords, OAuth users will have NULL
    Column("auth_provider", String, nullable=True),  # "google" or "facebook"
    Column("provider_id", String, unique=True, nullable=True),  # OAuth Provider ID (Google/Facebook ID)
)

shortener_metadata.create_all(bind=shortener_engine)
auth_metadata.create_all(bind=auth_engine)

shortener_database = Database(SHORTENER_DATABASE_URL)
auth_database = Database(AUTH_DATABASE_URL)
