from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from .base import Base


class CreationLog(Base):
    """
    创作日志模型
    
    代表创作过程中的活动日志，用于记录创作历程。
    """
    __tablename__ = "creation_logs"
    
    # 基本信息字段
    id = Column(Integer, primary_key=True, autoincrement=True, doc="日志唯一标识符")
    work_id = Column(Integer, ForeignKey("works.id"), nullable=False, doc="所属作品ID")
    action_type = Column(String(50), nullable=False, doc="操作类型")
    description = Column(Text, doc="操作描述")
    
    # 时间戳字段
    created_at = Column(DateTime, default=func.current_timestamp(), doc="创建时间")
    
    # 关系字段
    work = relationship("Work", back_populates="creation_logs", doc="所属作品")