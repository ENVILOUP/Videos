"""
Init tables user_profiles, channels
"""

from yoyo import step

__depends__ = {}

steps = [
    step("""
        CREATE TABLE user_profiles (
            id SERIAL PRIMARY KEY,
            profile_uuid UUID NOT NULL UNIQUE,
            user_uuid UUID NOT NULL UNIQUE,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            deleted BOOLEAN DEFAULT FALSE
        );
        """,
        "DROP TABLE IF EXISTS user_profiles;"
    ),
    step("""
        CREATE TABLE channels (
            id SERIAL PRIMARY KEY,
            channel_uuid UUID NOT NULL UNIQUE,
            owner_uuid UUID NOT NULL,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            deleted BOOLEAN DEFAULT FALSE
        );
        """,
        "DROP TABLE IF EXISTS channels;"
    )
]
