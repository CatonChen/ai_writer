from sqlalchemy import Column, Integer, Text, String, DateTime, func
from .base import Base


class FeedbackRecord(Base):
    """
    反馈记录模型
    
    代表用户对AI生成内容的反馈，用于改进AI模型。
    """
    __tablename__ = "feedback_records"
    
    # 基本信息字段
    id = Column(Integer, primary_key=True, autoincrement=True, doc="反馈记录唯一标识符")
    original_content = Column(Text, nullable=False, doc="原始AI生成内容")
    modified_content = Column(Text, nullable=False, doc="用户修改后的内容")
    feedback_type = Column(String(50), nullable=False, doc="反馈类型")
    
    # 时间戳字段
    created_at = Column(DateTime, default=func.current_timestamp(), doc="创建时间")