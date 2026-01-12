import os
from typing import Optional
from pydantic import BaseSettings


class Settings(BaseSettings):
    # 数据库配置
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./ai_writer.db")
    
    # API配置
    api_prefix: str = "/api/v1"
    
    # JWT配置
    secret_key: str = os.getenv("SECRET_KEY", "替换成你的强随机字符串")  # 更改这里的默认值
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # AI模型配置 - 改为智谱AI GLM-4.5
    zhipu_api_key: Optional[str] = os.getenv("ZHIPU_API_KEY")
    default_model: str = os.getenv("DEFAULT_MODEL", "glm-4.5")  # 改为智谱GLM-4.5
    
    class Config:
        env_file = ".env"


settings = Settings()