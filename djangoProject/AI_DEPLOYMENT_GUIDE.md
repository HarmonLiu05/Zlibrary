# BookNest AI 问答功能部署指南

## 🎉 恭喜！RAG AI 问答助手已经完整实现

---

## 📋 功能清单

✅ **1. 依赖包更新** (`requirements.txt`)
   - LangChain 0.1.0
   - LangChain-OpenAI 0.0.2
   - OpenAI 1.12.0
   - FAISS-CPU 1.7.4
   - Python-dotenv 1.0.0
   - Tiktoken 0.5.2

✅ **2. RAG 核心模块** (`books/utils/rag.py`)
   - RAGAssistant 类：封装完整的 RAG 逻辑
   - build_index()：构建 FAISS 向量索引
   - search_books()：向量检索
   - generate_answer()：LLM 生成回答
   - query_books()：完整查询流程

✅ **3. Management Command** (`books/management/commands/build_embeddings.py`)
   - 一键生成所有书籍的向量索引

✅ **4. API 接口** (`books/views.py` + `books/urls.py`)
   - `/api/chat/` POST 接口
   - 接收用户问题，返回 AI 回答

✅ **5. 前端聊天窗口** (`books/templates/base.html`)
   - 右下角悬浮按钮
   - 弹出式聊天界面
   - Bootstrap 5 风格设计

✅ **6. 环境配置** (`.env.example`)
   - OpenAI API Key 配置模板

---

## 🚀 部署步骤

### **步骤 1: 安装依赖**

```powershell
# 激活虚拟环境
.\venv\Scripts\Activate.ps1

# 安装新依赖
pip install -r requirements.txt
```

### **步骤 2: 配置 API Key**

1. 复制 `.env.example` 为 `.env`：
```powershell
Copy-Item .env.example .env
```

2. 编辑 `.env` 文件，填入你的 OpenAI API Key：
```env
OPENAI_API_KEY=sk-your-actual-api-key-here
```

### **步骤 3: 生成向量索引**

```powershell
python manage.py build_embeddings
```

**输出示例**：
```
开始构建书籍向量索引...
找到 50 本书籍
📊 正在为 50 本书生成向量...
✅ 索引构建完成！已保存到 data/faiss_index.bin
✅ 成功为 50 本书生成向量索引！
现在可以使用 AI 问答功能了
```

### **步骤 4: 启动服务**

```powershell
python manage.py runserver
```

### **步骤 5: 测试功能**

1. 打开浏览器访问：http://127.0.0.1:8000/
2. 点击右下角的紫色聊天按钮 💬
3. 输入问题测试，例如：
   - "有没有适合新手的 Python 书？"
   - "推荐几本机器学习的书籍"
   - "有哪些小说类的书？"

---

## 📁 新增文件结构

```
djangoProject/
├── books/
│   ├── utils/
│   │   ├── __init__.py          # ✅ 新建
│   │   └── rag.py               # ✅ 新建 (RAG 核心逻辑)
│   └── management/
│       └── commands/
│           └── build_embeddings.py  # ✅ 新建
├── data/                         # ✅ 自动创建
│   ├── faiss_index.bin          # 向量索引文件
│   └── book_metadata.pkl        # 书籍元数据
├── .env.example                 # ✅ 新建
├── .env                         # 需要自己创建
└── requirements.txt             # ✅ 已更新
```

---

## 🔧 技术细节

### **RAG 工作流程**

1. **用户提问** → 前端发送到 `/api/chat/`
2. **向量化** → 使用 OpenAI Embeddings 将问题转为向量
3. **检索** → FAISS 在本地索引中搜索最相似的 5 本书
4. **生成** → 将检索结果 + 问题组装成 Prompt，调用 GPT-3.5 生成回答
5. **返回** → JSON 格式返回给前端展示

### **性能优化**

- ✅ 使用 FAISS-CPU 轻量级向量库（无需 GPU）
- ✅ 索引文件本地存储，无需每次查询时重新计算
- ✅ 单例模式缓存 RAG 助手实例

### **成本控制**

- Embedding API 调用：仅在构建索引时调用（每本书 1 次）
- LLM API 调用：每次用户提问调用 1 次
- 预计成本：约 $0.002 - $0.005 / 问题

---

## ⚠️ 常见问题

### **Q1: 提示 "没有找到索引文件"**
**A**: 运行 `python manage.py build_embeddings` 生成索引

### **Q2: API 报错 "Invalid API Key"**
**A**: 检查 `.env` 文件中的 `OPENAI_API_KEY` 是否正确

### **Q3: 聊天窗口无响应**
**A**: 
1. 检查浏览器控制台是否有错误
2. 确认后端服务正常运行
3. 检查 `/api/chat/` 接口是否可访问

### **Q4: 想更新书籍数据后重新生成索引**
**A**: 删除 `data/` 目录，重新运行 `python manage.py build_embeddings`

---

## 🎨 前端界面说明

- **悬浮按钮**：右下角紫色圆形按钮，带渐变效果
- **聊天窗口**：380x550px，固定在右下角
- **消息气泡**：
  - 用户消息：蓝紫色，右对齐
  - AI 回答：白色，左对齐
- **加载状态**：显示 "AI 正在思考..." 提示

---

## 📊 下一步优化建议

1. **历史记录保存**：将对话记录存入数据库
2. **多轮对话**：支持上下文记忆
3. **用户反馈**：添加"赞"/"踩"按钮收集反馈
4. **流式输出**：使用 SSE 实现打字机效果
5. **个性化推荐**：结合用户借阅历史

---

## 📞 技术支持

如有问题，请检查：
1. 依赖是否完整安装
2. API Key 是否正确配置
3. 索引文件是否成功生成
4. 后端日志是否有报错信息

祝你使用愉快！🎉
