from fastapi import APIRouter

router = APIRouter()

@router.post("/")
def create_channel(name: str):
    return "Ok"

@router.get("/{channel_uuid}")
def get_channel(channel_uuid: str):
    return "Ok"

@router.get("/")
def get_channels():
    return "Ok"

@router.put("/{channel_uuid}")
def update_channel(channel_uuid: str, name: str):
    return "Ok"

@router.delete("/{channel_uuid}")
def delete_channel(channel_uuid: str):
    return "Ok"