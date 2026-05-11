# 智扫通机器人智能客服系统

## 📖 项目概述

智扫通机器人智能客服系统是一个基于 **AI + RAG (检索增强生成)** 技术的智能客服解决方案。该系统结合 FastAPI 后端和 Vue3 前端，为用户提供智能对话、知识库检索、文件管理等功能，实现高效的客户服务自动化。

### 核心特性

- 🤖 **智能对话引擎**：基于 React Agent 和 LLM 的智能对话系统
- 📚 **RAG 知识库**：集成 Milvus 向量数据库，支持向量化检索和重排
- 📁 **文件管理**：支持文档上传、处理和知识库导入
- 👤 **用户认证**：JWT 密钥认证和用户权限管理
- ⚡ **异步处理**：使用 RabbitMQ 消息队列实现异步任务处理
- 🔒 **数据持久化**：MySQL 数据库存储用户和聊天记录
- 💬 **流式响应**：支持 Server-Sent Events (SSE) 实时流式输出
- 🎨 **现代化前端**：Vue3 + Element Plus + Tailwind CSS 构建的美观界面

---

## 📂 项目结构

### 后端项目 (`zhisaotong-agent`)

```
zhisaotong-agent/
├── main.py                          # FastAPI 应用主入口
├── requirements.txt                 # Python 核心依赖清单
├── agent/
│   ├── react_agent.py              # React Agent 智能对话引擎
│   ├── middleware/
│   │   └── middleware.py           # Agent 中间件（日志、监控、工具管理）
│   └── tools/
│       └── agent_tools.py          # Agent 工具定义（天气、地址、数据获取等）
├── cache/
│   └── users_cache.py              # 用户缓存管理
├── config/                          # 配置文件目录
│   ├── agent.yml                   # Agent 配置（LLM 模型）
│   ├── jwt.yml                     # JWT 认证配置
│   ├── milvus.yml                  # 向量数据库配置
│   ├── mysql.yml                   # MySQL 数据库配置
│   ├── path.yml                    # 路径配置
│   ├── prompt.yml                  # 提示词配置
│   ├── rabbitmq.yml                # 消息队列配置
│   ├── rag.yml                     # RAG 配置（LLM 和嵌入模型）
│   └── redis.yml                   # Redis 配置
├── crud/                            # 数据库操作层
│   ├── chat.py                     # 聊天记录操作
│   ├── files.py                    # 文件操作
│   └── users.py                    # 用户操作
├── data/                            # 知识库数据
│   ├── 故障排除.txt
│   ├── 扫地机器人100问2.txt
│   ├── 扫拖一体机器人100问.txt
│   ├── 维护保养.txt
│   ├── 选购指南.txt
│   └── external/
│       └── records.csv             # 外部数据源
├── logs/                            # 日志文件存储目录
├── models/                          # 数据模型定义
│   ├── base.py                     # 基础模型
│   ├── chat_history.py             # 聊天历史数据模型
│   ├── factory.py                  # 模型工厂（LLM 初始化）
│   ├── files.py                    # 文件数据模型
│   ├── user_token.py               # Token 数据模型
│   └── users.py                    # 用户数据模型
├── mysql_db/
│   └── db_service.py               # MySQL 数据库服务
├── prompts/                         # 系统提示词
│   ├── main_prompt.txt             # 主对话提示词
│   ├── rag_summarize.txt           # RAG 总结提示词
│   └── report_prompt.txt           # 报告生成提示词
├── rabbitmq/
│   └── rabbitmq_service.py         # RabbitMQ 消息队列服务
├── rag/                             # RAG 核心模块
│   ├── rag_service.py              # RAG 服务主类
│   ├── embed/
│   │   └── embedding_service.py    # 文本嵌入服务
│   ├── milvus/
│   │   └── milvus_service.py       # Milvus 向量数据库服务
│   └── rerank/
│       └── bm25_service.py         # BM25 重排服务
├── reids_db/
│   └── redis_service.py            # Redis 缓存服务
├── routers/                         # API 路由定义
│   ├── chat.py                     # 聊天 API 端点
│   ├── files.py                    # 文件管理 API 端点
│   └── users.py                    # 用户管理 API 端点
├── schemas/                         # 请求/响应数据结构
│   ├── chat.py
│   ├── files.py
│   ├── token.py
│   └── users.py
├── tasks/
│   └── mq_consumer.py              # 消息队列消费者（异步任务处理）
├── uploads/                         # 文件上传目录
│   └── user-1/
├── utils/                           # 工具函数库
│   ├── auth.py                     # 认证工具
│   ├── clean_text.py               # 文本清理
│   ├── config_handler.py           # 配置处理
│   ├── db_transaction.py           # 数据库事务管理
│   ├── exception_handlers.py       # 异常处理
│   ├── exception.py                # 自定义异常
│   ├── file_handler.py             # 文件处理
│   ├── import_local_knowledge_on_startup.py  # 启动时导入本地知识库
│   ├── jwt.py                      # JWT 处理
│   ├── logger_handler.py           # 日志处理
│   ├── md5.py                      # MD5 加密
│   ├── path_tool.py                # 路径工具
│   ├── prompt_loader.py            # 提示词加载
│   ├── response.py                 # 响应格式处理
│   └── security.py                 # 安全相关函数
```

### 前端项目 (`zhisaotong-agent-web`)

```
zhisaotong-agent-web/
├── index.html                      # HTML 入口文件
├── jsconfig.json                   # JavaScript 配置
├── package.json                    # 项目依赖配置
├── vite.config.js                  # Vite 构建配置
├── public/                         # 静态资源目录
├── src/
│   ├── App.vue                    # 根组件
│   ├── main.js                    # 应用入口
│   ├── api/
│   │   └── user.js               # API 调用接口
│   ├── assets/                    # 样式和图片资源
│   ├── components/                # 可复用组件库
│   ├── router/
│   │   └── index.js              # 路由配置
│   ├── stores/
│   │   ├── index.js              # Pinia Store 配置
│   │   └── user.js               # 用户状态管理
│   ├── utils/
│   │   └── request.js            # HTTP 请求工具（基于 Axios）
│   └── views/                     # 页面组件
│       ├── Chat.vue              # 聊天页面
│       ├── Login.vue             # 登录页面
│       ├── Register.vue          # 注册页面
│       └── Upload.vue            # 文件上传页面
```

---

## 🛠 技术栈

### 后端技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| **FastAPI** | 最新 | Web 框架 |
| **Python** | 3.8+ | 编程语言 |
| **MySQL** | 5.7+ | 关系数据库 |
| **Milvus** | 最新 | 向量数据库 |
| **Redis** | 最新 | 缓存数据库 |
| **RabbitMQ** | 最新 | 消息队列 |
| **LangChain** | 最新 | LLM 框架 |
| **阿里云 Qwen** | 最新 | 大语言模型 |
| **BAAI** | 最新 | 文本重排模型 |

### 前端技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| **Vue** | 3.5.32 | 前端框架 |
| **Vite** | 8.0.8 | 构建工具 |
| **Element Plus** | 2.13.7 | UI 组件库 |
| **Tailwind CSS** | 4.2.4 | 样式框架 |
| **Vue Router** | 4.6.4 | 路由管理 |
| **Pinia** | 3.0.4 | 状态管理 |
| **Axios** | 1.16.0 | HTTP 客户端 |
| **Node.js** | 20.19.0+ | 运行环境 |

---

## 📋 系统要求

### 后端系统要求

- **Python**: 3.8 或更高版本
- **MySQL**: 5.7 或更高版本
- **Milvus**: 2.0 或更高版本（向量数据库）
- **Redis**: 最新版本（缓存）
- **RabbitMQ**: 最新版本（消息队列）
- **内存**: 至少 8GB（推荐 16GB）
- **磁盘**: 至少 50GB（用于存储向量数据和日志）

### 前端系统要求

- **Node.js**: 20.19.0 或 22.12.0 及以上版本
- **npm** 或 **yarn**: 最新版本
- **浏览器**: 支持 ES2020 的现代浏览器（Chrome、Firefox、Safari、Edge）

---

## 🚀 快速开始

### 后端部署

#### 1. 环境配置

```bash
# 进入后端项目目录
cd zhisaotong-agent

# 创建 Python 虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

#### 2. 数据库初始化

```bash
# 1. 创建 MySQL 数据库（自己导入SQL文件）
mysql -u root -p
CREATE DATABASE zhisaotong_agent CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;

# 2. 修改 config/mysql.yml 配置数据库连接信息
host: 127.0.0.1
user: root
password: your_password
port: 3306
database: zhisaotong_agent

# 3. 初始化 Milvus 向量数据库
# 启动 Milvus（使用 Docker）
docker run -d --name milvus -p 19530:19530 -p 9091:9091 milvusdb/milvus:latest

# 4. 启动 Redis
docker run -d --name redis -p 6379:6379 redis:latest

# 5. 启动 RabbitMQ
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

#### 3. 配置文件设置

修改 `config/` 目录下的配置文件：

- **agent.yml**: 设置 LLM 模型（阿里云 Qwen 等）
- **mysql.yml**: 数据库连接信息
- **milvus.yml**: 向量数据库连接信息
- **jwt.yml**: JWT 密钥配置
- **redis.yml**: Redis 连接信息
- **rabbitmq.yml**: RabbitMQ 连接信息
- **rag.yml**: RAG 相关模型配置

#### 4. 启动后端服务

```bash
# 启动 FastAPI 服务
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 或使用 Python 直接运行
python main.py
```

后端服务将在 `http://localhost:8000` 启动，API 文档可访问 `http://localhost:8000/docs`

### 前端部署

#### 1. 环境配置

```bash
# 进入前端项目目录
cd zhisaotong-agent-web

# 安装依赖
npm install
# 或使用 yarn
yarn install
```

#### 2. 开发模式

```bash
# 启动开发服务器
npm run dev

# 开发服务器将运行在 http://localhost:5173
```

#### 3. 生产构建

```bash
# 构建生产版本
npm run build

# 预览生产构建
npm run preview
```

构建输出将在 `dist/` 目录中。

#### 4. 配置 API 代理（开发环境）

前端 Vite 配置已设置 API 代理：

```javascript
server: {
    proxy: {
        '/api': {
            target: 'http://127.0.0.1:8000',
            changeOrigin: true,
            rewrite: (path) => path.replace(/^\/api/, '/api')
        }
    }
}
```

---

## 📡 API 端点

### 用户认证模块

| 方法 | 端点 | 功能 |
|------|------|------|
| POST | `/api/users/register` | 用户注册 |
| POST | `/api/users/login` | 用户登录 |
| GET | `/api/users/profile` | 获取用户信息 |
| PUT | `/api/users/profile` | 更新用户信息 |

### 聊天模块

| 方法 | 端点 | 功能 |
|------|------|------|
| POST | `/api/chat/message` | 发送聊天消息（支持流式响应） |
| GET | `/api/chat/history/{session_id}` | 获取聊天历史 |
| DELETE | `/api/chat/history/{session_id}` | 删除聊天历史 |

### 文件管理模块

| 方法 | 端点 | 功能 |
|------|------|------|
| POST | `/api/files/upload` | 上传文件 |
| GET | `/api/files/list` | 获取用户文件列表 |
| DELETE | `/api/files/{file_id}` | 删除文件 |
| POST | `/api/files/import` | 导入文件到知识库 |

> 详细 API 文档可访问后端 Swagger UI: `http://localhost:8000/docs`

---

## 🔧 配置说明

### 后端配置文件详解

#### `config/agent.yml` - Agent 配置

```yaml
chat_model_name: qwen3-max              # 聊天 LLM 模型
embedding_model_name: text-embedding-v4 # 文本嵌入模型
rerank_model_name: BAAI/bge-reranker-base # 重排模型
```

#### `config/milvus.yml` - Milvus 向量数据库配置

```yaml
host: 127.0.0.1        # Milvus 服务器地址
port: 19530           # Milvus 端口
user: root            # 用户名
password: Milvus      # 密码
collection: file_chunks # 集合名称
k: 5                  # 相似度检索条数
limit: 10             # 查询限制
top: 5                # TopN 返回
hit: 0.4              # 相似度阈值
chunk_size: 200       # 文本块大小
chunk_overlap: 20     # 文本块重叠
```

#### `config/mysql.yml` - MySQL 数据库配置

```yaml
host: 127.0.0.1
user: root
password: 123456
port: 3306
database: zhisaotong_agent
pool_size: 10
max_overflow: 20
```

---

## 🎯 核心功能说明

### 1. React Agent 智能对话系统

位置：`agent/react_agent.py`

**功能特性**：
- 基于 LangChain 的 ReAct 模式实现
- 支持工具调用和链式推理
- 集成多个工具函数（天气查询、地理编码、数据获取等）
- 支持流式响应和 SSE 输出

**流程**：
1. 用户输入问题
2. 前置 RAG 检索相关文档
3. Agent 分析问题并调用必要工具
4. 整合检索结果和工具输出
5. 生成最终回答并流式输出

### 2. RAG 知识库系统

位置：`rag/`

**核心组件**：
- **Embedding 服务**：将文本转换为向量表示
- **Milvus 向量数据库**：存储和检索文本向量
- **BM25 重排服务**：对检索结果进行重排优化
- **RAG 服务**：整合所有组件的主服务

**流程**：
1. 文件上传和预处理
2. 文本切分（chunk）
3. 向量化和存储到 Milvus
4. 用户查询时检索相似文本
5. 使用 BM25 进行重排
6. 返回最相关的结果

### 3. 用户认证系统

位置：`utils/auth.py`、`utils/jwt.py`

**功能特性**：
- JWT Token 认证
- 密码加密存储（MD5/BCrypt）
- 用户权限管理
- Session 会话管理

### 4. 异步任务处理

位置：`rabbitmq/`、`tasks/mq_consumer.py`

**功能特性**：
- 使用 RabbitMQ 消息队列
- 异步处理文件导入和向量化
- 任务队列和重试机制

### 5. 缓存管理

位置：`cache/`、`reids_db/redis_service.py`

**功能特性**：
- Redis 缓存用户数据
- 用户会话缓存
- 频繁查询结果缓存

---

## 🎨 前端功能说明

### 页面功能

#### 1. **登录页面** (`views/Login.vue`)
- 用户邮箱/用户名登录
- 记住密码功能
- 密码重置

#### 2. **注册页面** (`views/Register.vue`)
- 新用户注册
- 邮箱验证
- 密码强度检查

#### 3. **聊天页面** (`views/Chat.vue`)
- 实时流式聊天
- 聊天历史管理
- 支持 Markdown 渲染
- 知识库文档引用

#### 4. **文件上传页面** (`views/Upload.vue`)
- 单/多文件上传
- 进度显示
- 文件管理和删除
- 导入到知识库

### 核心组件

- **Pinia 状态管理**：管理用户信息、聊天状态等
- **Vue Router**：页面路由和导航
- **Axios 请求库**：与后端 API 通信
- **Element Plus**：UI 组件库
- **Tailwind CSS**：样式框架

---

## 🔐 安全特性

1. **CORS 跨域配置**：允许前端跨域请求
2. **JWT 认证**：所有 API 端点需要有效的 JWT Token
3. **密码加密**：使用强加密算法存储密码
4. **SQL 注入防护**：使用 ORM 和参数化查询
5. **文件上传验证**：限制文件类型和大小
6. **异常捕获**：全局异常处理和日志记录

---

## 📝 开发指南

### 添加新的 Agent 工具

在 `agent/tools/agent_tools.py` 中添加新工具：

```python
from langchain.tools import tool

@tool
def new_tool(param: str) -> str:
    """工具描述"""
    # 实现逻辑
    return result
```

然后在 `agent/react_agent.py` 的工具列表中注册。

### 添加新的 API 路由

在 `routers/` 目录创建新文件，定义路由：

```python
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/api/new", tags=["new"])

@router.get("/endpoint")
async def new_endpoint():
    return {"message": "success"}
```

在 `main.py` 中注册路由：

```python
from routers import new_router
app.include_router(new_router.router)
```

### 前端页面开发

在 `src/views/` 中创建新的 Vue 组件，使用 Vue 3 Composition API：

```vue
<template>
  <div>
    <!-- 页面内容 -->
  </div>
</template>

<script setup>
import { ref } from 'vue'
// 逻辑代码
</script>

<style scoped>
/* 样式 */
</style>
```

---

## 📊 性能优化建议

### 后端优化

1. **数据库索引**：为常查询字段添加索引
2. **缓存策略**：利用 Redis 缓存频繁查询
3. **异步处理**：使用 RabbitMQ 处理耗时任务
4. **连接池**：配置适当的数据库连接池
5. **向量搜索优化**：调整 Milvus 参数（chunk_size、k 等）

### 前端优化

1. **代码分割**：使用动态导入减少初始包大小
2. **图片优化**：压缩和懒加载图片
3. **缓存策略**：利用浏览器缓存和 CDN
4. **虚拟列表**：长列表使用虚拟滚动
5. **防抖节流**：优化高频交互事件

---

## 🐛 故障排查

### 常见问题

#### 问题 1: 无法连接到 Milvus
```
解决方案：
1. 确保 Milvus 服务正在运行
2. 检查 config/milvus.yml 中的主机和端口配置
3. 检查网络连接和防火墙设置
```

#### 问题 2: 聊天响应缓慢
```
解决方案：
1. 检查 LLM API 响应时间
2. 调整 Milvus 查询参数（k、limit 等）
3. 优化 chunk_size 和 chunk_overlap
4. 检查服务器资源使用情况
```

#### 问题 3: 文件上传失败
```
解决方案：
1. 检查上传目录权限
2. 验证文件类型和大小限制
3. 检查 RabbitMQ 是否正常运行
4. 查看日志文件获取详细错误信息
```

---

## 📚 相关文档

- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [Vue 3 官方文档](https://vuejs.org/)
- [Milvus 官方文档](https://milvus.io/)
- [LangChain 官方文档](https://python.langchain.com/)
- [Element Plus 组件库](https://element-plus.org/)

---

## 📄 许可证

本项目仅供学习与参考使用。 感谢黑马程序员开源免费项目、阿里云和高德地图等开放平台。

---

## 🙏 致谢

感谢以下开源项目和服务的支持：
- FastAPI 框架
- Vue 3 框架
- LangChain 库
- Milvus 向量数据库
- Element Plus UI 组件库
- 阿里云 Qwen 大语言模型
