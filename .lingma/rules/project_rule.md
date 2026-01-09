# AI写作工具项目开发规范

## 项目概述

本规范适用于AI写作工具项目的开发，项目采用Tauri + Python(FastAPI) + React的技术栈，旨在构建一个功能完整、可扩展的智能写作助手。所有参与项目的开发者必须遵循此规范。

本规范遵循PEP8规范，应用DRY/KISS/YAGNI原则，并结合OWASP安全最佳实践。开发过程将采用分步式开发方法，将任务拆解为最小单元。

---

## 技术栈规范
### 框架与工具
1. 核心框架：FastAPI 0.104+（高性能API场景）
2. 依赖管理：使用Poetry进行环境管理
3. ORM：SQLAlchemy 2.0+（桌面应用使用SQLite）
4. 测试框架：pytest
5. AI框架：LangGraph + LangChain
6. 桌面框架：Tauri（Rust + Web技术）
7. 前端框架：React 18+ + TypeScript
8. 数据库：SQLite（桌面应用），支持PostgreSQL扩展

---

## 代码结构规范
### 项目目录结构
```markdown
ai_writer/ 
├── backend/ # 后端代码 
│ ├── app/ # FastAPI应用主目录 
│ │ ├── api/ # API路由定义 
│ │ │ ├── v1/ # API版本1 
│ │ │ │ ├── routes/ # 路由文件 
│ │ │ │ └── init.py 
│ │ ├── models/ # SQLAlchemy数据模型 
│ │ ├── schemas/ # Pydantic数据模式 
│ │ ├── database/ # 数据库连接和会话管理 
│ │ ├── core/ # 核心配置（安全、设置等） 
│ │ ├── utils/ # 工具函数 
│ │ ├── ai/ # AI相关模块 
│ │ │ ├── generators/ # 内容生成器 
│ │ │ ├── templates/ # 模板管理 
│ │ │ ├── context/ # 上下文处理 
│ │ │ ├── analysis/ # 文本分析 
│ │ │ └── feedback/ # 用户反馈学习 
│ │ └── main.py # 应用入口 
│ ├── pyproject.toml # Poetry依赖管理 
│ └── tests/ # 测试文件 
├── frontend/ # 前端代码(Tauri) 
│ ├── src/ # React源代码 
│ │ ├── components/ # React组件 
│ │ ├── pages/ # 页面组件 
│ │ ├── hooks/ # 自定义hooks 
│ │ ├── types/ # TypeScript类型定义 
│ │ ├── services/ # API服务 
│ │ └── utils/ # 前端工具函数 
│ ├── src-tauri/ # Tauri后端代码 
│ ├── public/ # 静态资源 
│ ├── package.json # Node.js依赖 
│ └── tauri.conf.json # Tauri配置 
├── docs/ # 文档 
├── scripts/ # 构建和部署脚本 
└── README.md # 项目说明
```

---

### 代码风格
1. **命名规范**：
   - 类名：PascalCase（如`ContentGenerator`）
   - 函数/方法：snake_case（如`generate_content`）
   - 常量：UPPER_SNAKE_CASE（如`MAX_CONTENT_LENGTH`）
   - 前端组件：PascalCase（如`WorkEditor`）
   - 前端变量/函数：camelCase（如`handleSave`）
2. **缩进**：4个空格，禁止使用Tab
3. **文件长度**：Python单文件不超过500行，复杂类拆分为多个模块
4. **注释**：所有公共方法必须有类型注解和docstring

---

### 数据库规范

#### 模型设计
1. **SQLAlchemy模型**：
   ```python
   from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
   from sqlalchemy.orm import declarative_base, relationship
   from datetime import datetime

   Base = declarative_base()

   class Work(Base):
       __tablename__ = 'works'
       id = Column(Integer, primary_key=True, index=True)
       title = Column(String(255), nullable=False)
       description = Column(Text)
       created_at = Column(DateTime, default=datetime.utcnow)
       updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
       
       chapters = relationship("Chapter", back_populates="work")
    ```
2. **Django ORM模型（如果项目使用Django）**：
    ```python
    from django.db import models

    class Work(models.Model):
        title = models.CharField(max_length=255)
        description = models.TextField()
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)
        
        class Meta:
            indexes = [models.Index(fields=['title'])]
    ```
3. **表命名规范**：
- 使用复数形式表示集合（如works, chapters）
- 使用小写字母和下划线分隔单词（snake_case）
- 避免使用保留字作为表名
4. **字段命名规范**：
- 使用有意义的名称（如created_at而不是ctime）
- 保持一致性（如统一使用_at后缀表示时间字段）

#### 查询规范
1. 禁止直接拼接SQL字符串，必须使用ORM查询
2. 复杂查询需使用适当的加载策略预加载关联对象
3. 分页查询必须包含offset和limit参数
4. 使用连接池管理数据库连接
---

## API开发规范
### 接口设计
1. **RESTful规范**：
   - 资源路径：`/api/v1/works/{id}`
   - HTTP方法：GET/POST/PUT/PATCH/DELETE
   - 响应格式：JSON（后端使用snake_case字段名，前端转换为camelCase）

2. **FastAPI示例**：
    ```python
    from fastapi import APIRouter, Depends, HTTPException
    from pydantic import BaseModel
    from typing import Optional

    router = APIRouter(prefix="/works", tags=["works"])

    class WorkCreate(BaseModel):
        title: str
        description: Optional[str] = None

    @router.post("/", status_code=201)
    def create_work(work: WorkCreate, db: Session = Depends(get_db)):
        # 业务逻辑
        return {"message": "Work created", "id": 1}
    ```

### 错误处理
1. 统一使用HTTP状态码：
- 400：客户端错误（参数校验失败）
- 401：未认证
- 403：权限不足
- 404：资源不存在
- 500：服务器内部错误

2. **全局异常捕获**：
    ```python
    from fastapi import FastAPI, Request
    from fastapi.exceptions import RequestValidationError
    from fastapi.responses import JSONResponse

    app = FastAPI()

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        return JSONResponse(
            status_code=422,
            content={"detail": exc.errors()}
        )
    ```

---

## AI模块开发规范
### LangGraph/LangChain集成
1. 定义清晰的AI节点和边关系
2. 使用类型提示明确输入输出
3. 为AI调用添加适当的重试机制
4. 记录AI调用的输入输出用于调试和学习

### AI模型管理
1. 支持多种模型提供商的抽象层
2. 实现模型配置的动态切换
3. 对敏感信息进行加密处理
4. 本地模型与云端模型的无缝切换

---

## 测试规范
### 单元测试
1. **pytest结构**：
    ```python
    # tests/test_content_generator.py
    import pytest
    from app.ai.generators import ContentGenerator

    @pytest.mark.asyncio
    async def test_generate_content():
        generator = ContentGenerator()
        result = await generator.generate("test outline", "test context", "test template")
        assert isinstance(result, str)
    ```

2. 覆盖率要求：核心模块≥80%，AI模块≥70%

### 集成测试
1. 测试API端点的完整功能
2. 验证数据库操作正确性
3. 测试AI功能的基本可用性

---

## 安全规范
1. **输入校验**：
- 所有用户输入必须通过Pydantic模型校验
- 敏感字段（如API密钥）使用`SecretStr`类型
2. **数据保护**：
- 本地数据加密存储
- API密钥安全存储机制
- 用户隐私保护措施
3. **注入防护**：
- 禁止使用原始SQL查询
- 复杂查询必须通过参数化语句

---

## 部署规范
### 环境管理
1. 使用Tauri CLI工具进行桌面应用打包
2. 支持Windows、macOS和Linux平台
3. 环境变量管理：通过`python-dotenv`加载
4. 日志规范：
- 使用标准logging模块
- 格式：`%(asctime)s [%(levelname)s] %(name)s: %(message)s`
- 级别：生产环境设为WARNING，开发环境设为DEBUG

---

## 版本控制规范
1. Git提交规范：
- 类型：feat/fix/chore/docs/style/refactor/perf/test
- 格式：`<type>(<scope>): <subject>`
- 示例：`feat(ai_generator): add content generation with style templates`
2. 必须通过PR进行代码审查
3. 主分支禁止直接提交，必须通过CI/CD流水线

---

## 性能优化规范
1. **数据库优化**：
- 复杂查询必须添加索引
- 使用适当的查询分析工具
2. **AI处理优化**：
- 缓存AI生成结果减少重复计算
- 实现异步处理长时间运行的AI任务
3. **缓存策略**：
- 使用内存缓存高频访问的数据
- 缓存键命名规范：`{module}:{id}:{field}`

---

## 文档规范
1. 使用Sphinx生成Python API文档
2. 所有公共API必须包含OpenAPI文档
3. 重大变更需更新CHANGELOG.md
4. 提供详细的用户使用文档

---

## 代码审查规范
1. 每个PR必须至少1人审查
2. 代码复杂度（Cyclomatic）≤10
3. 方法行数≤50行，类行数≤200行
4. 审查重点：代码规范、安全问题、性能问题、测试覆盖

---

## 项目初始化规范
### 环境准备
1. **Python环境**：
   - 使用Python 3.10+版本
   - 推荐使用pyenv管理Python版本
   - 使用Poetry管理依赖

2. **开发环境设置**：
   ```bash
   # 安装依赖
   poetry install
   
   # 激活虚拟环境
   poetry shell
   
   # 运行测试
   poetry run pytest
   ```
### 开发流程
1. **分支策略**：
   - 主分支：main（受保护）
   - 功能分支：feature/功能名
   - 修复分支：fix/问题描述
   - 发布分支：release/版本号

---

## 代码质量规范
### 代码检查工具
1. **静态分析**：
   - 使用mypy进行类型检查
   - 使用flake8进行代码风格检查
   - 使用bandit进行安全扫描

2. **格式化工具**：
   - 使用black格式化Python代码
   - 使用isort整理import语句

### CI/CD配置
1. **自动化测试**：
   - 提交代码时自动运行单元测试
   - 代码覆盖率检查
   - 代码质量扫描

---

## 前端开发规范（补充）
### React组件开发
1. **组件结构**：
   - 使用函数组件配合Hooks
   - 组件单一职责原则
   - 合理使用TypeScript类型定义

2. **状态管理**：
   - 简单状态：useState, useReducer
   - 全局状态：根据项目规模选择Context API或Redux Toolkit

### 性能优化
1. **组件优化**：
   - 使用React.memo避免不必要的重渲染
   - 使用useCallback/useMemo优化性能
   - 懒加载非关键组件