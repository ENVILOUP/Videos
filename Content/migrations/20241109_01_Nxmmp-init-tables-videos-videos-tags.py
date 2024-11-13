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
            title VARCHAR(255) NOT NULL,
            description TEXT,
            video_url VARCHAR(255) NOT NULL,
            thumbnail_url VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            modified_at TIMESTAMP
        );
        """,
        "DROP TABLE IF EXISTS videos;"
    ),
    step("""
        CREATE TABLE videos_tags (
            video_uuid UUID NOT NULL,
            tag VARCHAR(255) NOT NULL,
            FOREIGN KEY (video_uuid) REFERENCES videos(video_uuid) ON DELETE CASCADE
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
        "CREATE INDEX idx_videos_tags_tag ON videos_tags(tag);",
        "DROP INDEX IF EXISTS idx_videos_tags_tag;"
    ),
    step(
        "ALTER TABLE videos_tags ADD CONSTRAINT unique_video_tag UNIQUE (video_uuid, tag);",
        "DROP CONSTRAINT IF EXISTS unique_video_tag;"
    )
]
