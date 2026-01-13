from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Character(Base):
    """
    角色设定模型
    
    代表作品中的一个角色，包含角色名称、描述和特征等信息。
    """
    __tablename__ = "characters"
    
    # 基本信息字段
    id = Column(Integer, primary_key=True, autoincrement=True, doc="角色唯一标识符")
    work_id = Column(Integer, ForeignKey("works.id"), nullable=False, doc="所属作品ID")
    name = Column(String(255), nullable=False, doc="角色姓名")
    description = Column(Text, doc="角色描述")
    traits = Column(Text, doc="角色特征")
    
    # 关系字段
    work = relationship("Work", back_populates="characters", doc="所属作品")