from fastapi import APIRouter, Depends
from app.profile.channel.repositories import ChannelRepository
from app.profile.channel.models import Channel

from typing import Annotated

from uuid import UUID

from app.dependencies import get_connection
from asyncpg import Connection

router = APIRouter()

@router.post("/")
async def create_channel(channel: Channel, db: Annotated[Connection, Depends(get_connection)]):
    async with db as conn:
        uuid = ChannelRepository.add_channel(conn, channel)
        return uuid 

@router.get("/{channel_uuid}")
async def get_channel(channel_uuid: str, db: Annotated[Connection, Depends(get_connection)]):
    async with db as conn:
        channel = ChannelRepository.get_channel(conn, channel_uuid)
        return channel

@router.get("/")
async def get_channels(owner_uuid: UUID, db: Annotated[Connection, Depends(get_connection)]):
    async with db as conn:
        channels = ChannelRepository.get_channels(conn, owner_uuid)
        return channels

@router.put("/{channel_uuid}")
async def update_channel(channel: Channel, db: Annotated[Connection, Depends(get_connection)]):
    async with db as conn:
        uuid = ChannelRepository.update_channel(conn, channel)
        return uuid


@router.delete("/{channel_uuid}")
async def delete_channel(channel_uuid: str, db: Annotated[Connection, Depends(get_connection)]):
    async with db as conn: 
        uuid = ChannelRepository.delete_channel(conn, channel_uuid)
        return uuid