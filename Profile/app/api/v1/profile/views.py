from typing import Annotated, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from asyncpg import Connection

from app.dependencies.postgresql import database_сonnection
from app.dependencies.jwt import JWTPayload, get_uuid_from_token
from app.api.v1.profile.repositories import ProfileRepository, ChannelRepository
from app.models.channel import Channel
from app.models.user_profile import UserProfile
from app.api.v1.profile.schemas import (UserProfileCreationModel,
                                        UserProfileUpdateModel,
                                        ChannelCreationModel,
                                        ChannelUpdateModel
                                        )
from app.helpers.statuses import StatusCodes
from app.helpers.schemas import SuccessResponse

router = APIRouter(
    prefix="/profiles"
)


@router.post(
    path="/",
    response_model=SuccessResponse[UUID]
)
async def create_profile(profile_data: UserProfileCreationModel, db: Annotated[Connection, Depends(database_сonnection)], jwt_payload: Annotated[JWTPayload, Depends(get_uuid_from_token)]):
    profile = UserProfile(name=profile_data.name,
                          user_uuid=jwt_payload.sub)
    uuid = await ProfileRepository(db).add_profile(profile)

    return {
        "status_code": StatusCodes.OK,
        "data": uuid
    }


@router.get(
    path="/{profile_uuid}",
    response_model=SuccessResponse[UserProfile]
)
async def get_profile(profile_uuid: UUID, db: Annotated[Connection, Depends(database_сonnection)]):
    profile = await ProfileRepository(db).get_profile(profile_uuid)
    return {
        "status_code": StatusCodes.OK,
        "data": profile
    }


@router.put(
    path="/{profile_uuid}",
    response_model=SuccessResponse[UUID]
)
async def update_profile(profile_uuid: UUID, profile_data: UserProfileUpdateModel, db: Annotated[Connection, Depends(database_сonnection)], jwt_payload: Annotated[JWTPayload, Depends(get_uuid_from_token)]):
    profile = UserProfile(name=profile_data.name,
                          user_uuid=jwt_payload.sub, profile_uuid=profile_uuid)
    uuid = await ProfileRepository(db).update_profile(profile)
    return {
        "status_code": StatusCodes.OK,
        "data": uuid
    }


@router.delete(
    path="/{profile_uuid}",
    response_model=SuccessResponse[UUID]
)
async def delete_profile(profile_uuid: UUID, db: Annotated[Connection, Depends(database_сonnection)], jwt_payload: Annotated[JWTPayload, Depends(get_uuid_from_token)]):
    if jwt_payload.role != "admin":
        raise HTTPException(status_code=401, detail="Unauthorized")
    uuid = await ProfileRepository(db).delete_profile(profile_uuid)
    return {
        "status_code": StatusCodes.OK,
        "data": uuid
    }


@router.post(
    path="/{owner_uuid}/channels",
    response_model=SuccessResponse[UUID]
)
async def create_channel(owner_uuid: UUID, channel_data: ChannelCreationModel, db: Annotated[Connection, Depends(database_сonnection)]):
    channel = Channel(name=channel_data.name, owner_uuid=owner_uuid)
    uuid = await ChannelRepository(db).add_channel(channel)
    return {
        "status_code": StatusCodes.OK,
        "data": uuid
    }


@router.get(
    path="/{owner_uuid}/channels/{channel_uuid}",
    response_model=SuccessResponse[Channel]
)
async def get_channel(channel_uuid: UUID, db: Annotated[Connection, Depends(database_сonnection)]):
    channel = await ChannelRepository(db).get_channel(channel_uuid)
    return {
        "status_code": StatusCodes.OK,
        "data": channel
    }


@router.get(
    path="/{owner_uuid}/channels",
    response_model=SuccessResponse[List[Channel]]
)
async def get_channels(owner_uuid: UUID, db: Annotated[Connection, Depends(database_сonnection)]):
    channels = await ChannelRepository(db).get_channels(owner_uuid)
    return {
        "status_code": StatusCodes.OK,
        "data": [channel for channel in channels]
    }


@router.put(
    path="/{owner_uuid}/channels/{channel_uuid}",
    response_model=SuccessResponse[UUID]
)
async def update_channel(channel_uuid: UUID, channel_data: ChannelUpdateModel, db: Annotated[Connection, Depends(database_сonnection)]):
    channel = Channel(name=channel_data.name, channel_uuid=channel_uuid)
    uuid = await ChannelRepository(db).update_channel(channel)
    return {
        "status_code": StatusCodes.OK,
        "data": uuid
    }


@router.delete(
    path="/{owner_uuid}/channels/{channel_uuid}",
    response_model=SuccessResponse[UUID]
)
async def delete_channel(channel_uuid: str, db: Annotated[Connection, Depends(database_сonnection)]):
    uuid = await ChannelRepository(db).delete_channel(channel_uuid)
    return {
        "status_code": StatusCodes.OK,
        "data": uuid
    }
