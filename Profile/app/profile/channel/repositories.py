from uuid import UUID
from typing import Optional
from asyncpg import Connection
from app.profile.channel.models import Channel
from typing import List

class ChannelRepository:
    
    @staticmethod
    async def add_channel(conn: Connection, channel: Channel) -> Optional[UUID]:
        query = """
            INSERT INTO channel
                (channel_uuid,
                 owner_uuid,
                 name,
                 created,
                 updated)
            VALUES
                ($1, $2, $3, $4, $5)
            ON CONFLICT (channel_uuid) DO UPDATE SET
                owner_uuid = EXCLUDED.owner_uuid,
                name = EXCLUDED.name,
                updated = EXCLUDED.updated
            WHERE channel.channel_uuid = EXCLUDED.channel_uuid
            RETURNING channel_uuid;
        """

        args = (channel.channel_uuid,
                channel.owner_uuid,
                channel.name,
                channel.created,
                channel.updated)

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
                created,
                updated
            FROM channel
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
                created,
                updated
            FROM channel 
            WHERE owner_uuid = $1;
        """

        result = await conn.fetch(query, owner_uuid)

        if not result:
            return None

        return [Channel(**channel) for channel in result]
    
    @staticmethod
    async def delete_channel(conn: Connection, uuid: UUID) -> Optional[UUID]:
        query = """
            DELETE FROM channel
            WHERE channel_uuid = $1;
        """

        result = await conn.execute(query, uuid)
        
        if not result:
            return None

        return result.get('channel_uuid')
    
    @staticmethod
    async def update_channel(conn: Connection, channel: Channel) -> Optional[UUID]:
        query = """
            UPDATE channel
            SET
                name = $1,
                updated = $2
            WHERE channel_uuid = $3;
        """

        args = (channel.name,
                channel.updated,
                channel.channel_uuid)

        result = await conn.execute(query, *args)

        if not result:
            return None

        return result.get('channel_uuid')