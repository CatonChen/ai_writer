from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 添加CORS中间件，允许Tauri前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:1420", 
        "tauri://localhost", 
        "https://tauri.localhost",
        "http://127.0.0.1:8000",  # 添加后端地址本身
        "*"  # 开发期间临时允许所有来源，生产环境应限制
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World", "Service": "AI Writer Backend"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "AI Writer Backend"}