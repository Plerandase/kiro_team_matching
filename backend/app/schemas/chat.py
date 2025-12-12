"""
Chat and communication schemas
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel
from ..models.chat import MessageType


class ChatRoomBase(BaseModel):
    name: str


class ChatRoomCreate(ChatRoomBase):
    pass


class ChatRoomResponse(ChatRoomBase):
    id: str
    project_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class MessageBase(BaseModel):
    content: str
    message_type: MessageType = MessageType.TEXT


class MessageCreate(MessageBase):
    pass


class MessageResponse(MessageBase):
    id: str
    room_id: str
    sender_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class MessageListResponse(BaseModel):
    messages: List[MessageResponse]
    total: int
    page: int
    size: int


class MeetingSummaryRequest(BaseModel):
    raw_text: str
    include_actions: bool = True
    include_next_agenda: bool = False


class MeetingSummaryResponse(BaseModel):
    id: str
    project_id: str
    summary_ai: str
    action_items_ai: Optional[List[str]] = None
    next_meeting_agenda: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True