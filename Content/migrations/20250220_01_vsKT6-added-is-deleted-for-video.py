"""
Added is_deleted for video
"""

from yoyo import step

__depends__ = {'20241109_01_Nxmmp-init-tables-videos-videos-tags'}

steps = [
    step("""
        ALTER TABLE videos
        ADD COLUMN is_deleted BOOLEAN NOT NULL DEFAULT FALSE;
        """,
        """
            ALTER TABLE videos
            DROP COLUMN is_deleted;
        """ 
    )
]
