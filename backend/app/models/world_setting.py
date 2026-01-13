from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class WorldSetting(Base):
    """
    世界观设定模型
    
    代表作品中的世界观设定，如地点、组织、规则等背景信息。
    """
    __tablename__ = "world_settings"
    
    # 基本信息字段
    id = Column(Integer, primary_key=True, autoincrement=True, doc="世界观设定唯一标识符")
    work_id = Column(Integer, ForeignKey("works.id"), nullable=False, doc="所属作品ID")
    name = Column(String(255), nullable=False, doc="世界观设定名称")
    description = Column(Text, doc="世界观设定描述")
    
    # 关系字段
    work = relationship("Work", back_populates="world_settings", doc="所属作品")