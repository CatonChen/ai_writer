from sqlalchemy import Column, Integer, String, Text, DateTime, func
from sqlalchemy.orm import relationship
from .base import Base


class Work(Base):
    """
    作品模型
    
    代表一个完整的写作项目，如一本书、一篇文章或其他类型的创作作品。
    一个作品可以包含多个章节、角色设定、世界观设定等内容。
    """
    __tablename__ = "works"
    
    # 基本信息字段
    id = Column(Integer, primary_key=True, autoincrement=True, doc="作品唯一标识符")
    title = Column(String(255), nullable=False, doc="作品标题")
    description = Column(Text, doc="作品描述")
    
    # 时间戳字段
    created_at = Column(DateTime, default=func.current_timestamp(), doc="创建时间")
    updated_at = Column(
        DateTime, 
        default=func.current_timestamp(), 
        onupdate=func.current_timestamp(), 
        doc="最后更新时间"
    )
    
    # 关系字段 - 一个作品可以包含多个章节、角色等
    chapters = relationship("Chapter", back_populates="work", cascade="all, delete-orphan", 
                           doc="作品的章节列表")
    characters = relationship("Character", back_populates="work", cascade="all, delete-orphan",
                             doc="作品的角色设定列表")
    world_settings = relationship("WorldSetting", back_populates="work", cascade="all, delete-orphan",
                                 doc="作品的世界观设定列表")
    session_states = relationship("SessionState", back_populates="work", cascade="all, delete-orphan",
                                 doc="作品的会话状态列表")
    version_history = relationship("VersionHistory", back_populates="work", cascade="all, delete-orphan",
                                  doc="作品的版本历史列表")
    annotations = relationship("Annotation", back_populates="work", cascade="all, delete-orphan",
                              doc="作品的批注列表")
    creation_logs = relationship("CreationLog", back_populates="work", cascade="all, delete-orphan",
                                doc="作品的创作日志列表")