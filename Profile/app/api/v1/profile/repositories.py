from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4
from asyncpg import Connection

from app.helpers.sql import clean_query
from app.models.channel import Channel
from app.models.user_profile import UserProfile


class ProfileRepository:

    def __init__(self, conn: Connection):
        self._conn = conn

    async def add_profile(self, profile: UserProfile) -> Optional[UUID]:
        profile.profile_uuid = uuid4()

        query = clean_query("""
            INSERT INTO user_profiles
                (profile_uuid,
                 user_uuid,
                 name,
                 created_at,
                 updated_at)
            VALUES
                ($1, $2, $3, $4, $5)
            ON CONFLICT DO NOTHING 
            RETURNING profile_uuid;
        """)

        args = (profile.profile_uuid,
                profile.user_uuid,
                profile.name,
                profile.created_at,
                profile.updated_at)

        result = await self._conn.fetchrow(query, *args)

        if not result:
            return None

        return result['profile_uuid']

    async def get_profile(self, uuid: UUID) -> Optional[UserProfile]:
        query = clean_query("""
            SELECT
                profile_uuid,
                user_uuid,
                name,
                created_at,
                updated_at,
                deleted 
            FROM user_profiles
            WHERE profile_uuid = $1 and deleted = false;
        """)

        result = await self._conn.fetchrow(query, uuid)

        if not result:
            return None

        return UserProfile(
            profile_uuid=result['profile_uuid'],
            user_uuid=result['user_uuid'],
            name=result['name'],
            created_at=result['created_at'],
            updated_at=result['updated_at'],
            deleted=result['deleted']
        )

    async def update_profile(self, profile: UserProfile) -> Optional[UUID]:
        profile.updated_at = datetime.now()

        query = clean_query("""
            UPDATE user_profiles
            SET
                user_uuid = $1,
                name = $2,
                updated_at = $3
            WHERE profile_uuid = $4 and deleted = false;
        """)

        args = (profile.user_uuid,
                profile.name,
                profile.updated_at,
                profile.profile_uuid)

        result = await self._conn.execute(query, *args)

        if not result:
            return None

        return profile.profile_uuid

    async def delete_profile(self, uuid: UUID) -> Optional[UUID]:

        query = clean_query("""
            UPDATE user_profiles
            SET
                deleted = true
            WHERE profile_uuid = $1 and deleted = false;
        """)

        result = await self._conn.execute(query, uuid)

        if not result:
            return None

        return uuid


class ChannelRepository:

    def __init__(self, conn: Connection):
        self._conn = conn

    async def add_channel(self, channel: Channel) -> Optional[UUID]:
        channel.channel_uuid = uuid4()

        query = clean_query("""
            INSERT INTO channels
                (channel_uuid,
                 owner_uuid,
                 name,
                 created_at,
                 updated_at)
            VALUES
                ($1, $2, $3, $4, $5)
            ON CONFLICT DO NOTHING 
            RETURNING channel_uuid;
        """)

        args = (channel.channel_uuid,
                channel.owner_uuid,
                channel.name,
                channel.created_at,
                channel.updated_at)

        result = await self._conn.fetchrow(query, *args)

        if not result:
            return None

        return result['channel_uuid']

    async def get_channel(self, uuid: UUID) -> Optional[Channel]:
        query = clean_query("""
            SELECT
                channel_uuid,
                owner_uuid,
                name,
                created_at,
                updated_at,
                deleted
            FROM channels
            WHERE channel_uuid = $1 and deleted = false;
        """)

        result = await self._conn.fetchrow(query, uuid)

        if not result:
            return None

        return Channel(
            channel_uuid=result['channel_uuid'],
            owner_uuid=result['owner_uuid'],
            name=result['name'],
            created_at=result['created_at'],
            updated_at=result['updated_at'],
            deleted=result['deleted']
        )

    async def get_channels(self, owner_uuid: Optional[UUID]) -> List[Channel]:
        query = clean_query("""
            SELECT
                channel_uuid,
                owner_uuid,
                name,
                created_at,
                updated_at,
                deleted
            FROM channels 
            WHERE owner_uuid = $1 and deleted = false;
        """)

        result = await self._conn.fetch(query, owner_uuid)

        if not result:
            return []

        return [
            Channel(
                channel_uuid=channel['channel_uuid'],
                owner_uuid=channel['owner_uuid'],
                name=channel['name'],
                created_at=channel['created_at'],
                updated_at=channel['updated_at'],
                deleted=channel['deleted']
            )
            for channel in result
        ]

    async def delete_channel(self, uuid: UUID) -> Optional[UUID]:
        query = clean_query("""
            UPDATE channels 
            SET
                deleted = true
            WHERE channel_uuid = $1 and deleted = false;
        """)

        result = await self._conn.execute(query, uuid)

        if not result:
            return None

        return uuid

    async def update_channel(self, channel: Channel) -> Optional[UUID]:
        query = clean_query("""
            UPDATE channels
            SET
                name = $1,
                updated_at = $2
            WHERE channel_uuid = $3 and deleted = false;
        """)

        args = (channel.name,
                channel.updated_at,
                channel.channel_uuid)

        result = await self._conn.execute(query, *args)

        if not result:
            return None

        return channel.channel_uuid
