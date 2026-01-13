from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from .base import Base


class VersionHistory(Base):
    """
    版本历史模型
    
    代表作品或章节的版本历史，用于追踪内容的变化。
    """
    __tablename__ = "version_history"
    
    # 基本信息字段
    id = Column(Integer, primary_key=True, autoincrement=True, doc="版本历史唯一标识符")
    work_id = Column(Integer, ForeignKey("works.id"), nullable=False, doc="所属作品ID")
    chapter_id = Column(Integer, ForeignKey("chapters.id"), doc="所属章节ID（可选）")
    content = Column(Text, nullable=False, doc="版本内容")
    version_notes = Column(Text, doc="版本说明")
    
    # 时间戳字段
    created_at = Column(DateTime, default=func.current_timestamp(), doc="创建时间")
    
    # 关系字段
    work = relationship("Work", back_populates="version_history", doc="所属作品")
    chapter = relationship("Chapter", back_populates="version_history", doc="所属章节")