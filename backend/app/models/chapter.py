from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey, JSON, func
from sqlalchemy.orm import relationship
from .base import Base


class Chapter(Base):
    """
    章节模型
    
    代表作品中的一个章节，包含章节标题、内容、位置信息以及情感分数、节奏指标等元数据。
    """
    __tablename__ = "chapters"
    
    # 基本信息字段
    id = Column(Integer, primary_key=True, autoincrement=True, doc="章节唯一标识符")
    work_id = Column(Integer, ForeignKey("works.id"), nullable=False, doc="所属作品ID")
    title = Column(String(255), nullable=False, doc="章节标题")
    content = Column(Text, nullable=False, doc="章节内容")
    position = Column(Integer, nullable=False, doc="章节在作品中的位置")
    
    # 分析相关字段
    compressed_summary = Column(Text, doc="章节内容的压缩摘要")
    emotion_score = Column(Float, doc="章节的情感分数")
    rhythm_metrics = Column(JSON, doc="章节的节奏指标，JSON格式存储")
    
    # 关系字段
    work = relationship("Work", back_populates="chapters", doc="所属作品")
    version_history = relationship("VersionHistory", back_populates="chapter", 
                                  cascade="all, delete-orphan", doc="章节的版本历史列表")
    annotations = relationship("Annotation", back_populates="chapter", 
                              cascade="all, delete-orphan", doc="章节的批注列表")