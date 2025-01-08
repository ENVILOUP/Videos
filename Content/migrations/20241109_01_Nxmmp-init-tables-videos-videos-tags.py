"""
Init tables 'videos', 'videos_tags'
"""

from yoyo import step

__depends__ = {}

steps = [
    step("""
        CREATE TABLE videos (
            id SERIAL PRIMARY KEY,
            video_uuid UUID NOT NULL UNIQUE,
            yt_id TEXT DEFAULT NULL, 
            title TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        "DROP TABLE IF EXISTS videos;"
    ),
    step("""
        CREATE TABLE videos_tags (
            id SERIAL PRIMARY KEY,
            video_uuid UUID NOT NULL,
            tag TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        "DROP TABLE IF EXISTS videos_tags;"
    ),
    step(
        "CREATE INDEX idx_videos_video_uuid ON videos(video_uuid);",
        "DROP INDEX IF EXISTS idx_videos_video_uuid;"
    ),
    step(
        "CREATE INDEX idx_videos_tags_video_uuid ON videos_tags(video_uuid);",
        "DROP INDEX IF EXISTS idx_videos_tags_video_uuid;"
    ),
    step(
        "ALTER TABLE videos_tags ADD CONSTRAINT unique_video_tag UNIQUE (video_uuid, tag);",
        "ALTER TABLE videos_tags DROP CONSTRAINT IF EXISTS unique_video_tag;"
    )
]
