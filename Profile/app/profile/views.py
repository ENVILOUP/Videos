from fastapi import APIRouter, Depends
from app.profile.repositories import ProfileRepository
from app.profile.models import UserProfile

from typing import Annotated

from asyncpg import Connection
from app.dependencies import get_connection

router = APIRouter()

@router.post("/")
async def create_profile(profile: UserProfile, db: Annotated[Connection, Depends(get_connection)]):
    async with db as conn:
        uuid = ProfileRepository.add_profile(conn, profile)
        return uuid

@router.get("/{profile_uuid}")
async def get_profile(profile_uuid: str, db: Annotated[Connection, Depends(get_connection)]):
    async with db as conn:
        profile = ProfileRepository.get_profile(conn, profile_uuid)
        return profile

@router.put("/{profile_uuid}")
async def update_profile(profile: UserProfile, db: Annotated[Connection, Depends(get_connection)]):
    async with db as conn:
        uuid = ProfileRepository.update_profile(conn, profile)
        return uuid

@router.delete("/{profile_uuid}")
async def delete_profile(profile_uuid: str, db: Annotated[Connection, Depends(get_connection)]):
    async with db as conn:
        uuid = ProfileRepository.delete_profile(conn, profile_uuid)
        return uuid