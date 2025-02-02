from fastapi import APIRouter

router = APIRouter()

@router.post("/")
def create_profile(name: str):
    return "Ok"

@router.get("/{profile_uuid}")
def get_profile(profile_uuid: str):
    return "Ok"

@router.put("/{profile_uuid}")
def update_profile(profile_uuid: str, name: str):
    return "Ok"

@router.delete("/{profile_uuid}")
def delete_profile(profile_uuid: str):
    return "Ok"