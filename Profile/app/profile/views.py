from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Request, HTTPException
from asyncpg import Connection
import jwt

from app.dependencies import get_connection
from app.profile.repositories import ProfileRepository, ChannelRepository
from app.profile.models import UserProfile, Channel
from app.profile.schemas import (UserProfileCreationModel,
                                 UserProfileUpdateModel,
                                 ChannelCreationModel,
                                 ChannelUpdateModel)

router = APIRouter()


@router.post("/")
async def create_profile(profile_data: UserProfileCreationModel, request: Request, db: Annotated[Connection, Depends(get_connection)]):
    async with db as conn:
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            raise HTTPException(
                status_code=401, detail="Authorization header is missing")

        if not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=401, detail="Invalid authorization scheme")

        token = auth_header.split("Bearer ")[1]

        SECRET_KEY = "18Z0Vmuq5j99VY0X1xkIVlZ499t3SqHha7siBG29tnb4WAuR"

        decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"], options={
                                     "verify_exp": False, "verify_aud": False})

        profile = UserProfile(name=profile_data.name,
                              user_uuid=decoded_payload['sub'])
        uuid = await ProfileRepository.add_profile(conn, profile)
        return uuid


@router.get("/{profile_uuid}")
async def get_profile(profile_uuid: UUID, db: Annotated[Connection, Depends(get_connection)]):
    async with db as conn:
        profile = await ProfileRepository.get_profile(conn, profile_uuid)
        return profile


@router.put("/{profile_uuid}")
async def update_profile(profile_data: UserProfileUpdateModel, db: Annotated[Connection, Depends(get_connection)]):
    async with db as conn:
        profile = UserProfile(name=profile_data.name)
        uuid = await ProfileRepository.update_profile(conn, profile)
        return uuid


@router.delete("/{profile_uuid}")
async def delete_profile(profile_uuid: UUID, db: Annotated[Connection, Depends(get_connection)]):
    async with db as conn:
        uuid = await ProfileRepository.delete_profile(conn, profile_uuid)
        return uuid


@router.post("/{profile_uuid}/channel")
async def create_channel(channel_data: ChannelCreationModel, db: Annotated[Connection, Depends(get_connection)]):
    async with db as conn:
        channel = Channel(name=channel_data.name)
        uuid = await ChannelRepository.add_channel(conn, channel)
        return uuid


@router.get("/profile/{profile_uuid}/channel/{channel_uuid}")
async def get_channel(channel_uuid: str, db: Annotated[Connection, Depends(get_connection)]):
    async with db as conn:
        channel = await ChannelRepository.get_channel(conn, channel_uuid)
        return channel


@router.get("/{owner_uuid}/channel")
async def get_channels(owner_uuid: UUID, db: Annotated[Connection, Depends(get_connection)]):
    async with db as conn:
        channels = await ChannelRepository.get_channels(conn, owner_uuid)
        return channels


@router.put("/{channel_uuid}")
async def update_channel(channel_data: ChannelUpdateModel, db: Annotated[Connection, Depends(get_connection)]):
    async with db as conn:
        channel = Channel(name=channel_data.name)
        uuid = await ChannelRepository.update_channel(conn, channel)
        return uuid


@router.delete("/{channel_uuid}")
async def delete_channel(channel_uuid: str, db: Annotated[Connection, Depends(get_connection)]):
    async with db as conn:
        uuid = await ChannelRepository.delete_channel(conn, channel_uuid)
        return uuid
