"""
RAG (检索增强生成) 核心模块
用于图书管理系统的智能问答功能
支持两种 API：OpenAI 官方 API 和 ModelScope API
"""
import os
import pickle
from pathlib import Path
from typing import List, Dict

import faiss
import numpy as np
from django.conf import settings
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置
# 使用项目根目录下的 rag_data 文件夹存储索引数据
# 这样可以确保在不同主机上都能正常使用
DATA_DIR = Path(settings.BASE_DIR) / "rag_data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

FAISS_INDEX_PATH = DATA_DIR / "faiss_index.bin"
BOOK_METADATA_PATH = DATA_DIR / "book_metadata.pkl"

# 动态设置向量维度（根据使用的模型）
if os.getenv("API_PROVIDER", "openai").lower() == "modelscope":
    EMBEDDING_DIM = 4096  # DeepSeek/Qwen Embedding 模型的维度
else:
    EMBEDDING_DIM = 1536  # OpenAI text-embedding-ada-002 的维度

# API 提供商配置
API_PROVIDER = os.getenv("API_PROVIDER", "openai").lower()  # 默认使用 openai

# 确保数据目录存在
FAISS_INDEX_PATH.parent.mkdir(exist_ok=True)


def create_embeddings():
    """
    创建 Embeddings 实例
    支持 OpenAI 和 ModelScope (DeepSeek) 两种 API
    """
    if API_PROVIDER == "modelscope":
        # 使用 ModelScope API with DeepSeek Embedding
        # 注意：DeepSeek 可能没有独立的 Embedding 模型，这里使用 Qwen Embedding
        return OpenAIEmbeddings(
            openai_api_key=os.getenv("MODELSCOPE_ACCESS_TOKEN"),
            openai_api_base="https://api-inference.modelscope.cn/v1",
            model="Qwen/Qwen3-Embedding-8B"  # 向量模型（DeepSeek暂无独立Embedding，使用Qwen）
        )
    else:
        # 使用官方 OpenAI API（默认）
        return OpenAIEmbeddings(
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            model="text-embedding-ada-002"
        )


def create_llm():
    """
    创建 LLM 实例
    支持 OpenAI 和 ModelScope (DeepSeek) 两种 API
    """
    if API_PROVIDER == "modelscope":
        # 使用 ModelScope API with DeepSeek-V3.2
        return ChatOpenAI(
            openai_api_key=os.getenv("MODELSCOPE_ACCESS_TOKEN"),
            openai_api_base="https://api-inference.modelscope.cn/v1",
            model="deepseek-ai/DeepSeek-V3.2",  # DeepSeek-V3.2 对话模型
            temperature=0.7
        )
    else:
        # 使用官方 OpenAI API（默认）
        return ChatOpenAI(
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            model="gpt-3.5-turbo",
            temperature=0.7
        )


class RAGAssistant:
    """RAG 助手类"""
    
    def __init__(self):
        self.embeddings = create_embeddings()
        self.llm = create_llm()
        self.index = None
        self.book_metadata = []
        self._load_index()
        
        # 显示使用的模型信息
        print(f"✅ RAG 助手已初始化 (API 提供商: {API_PROVIDER.upper()})")
        if API_PROVIDER == "modelscope":
            print(f"💬 对话模型: deepseek-ai/DeepSeek-V3.2")
            print(f"🔍 Embedding 模型: Qwen/Qwen3-Embedding-8B")
        else:
            print(f"💬 对话模型: gpt-3.5-turbo")
            print(f"🔍 Embedding 模型: text-embedding-ada-002")
    
    def _load_index(self):
        """加载 FAISS 索引和书籍元数据"""
        if FAISS_INDEX_PATH.exists() and BOOK_METADATA_PATH.exists():
            try:
                self.index = faiss.read_index(str(FAISS_INDEX_PATH))
                with open(BOOK_METADATA_PATH, 'rb') as f:
                    self.book_metadata = pickle.load(f)
                print(f"✅ 成功加载索引，共 {len(self.book_metadata)} 本书")
            except Exception as e:
                print(f"❌ 加载索引失败: {e}")
                self.index = None
                self.book_metadata = []
        else:
            print("⚠️  索引文件不存在，请先运行 python manage.py build_embeddings")
    
    def build_index(self, books_queryset):
        """
        构建 FAISS 索引
        :param books_queryset: Django QuerySet of Book 模型
        """
        try:
            print("🔨 开始构建向量索引...")
            
            # 准备数据
            texts = []
            metadata = []
            
            for book in books_queryset:
                # 组合书籍信息作为文本
                text = f"书名: {book.title}\n作者: {book.author}\n分类: {book.category}"
                if book.publisher:
                    text += f"\n出版社: {book.publisher}"
                if book.description:
                    text += f"\n简介: {book.description}"
                
                texts.append(text)
                metadata.append({
                    'id': book.id,
                    'title': book.title,
                    'author': book.author,
                    'category': book.category,
                    'publisher': book.publisher or '',
                    'description': book.description or '',
                    'stock': book.stock
                })
            
            if not texts:
                print("⚠️  没有找到任何书籍数据")
                return
            
            # 生成向量
            print(f"📊 正在为 {len(texts)} 本书生成向量...")
            embeddings = self.embeddings.embed_documents(texts)
            embeddings_array = np.array(embeddings, dtype='float32')
            
            print(f"📦 向量生成完成，形状: {embeddings_array.shape}")
            print(f"🔢 期望维度: {EMBEDDING_DIM}, 实际维度: {embeddings_array.shape[1]}")
            
            # 创建 FAISS 索引
            print(f"🛠️  创建 FAISS 索引 (维度: {EMBEDDING_DIM})...")
            self.index = faiss.IndexFlatL2(EMBEDDING_DIM)
            self.index.add(embeddings_array)
            self.book_metadata = metadata
            
            print(f"💾 保存索引到: {FAISS_INDEX_PATH}")
            # 确保目录存在（在保存之前）
            data_dir = FAISS_INDEX_PATH.parent
            print(f"📂 检查目录: {data_dir}")
            if not data_dir.exists():
                print(f"📦 目录不存在，创建中...")
                data_dir.mkdir(parents=True, exist_ok=True)
                print(f"✅ 目录已创建: {data_dir}")
            else:
                print(f"✅ 目录已存在: {data_dir}")
            
            # 保存索引
            faiss.write_index(self.index, str(FAISS_INDEX_PATH))
            print(f"✅ FAISS 索引已保存")
            
            print(f"💾 保存元数据到: {BOOK_METADATA_PATH}")
            with open(BOOK_METADATA_PATH, 'wb') as f:
                pickle.dump(metadata, f)
            print(f"✅ 元数据已保存")
            
            print(f"\n✅ 索引构建完成！已保存到 {FAISS_INDEX_PATH}")
            
        except Exception as e:
            print(f"\n❌ 构建索引失败: {e}")
            import traceback
            print(f"详细错误信息:\n{traceback.format_exc()}")
            raise
    
    def search_books(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        检索相关书籍
        :param query: 用户问题
        :param top_k: 返回前 k 本书
        :return: 书籍列表
        """
        if self.index is None or not self.book_metadata:
            return []
        
        # 将查询转为向量
        query_embedding = self.embeddings.embed_query(query)
        query_vector = np.array([query_embedding], dtype='float32')
        
        # 搜索最相似的书籍
        distances, indices = self.index.search(query_vector, top_k)
        
        results = []
        for idx, distance in zip(indices[0], distances[0]):
            if idx < len(self.book_metadata):
                book = self.book_metadata[idx].copy()
                book['similarity_score'] = float(1 / (1 + distance))  # 转换为相似度分数
                results.append(book)
        
        return results
    
    def generate_answer(self, question: str, retrieved_books: List[Dict]) -> str:
        """
        生成回答
        :param question: 用户问题
        :param retrieved_books: 检索到的书籍列表
        :return: AI 生成的回答
        """
        print(f"🤖 正在使用 DeepSeek-V3.2 生成回答...")  # 添加日志
        
        if not retrieved_books:
            return "抱歉，我没有找到相关的书籍。您可以尝试换一个问题，或者直接在首页搜索书名和作者。"
        
        # 构建上下文
        context = "以下是图书馆中与您问题相关的书籍：\n\n"
        for i, book in enumerate(retrieved_books, 1):
            context += f"{i}. **《{book['title']}》**\n"
            context += f"   - 作者: {book['author']}\n"
            context += f"   - 分类: {book['category']}\n"
            if book.get('publisher'):
                context += f"   - 出版社: {book['publisher']}\n"
            if book.get('description'):
                context += f"   - 简介: {book['description'][:100]}...\n"
            context += f"   - 库存: {'有货' if book['stock'] > 0 else '暂无'}\n"
            context += f"   - 详情链接: /books/{book['id']}/\n\n"
        
        # 创建 Prompt
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", """你是 BookNest 图书管理系统的智能助手。你的任务是根据用户的问题和提供的书籍信息，给出专业、友好的推荐。

规则：
1. 基于提供的书籍信息进行推荐
2. 如果提到书名，请使用《书名》格式
3. 可以附上详情链接，格式为：[查看详情](/books/书籍ID/)
4. 保持回答简洁、友好
5. 如果用户问题与书籍无关，礼貌地引导回图书相关话题"""),
            ("user", "用户问题: {question}\n\n{context}\n\n请根据以上信息回答用户的问题。")
        ])
        
        # 生成回答
        messages = prompt_template.format_messages(
            question=question,
            context=context
        )
        
        response = self.llm.invoke(messages)
        return response.content
    
    def query_books(self, question: str) -> Dict:
        """
        完整的查询流程
        :param question: 用户问题
        :return: 包含回答和相关书籍的字典
        """
        # 检索书籍
        retrieved_books = self.search_books(question, top_k=5)
        
        # 生成回答
        answer = self.generate_answer(question, retrieved_books)
        
        return {
            'answer': answer,
            'books': retrieved_books[:3],  # 只返回前3本用于前端展示
            'total_found': len(retrieved_books)
        }


# 全局单例
_rag_assistant = None


def get_rag_assistant() -> RAGAssistant:
    """获取 RAG 助手单例"""
    global _rag_assistant
    if _rag_assistant is None:
        _rag_assistant = RAGAssistant()
    return _rag_assistant
