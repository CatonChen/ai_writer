from sqlalchemy import Column, Integer, JSON, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from .base import Base


class SessionState(Base):
    """
    会话状态模型
    
    代表用户在创作过程中的会话状态，用于恢复用户的创作进度。
    """
    __tablename__ = "session_states"
    
    # 基本信息字段
    id = Column(Integer, primary_key=True, autoincrement=True, doc="会话状态唯一标识符")
    work_id = Column(Integer, ForeignKey("works.id"), nullable=False, doc="所属作品ID")
    user_id = Column(Integer, doc="用户ID")
    session_data = Column(JSON, nullable=False, doc="会话数据，JSON格式存储")
    
    # 时间戳字段
    last_accessed = Column(DateTime, default=func.current_timestamp(), 
                          onupdate=func.current_timestamp(), doc="最后访问时间")
    
    # 关系字段
    work = relationship("Work", back_populates="session_states", doc="所属作品")