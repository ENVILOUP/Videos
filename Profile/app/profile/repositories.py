
from uuid import UUID
from typing import Optional
from asyncpg import Connection
from app.profile.models import UserProfile

class ProfileRepository:

    @staticmethod
    async def add_profile(conn: Connection, profile: UserProfile) -> Optional[UUID]:
        query = """
            INSERT INTO profile
                (profile_uuid,
                 user_id,
                 name,
                 created,
                 updated)
            VALUES
                ($1, $2, $3, $4, $5)
            ON CONFLICT (profile_uuid) DO UPDATE SET
                user_id = EXCLUDED.user_id,
                name = EXCLUDED.name,
                updated = EXCLUDED.updated
            WHERE profile.profile_uuid = EXCLUDED.profile_uuid
            RETURNING profile_uuid;
        """

        args = (profile.profile_uuid,
                profile.user_id,
                profile.name,
                profile.created,
                profile.updated)

        result = await conn.fetchrow(query, *args)

        if not result:
            return None

        return result.get('profile_uuid')

    @staticmethod
    async def get_profile(conn: Connection, uuid: UUID) -> Optional[UserProfile]:
        query = """
            SELECT
                profile_uuid,
                user_id,
                name,
                created,
                updated
            FROM profile
            WHERE profile_uuid = $1;
        """

        result = await conn.fetchrow(query, uuid)
        
        if not result:
            return None
        
        return UserProfile(**result)
    

    @staticmethod
    async def update_profile(conn: Connection, profile: UserProfile) -> Optional[UUID]:
        query = """
            UPDATE profile
            SET
                user_id = $1,
                name = $2,
                updated = $3
            WHERE profile_uuid = $4;
        """

        args = (profile.user_id,
                profile.name,
                profile.updated,
                profile.profile_uuid)

        if not result:
            return None

        result = await conn.execute(query, *args)

        return result.get('profile_uuid')

    @staticmethod
    async def delete_profile(conn: Connection, uuid: UUID) -> Optional[UUID]:
        query = """
            DELETE FROM profile
            WHERE profile_uuid = $1;
        """

        if not result:
            return None

        result = await conn.execute(query, uuid)

    