# 图书管理系统 📚

小组作业，基于 Django 的智能图书管理系统，集成 AI 问答助手（RAG）。

## 👥 团队分工

- **前端** - 黄为浩
- **后端** - 夏梓程
- **数据库** - 刘和雄

---

## 🌟 功能特性

- ✅ 用户注册/登录（邮箱激活）
- ✅ 图书浏览与搜索
- ✅ 图书借阅/归还管理
- ✅ 个人借阅记录查询
- ✅ 批量导入图书（CSV + 图片）
- ✅ **AI 智能问答助手**（基于 RAG + DeepSeek-V3.2）

---

## 🛠️ 技术栈

- **后端框架**: Django 6.0
- **数据库**: SQLite3
- **AI 模型**: 
  - 对话模型：DeepSeek-V3.2（通过 ModelScope API）
  - 向量模型：Qwen3-Embedding-8B
- **向量检索**: FAISS
- **前端**: Bootstrap 5 + JavaScript

---

## 📦 快速开始

### 1️⃣ 环境要求

- Python 3.8+
- Windows/Linux/MacOS

### 2️⃣ 克隆项目

```bash
git clone <项目地址>
cd Zlibrary/djangoProject
```

### 3️⃣ 创建虚拟环境

**Windows (PowerShell)**:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux/Mac**:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4️⃣ 安装依赖

```bash
pip install -r requirements.txt
```

### 5️⃣ 配置环境变量

复制示例配置文件：
```bash
cp .env.example .env
```

编辑 `.env` 文件，配置 API：

```env
# 使用 ModelScope API（免费）
API_PROVIDER=modelscope
MODELSCOPE_ACCESS_TOKEN=你的ModelScope_Token

# 或使用 OpenAI API（需付费）
# API_PROVIDER=openai
# OPENAI_API_KEY=你的OpenAI_API_Key
```

**如何获取 ModelScope Token？**
1. 访问 https://modelscope.cn/
2. 注册/登录账号
3. 进入 **个人中心** → **API Token**
4. 创建或复制 Access Token

### 6️⃣ 初始化数据库

```bash
python manage.py migrate
```

### 7️⃣ 生成 AI 向量索引

```bash
python manage.py build_embeddings
```

**预期输出**:
```
开始构建书籍向量索引...
找到 XX 本书籍
📊 正在为 XX 本书生成向量...
✅ 索引构建完成！
```

### 8️⃣ 创建管理员账号（可选）

```bash
python manage.py createsuperuser
```

### 9️⃣ 启动服务

```bash
python manage.py runserver
```

**访问地址**:
- 前台：http://127.0.0.1:8000/
- 管理后台：http://127.0.0.1:8000/admin/

---

## 🤖 AI 问答助手使用

1. 打开网站首页
2. 点击右下角 **紫色聊天按钮** 💬
3. 输入问题，例如：
   - "有没有适合新手的 Python 书？"
   - "推荐几本机器学习的书籍"
   - "有哪些小说类的书？"

**注意**: 首次使用时响应时间约 10-20 秒（模型加载 + API 调用）

---

## 📊 批量导入图书

1. 访问 http://127.0.0.1:8000/import/
2. 准备 CSV 文件，格式：
   ```csv
   title,author,isbn,stock,category,publisher,publish_date,description,image_url
   Python编程,张三,9787111111111,5,编程,机械工业出版社,2023-01-01,Python入门书籍,https://...
   ```
3. 可选：准备图片压缩包（ZIP），图片名为 ISBN 号
4. 上传并导入

---

## 🔧 常见问题

### Q1: AI 聊天响应很慢？

**原因**: 使用免费的 ModelScope API，响应时间 10-20 秒属于正常。

**解决方案**:
- 切换到 OpenAI API（响应时间 < 2 秒）
- 或者等待，系统已优化显示等待进度

### Q2: 提示 "没有找到索引文件"？

**解决**: 运行 `python manage.py build_embeddings` 生成索引

### Q3: API 报错 "Invalid Token"？

**检查**:
1. `.env` 文件中的 Token 是否正确
2. ModelScope Token 是否过期
3. 网络是否正常连接

### Q4: 邮件激活失败？

**配置**: 修改 `djangoProject/settings.py` 中的邮箱配置：
```python
EMAIL_HOST_USER = '你的邮箱@qq.com'
EMAIL_HOST_PASSWORD = '你的授权码'
```

---

## 📁 项目结构

```
djangProject/
├── books/                    # 主应用
│   ├── management/
│   │   └── commands/
│   │       └── build_embeddings.py  # 生成向量索引命令
│   ├── templates/            # HTML 模板
│   ├── utils/
│   │   └── rag.py           # RAG 核心逻辑
│   ├── models.py            # 数据模型
│   ├── views.py             # 视图函数
│   └── urls.py              # 路由配置
├── djangoProject/           # 项目配置
│   └── settings.py          # 全局设置
├── rag_data/                # 向量索引数据（自动生成）
│   ├── faiss_index.bin
│   └── book_metadata.pkl
├── media/                   # 上传的图片
├── .env                     # 环境变量配置
├── requirements.txt         # 依赖包列表
└── manage.py               # Django 管理脚本
```

---

## 🚀 性能优化建议

1. **生产环境部署**:
   - 使用 Nginx + Gunicorn
   - 切换到 PostgreSQL 数据库
   - 配置 Redis 缓存

2. **API 优化**:
   - 切换到 OpenAI API（速度提升 5-10 倍）
   - 或使用本地部署的模型

3. **向量检索优化**:
   - 定期更新索引
   - 使用 GPU 加速（FAISS-GPU）

---

## 📝 更新日志

### v2.0 (2025-12-28)
- ✅ 集成 DeepSeek-V3.2 AI 对话模型
- ✅ 优化聊天界面用户体验
- ✅ 添加实时等待进度显示
- ✅ 完善部署文档

### v1.0
- ✅ 基础图书管理功能
- ✅ 用户注册与邮箱激活
- ✅ 图书借阅管理

---

## 📞 技术支持

如有问题，请检查：
1. Python 版本是否 ≥ 3.8
2. 依赖是否完整安装
3. `.env` 配置是否正确
4. 向量索引是否成功生成

**相关文档**:
- [API 提供商选择指南](API_PROVIDER_GUIDE.md)
- [AI 部署指南](AI_DEPLOYMENT_GUIDE.md)

---

## 📄 开源协议

MIT License

---

**祝你使用愉快！** 🎉