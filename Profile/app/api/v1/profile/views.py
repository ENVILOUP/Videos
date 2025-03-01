from typing import Annotated, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from asyncpg import Connection

from app.dependencies import JWTPayload, get_connection, get_uuid_from_token
from app.api.v1.profile.repositories import ProfileRepository, ChannelRepository
from app.models.channel import Channel
from app.models.user_profile import UserProfile
from app.api.v1.profile.schemas import (UserProfileCreationModel,
                                 UserProfileUpdateModel,
                                 ChannelCreationModel,
                                 ChannelUpdateModel,
                                 SuccessResponse)
from app.helpers.statuses import StatusCodes

router = APIRouter(
    prefix="/profiles"
)


@router.post(
    path="/", 
    response_model=SuccessResponse[UUID]
)
async def create_profile(profile_data: UserProfileCreationModel, db: Annotated[Connection, Depends(get_connection)], jwt_payload: Annotated[JWTPayload, Depends(get_uuid_from_token)]):
    async with db as conn:
            profile = UserProfile(name=profile_data.name,
                                user_uuid=jwt_payload.sub)
            uuid = await ProfileRepository.add_profile(conn, profile)

            return {
                "status_code": StatusCodes.OK,
                "data": uuid
            }


@router.get(
    path="/{profile_uuid}", 
    response_model=SuccessResponse[UserProfile]
)
async def get_profile(profile_uuid: UUID, db: Annotated[Connection, Depends(get_connection)]):
    async with db as conn:
        profile = await ProfileRepository.get_profile(conn, profile_uuid)
        return {
            "status_code": StatusCodes.OK,
            "data": profile
        }


@router.put(
    path="/{profile_uuid}",
    response_model=SuccessResponse[UUID]
)
async def update_profile(profile_uuid: UUID, profile_data: UserProfileUpdateModel, db: Annotated[Connection, Depends(get_connection)], jwt_payload: Annotated[JWTPayload, Depends(get_uuid_from_token)]):
    async with db as conn:
        profile = UserProfile(name=profile_data.name, user_uuid=jwt_payload.sub, profile_uuid=profile_uuid)
        uuid = await ProfileRepository.update_profile(conn, profile)
        return {
            "status_code": StatusCodes.OK,
            "data": uuid
        }


@router.delete(
    path="/{profile_uuid}",
    response_model=SuccessResponse[UUID]
)
async def delete_profile(profile_uuid: UUID, db: Annotated[Connection, Depends(get_connection)], jwt_payload: Annotated[JWTPayload, Depends(get_uuid_from_token)]):
    async with db as conn:
        if jwt_payload.role != "admin":
            raise HTTPException(status_code=401, detail="Unauthorized") 
        uuid = await ProfileRepository.delete_profile(conn, profile_uuid)
        return {
            "status_code": StatusCodes.OK,
            "data": uuid
        }


@router.post(
    path="/{owner_uuid}/channels",
    response_model=SuccessResponse[UUID]
)
async def create_channel(owner_uuid: UUID, channel_data: ChannelCreationModel, db: Annotated[Connection, Depends(get_connection)]):
    async with db as conn:
        channel = Channel(name=channel_data.name, owner_uuid=owner_uuid)
        uuid = await ChannelRepository.add_channel(conn, channel)
        return {
            "status_code": StatusCodes.OK,
            "data": uuid
        }


@router.get(
    path="/{owner_uuid}/channels/{channel_uuid}",
    response_model=SuccessResponse[Channel]
)
async def get_channel(channel_uuid: UUID, db: Annotated[Connection, Depends(get_connection)]):
    async with db as conn:
        channel = await ChannelRepository.get_channel(conn, channel_uuid)
        return {
            "status_code": StatusCodes.OK,
            "data": channel
        }


@router.get(
    path="/{owner_uuid}/channels",
    response_model=SuccessResponse[List[Channel]]
)
async def get_channels(owner_uuid: UUID, db: Annotated[Connection, Depends(get_connection)]):
    async with db as conn:
        channels = await ChannelRepository.get_channels(conn, owner_uuid)
        return {
            "status_code": StatusCodes.OK,
            "data": channels
        }


@router.put(
    path="/{owner_uuid}/channels/{channel_uuid}",
    response_model=SuccessResponse[UUID]
)
async def update_channel(channel_uuid: UUID, channel_data: ChannelUpdateModel, db: Annotated[Connection, Depends(get_connection)]):
    async with db as conn:
        channel = Channel(name=channel_data.name, channel_uuid=channel_uuid)
        uuid = await ChannelRepository.update_channel(conn, channel)
        return {
            "status_code": StatusCodes.OK,
            "data": uuid
        }


@router.delete(
    path="/{owner_uuid}/channels/{channel_uuid}",
    response_model=SuccessResponse[UUID]
)
async def delete_channel(channel_uuid: str, db: Annotated[Connection, Depends(get_connection)]):
    async with db as conn:
        uuid = await ChannelRepository.delete_channel(conn, channel_uuid)
        return {
            "status_code": StatusCodes.OK,
            "data": uuid
        }
