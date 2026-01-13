from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from .base import Base


class Annotation(Base):
    """
    批注模型
    
    代表对作品或章节内容的批注信息。
    """
    __tablename__ = "annotations"
    
    # 基本信息字段
    id = Column(Integer, primary_key=True, autoincrement=True, doc="批注唯一标识符")
    work_id = Column(Integer, ForeignKey("works.id"), nullable=False, doc="所属作品ID")
    chapter_id = Column(Integer, ForeignKey("chapters.id"), nullable=False, doc="所属章节ID")
    content_position = Column(Integer, nullable=False, doc="批注在内容中的位置")
    annotation_text = Column(Text, nullable=False, doc="批注文本")
    
    # 时间戳字段
    created_at = Column(DateTime, default=func.current_timestamp(), doc="创建时间")
    
    # 关系字段
    work = relationship("Work", back_populates="annotations", doc="所属作品")
    chapter = relationship("Chapter", back_populates="annotations", doc="所属章节")