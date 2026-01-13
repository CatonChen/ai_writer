from sqlalchemy import Column, Integer, String, Text, DateTime, func
from .base import Base


class Template(Base):
    """
    模板模型
    
    代表提示词模板，用于AI内容生成的引导。
    """
    __tablename__ = "templates"
    
    # 基本信息字段
    id = Column(Integer, primary_key=True, autoincrement=True, doc="模板唯一标识符")
    name = Column(String(255), nullable=False, doc="模板名称")
    content = Column(Text, nullable=False, doc="模板内容")
    template_type = Column(String(50), nullable=False, doc="模板类型")
    
    # 时间戳字段
    created_at = Column(DateTime, default=func.current_timestamp(), doc="创建时间")