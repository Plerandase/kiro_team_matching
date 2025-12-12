"""
Chat and communication router for team collaboration
"""
import json
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_
from ..core.database import get_db
from ..core.deps import get_current_active_user
from ..models.user import User
from ..models.project import Project
from ..models.application import TeamMember
from ..models.chat import ChatRoom, ChatMessage, MeetingNote
from ..schemas.chat import (
    ChatRoomCreate, ChatRoomResponse, MessageCreate, MessageResponse, 
    MessageListResponse, MeetingSummaryRequest, MeetingSummaryResponse
)

router = APIRouter()


def check_project_access(project_id: str, user: User, db: Session) -> Project:
    """Check if user has access to project (is leader or team member)"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Check if user is leader
    if str(project.leader_id) == str(user.id):
        return project
    
    # Check if user is team member
    team_member = db.query(TeamMember).filter(
        and_(
            TeamMember.project_id == project_id,
            TeamMember.user_id == user.id,
            TeamMember.left_at.is_(None)
        )
    ).first()
    
    if not team_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. You are not a member of this project."
        )
    
    return project


@router.post("/projects/{project_id}/chatrooms", response_model=ChatRoomResponse)
async def create_chat_room(
    project_id: str,
    room_data: ChatRoomCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create a new chat room for a project (team members only)
    """
    project = check_project_access(project_id, current_user, db)
    
    # Check if room with same name already exists
    existing_room = db.query(ChatRoom).filter(
        and_(
            ChatRoom.project_id == project_id,
            ChatRoom.name == room_data.name
        )
    ).first()
    
    if existing_room:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chat room with this name already exists"
        )
    
    # Create chat room
    db_room = ChatRoom(
        project_id=project_id,
        name=room_data.name
    )
    
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    
    return ChatRoomResponse(
        id=str(db_room.id),
        project_id=str(db_room.project_id),
        name=db_room.name,
        created_at=db_room.created_at
    )


@router.get("/projects/{project_id}/chatrooms", response_model=List[ChatRoomResponse])
async def get_project_chat_rooms(
    project_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get all chat rooms for a project (team members only)
    """
    project = check_project_access(project_id, current_user, db)
    
    rooms = db.query(ChatRoom).filter(ChatRoom.project_id == project_id).all()
    
    return [
        ChatRoomResponse(
            id=str(room.id),
            project_id=str(room.project_id),
            name=room.name,
            created_at=room.created_at
        )
        for room in rooms
    ]


@router.get("/chatrooms/{room_id}/messages", response_model=MessageListResponse)
async def get_chat_messages(
    room_id: str,
    page: int = Query(1, ge=1),
    size: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get messages from a chat room with pagination (team members only)
    """
    # Get chat room and verify access
    room = db.query(ChatRoom).filter(ChatRoom.id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat room not found"
        )
    
    # Check project access
    check_project_access(str(room.project_id), current_user, db)
    
    # Get messages with pagination (newest first)
    query = db.query(ChatMessage).filter(ChatMessage.room_id == room_id)
    total = query.count()
    
    offset = (page - 1) * size
    messages = query.order_by(ChatMessage.created_at.desc()).offset(offset).limit(size).all()
    
    # Reverse to show oldest first in the page
    messages.reverse()
    
    return MessageListResponse(
        messages=[
            MessageResponse(
                id=str(msg.id),
                room_id=str(msg.room_id),
                sender_id=str(msg.sender_id),
                content=msg.content,
                message_type=msg.message_type,
                created_at=msg.created_at
            )
            for msg in messages
        ],
        total=total,
        page=page,
        size=size
    )


@router.post("/chatrooms/{room_id}/messages", response_model=MessageResponse)
async def send_message(
    room_id: str,
    message_data: MessageCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Send a message to a chat room (team members only)
    """
    # Get chat room and verify access
    room = db.query(ChatRoom).filter(ChatRoom.id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat room not found"
        )
    
    # Check project access
    check_project_access(str(room.project_id), current_user, db)
    
    # Create message
    db_message = ChatMessage(
        room_id=room_id,
        sender_id=current_user.id,
        content=message_data.content,
        message_type=message_data.message_type
    )
    
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    
    return MessageResponse(
        id=str(db_message.id),
        room_id=str(db_message.room_id),
        sender_id=str(db_message.sender_id),
        content=db_message.content,
        message_type=db_message.message_type,
        created_at=db_message.created_at
    )


@router.post("/projects/{project_id}/meeting-notes/ai-summarize", response_model=MeetingSummaryResponse)
async def create_meeting_summary(
    project_id: str,
    summary_request: MeetingSummaryRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create AI-powered meeting summary (team members only)
    """
    project = check_project_access(project_id, current_user, db)
    
    # TODO: Integrate with AI service for actual summarization
    # For now, create a simple summary
    summary_text = f"Meeting summary for: {summary_request.raw_text[:100]}..."
    action_items = ["Review project progress", "Assign new tasks", "Schedule next meeting"]
    next_agenda = "Discuss implementation details" if summary_request.include_next_agenda else None
    
    # Create meeting note
    db_note = MeetingNote(
        project_id=project_id,
        raw_text=summary_request.raw_text,
        summary_ai=summary_text,
        action_items_ai=json.dumps(action_items) if summary_request.include_actions else None,
        next_meeting_agenda=next_agenda,
        created_by=current_user.id
    )
    
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    
    return MeetingSummaryResponse(
        id=str(db_note.id),
        project_id=str(db_note.project_id),
        summary_ai=db_note.summary_ai,
        action_items_ai=json.loads(db_note.action_items_ai) if db_note.action_items_ai else None,
        next_meeting_agenda=db_note.next_meeting_agenda,
        created_at=db_note.created_at
    )


@router.get("/projects/{project_id}/meeting-notes", response_model=List[MeetingSummaryResponse])
async def get_meeting_notes(
    project_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get all meeting notes for a project (team members only)
    """
    project = check_project_access(project_id, current_user, db)
    
    notes = db.query(MeetingNote).filter(
        MeetingNote.project_id == project_id
    ).order_by(MeetingNote.created_at.desc()).all()
    
    return [
        MeetingSummaryResponse(
            id=str(note.id),
            project_id=str(note.project_id),
            summary_ai=note.summary_ai,
            action_items_ai=json.loads(note.action_items_ai) if note.action_items_ai else None,
            next_meeting_agenda=note.next_meeting_agenda,
            created_at=note.created_at
        )
        for note in notes
    ]