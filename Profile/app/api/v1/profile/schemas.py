from pydantic import BaseModel


class UserProfileCreationModel(BaseModel):
    name: str


class UserProfileUpdateModel(BaseModel):
    name: str


class ChannelCreationModel(BaseModel):
    name: str


class ChannelUpdateModel(BaseModel):
    name: str
