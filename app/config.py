import os

APP_ENV = os.getenv("APP_ENV", "development")
JWT_SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY", "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caf"
)
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_TOKEN_EXPIRE_MINUTES = os.getenv("JWT_TOKEN_EXPIRE_MINUTES", 60)
APP_EMAIL = os.getenv("APP_EMAIL", "app@ilmx.io")
APP_PASSWORD = os.getenv("APP_PASSWORD", "ilmx-arbisoft042")
