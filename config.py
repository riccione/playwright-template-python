import os

from dotenv import load_dotenv

# Load variables from the local .env file into os.environ
load_dotenv()


class Config:
    """Centralized configuration values for the test framework."""

    BASE_URL = os.getenv("BASE_URL", "https://default-fallback.example.com")
    ADMIN_USER = os.getenv("ADMIN_USER")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")


# Create a single instance to import across the framework
settings = Config()
