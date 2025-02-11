from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Request, HTTPException
from asyncpg import Connection

from app.dependencies import get_connection, get_uuid_from_token
from app.profile.repositories import ProfileRepository, ChannelRepository
from app.profile.models import UserProfile, Channel
from app.profile.schemas import (UserProfileCreationModel,
                                 UserProfileUpdateModel,
                                 ChannelCreationModel,
                                 ChannelUpdateModel)

router = APIRouter()


@router.post("/")
async def create_profile(profile_data: UserProfileCreationModel, db: Annotated[Connection, Depends(get_connection)], jwt_payload: Annotated[Request, Depends(get_uuid_from_token)]):
    async with db as conn:
            profile = UserProfile(name=profile_data.name,
                                user_uuid=jwt_payload.sub)
            uuid = await ProfileRepository.add_profile(conn, profile)

            return uuid


@router.get("/{profile_uuid}")
async def get_profile(profile_uuid: UUID, db: Annotated[Connection, Depends(get_connection)]):
    async with db as conn:
        profile = await ProfileRepository.get_profile(conn, profile_uuid)
        return profile


@router.put("/{profile_uuid}")
async def update_profile(profile_uuid: UUID, request: Request, profile_data: UserProfileUpdateModel, db: Annotated[Connection, Depends(get_connection)], jwt_payload: Annotated[Request, Depends(get_uuid_from_token)]):
    async with db as conn:
        profile = UserProfile(name=profile_data.name, user_uuid=jwt_payload.sub, profile_uuid=profile_uuid)
        uuid = await ProfileRepository.update_profile(conn, profile)
        return uuid


@router.delete("/{profile_uuid}")
async def delete_profile(profile_uuid: UUID, request: Request, db: Annotated[Connection, Depends(get_connection)], jwt_payload: Annotated[Request, Depends(get_uuid_from_token)]):
    async with db as conn:
        if jwt_payload.role != "admin":
            raise HTTPException(status_code=401, detail="Unauthorized") 
        uuid = await ProfileRepository.delete_profile(conn, profile_uuid)
        return uuid


@router.post("/{owner_uuid}/channels")
async def create_channel(owner_uuid: UUID, channel_data: ChannelCreationModel, db: Annotated[Connection, Depends(get_connection)]):
    async with db as conn:
        channel = Channel(name=channel_data.name, owner_uuid=owner_uuid)
        uuid = await ChannelRepository.add_channel(conn, channel)
        return uuid


@router.get("/{owner_uuid}/channels/{channel_uuid}")
async def get_channel(channel_uuid: UUID, db: Annotated[Connection, Depends(get_connection)]):
    async with db as conn:
        channel = await ChannelRepository.get_channel(conn, channel_uuid)
        return channel


@router.get("/{owner_uuid}/channels")
async def get_channels(owner_uuid: UUID, db: Annotated[Connection, Depends(get_connection)]):
    async with db as conn:
        channels = await ChannelRepository.get_channels(conn, owner_uuid)
        return channels


@router.put("/{owner_uuid}/channels/{channel_uuid}")
async def update_channel(channel_uuid: UUID, channel_data: ChannelUpdateModel, db: Annotated[Connection, Depends(get_connection)]):
    async with db as conn:
        channel = Channel(name=channel_data.name, channel_uuid=channel_uuid)
        uuid = await ChannelRepository.update_channel(conn, channel)
        return uuid


@router.delete("/{owner_uuid}/channels/{channel_uuid}")
async def delete_channel(channel_uuid: str, db: Annotated[Connection, Depends(get_connection)]):
    async with db as conn:
        uuid = await ChannelRepository.delete_channel(conn, channel_uuid)
        return uuid
