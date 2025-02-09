from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4
from asyncpg import Connection

from app.profile.models import Channel, UserProfile


class ProfileRepository:

    @staticmethod
    async def add_profile(conn: Connection, profile: UserProfile) -> Optional[UUID]:
        profile.profile_uuid = uuid4()

        query = """
            INSERT INTO user_profiles
                (profile_uuid,
                 user_uuid,
                 name,
                 created_at,
                 updated_at)
            VALUES
                ($1, $2, $3, $4, $5)
            ON CONFLICT (profile_uuid) DO UPDATE SET
                user_uuid = EXCLUDED.user_uuid,
                name = EXCLUDED.name,
                updated_at = EXCLUDED.updated_at
            WHERE user_profiles.profile_uuid = EXCLUDED.profile_uuid
            RETURNING profile_uuid;
        """

        args = (profile.profile_uuid,
                profile.user_uuid,
                profile.name,
                profile.created_at,
                profile.updated_at)

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
                created_at,
                updated_at
            FROM user_profiles
            WHERE profile_uuid = $1;
        """

        result = await conn.fetchrow(query, uuid)

        if not result:
            return None

        return UserProfile(**result)

    @staticmethod
    async def update_profile(conn: Connection, profile: UserProfile) -> Optional[UUID]:
        profile.updated_at = datetime.now()

        query = """
            UPDATE user_profiles
            SET
                user_id = $1,
                name = $2,
                updated_at = $3
            WHERE profile_uuid = $4;
        """

        args = (profile.user_uuid,
                profile.name,
                profile.updated_at,
                profile.profile_uuid)

        result = await conn.execute(query, *args)

        if not result:
            return None

        return result.get('profile_uuid')

    @staticmethod
    async def delete_profile(conn: Connection, uuid: UUID) -> Optional[UUID]:

        query = """
            UPDATE user_profiles
            SET
                deleted = true
            WHERE profile_uuid = $4;
        """

        result = await conn.execute(query, uuid)

        if not result:
            return None

        return result.get('profile_uuid')


class ChannelRepository:

    @staticmethod
    async def add_channel(conn: Connection, channel: Channel) -> Optional[UUID]:
        channel.channel_uuid = uuid4()

        query = """
            INSERT INTO channels
                (channel_uuid,
                 owner_uuid,
                 name,
                 created_at,
                 updated_at)
            VALUES
                ($1, $2, $3, $4, $5)
            ON CONFLICT (channel_uuid) DO UPDATE SET
                owner_uuid = EXCLUDED.owner_uuid,
                name = EXCLUDED.name,
                updated_at = EXCLUDED.updated_at
            WHERE channels.channel_uuid = EXCLUDED.channel_uuid
            RETURNING channel_uuid;
        """

        args = (channel.channel_uuid,
                channel.owner_uuid,
                channel.name,
                channel.created_at,
                channel.updated_at)

        result = await conn.fetchrow(query, *args)

        if not result:
            return None

        return result.get('channel_uuid')

    @staticmethod
    async def get_channel(conn: Connection, uuid: UUID) -> Optional[Channel]:
        query = """
            SELECT
                channel_uuid,
                owner_uuid,
                name,
                created_at,
                updated_at
            FROM channels
            WHERE channel_uuid = $1;
        """

        result = await conn.fetchrow(query, uuid)

        if not result:
            return None

        return Channel(**result)

    @staticmethod
    async def get_channels(conn: Connection, owner_uuid: Optional[UUID]) -> Optional[List[Channel]]:
        query = """
            SELECT
                channel_uuid,
                owner_uuid,
                name,
                created_at,
                updated_at
            FROM channels 
            WHERE owner_uuid = $1;
        """

        result = await conn.fetch(query, owner_uuid)

        if not result:
            return None

        return [Channel(**channel) for channel in result]

    @staticmethod
    async def delete_channel(conn: Connection, uuid: UUID) -> Optional[UUID]:
        query = """
            UPDATE user_profiles
            SET
                deleted = true
            WHERE profile_uuid = $4;
        """

        result = await conn.execute(query, uuid)

        if not result:
            return None

        return result.get('channel_uuid')

    @staticmethod
    async def update_channel(conn: Connection, channel: Channel) -> Optional[UUID]:
        query = """
            UPDATE channels
            SET
                name = $1,
                updated_at = $2
            WHERE channel_uuid = $3;
        """

        args = (channel.name,
                channel.updated_at,
                channel.channel_uuid)

        result = await conn.execute(query, *args)

        if not result:
            return None

        return result.get('channel_uuid')
