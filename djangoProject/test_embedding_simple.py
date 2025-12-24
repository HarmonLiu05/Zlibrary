"""
简单测试 Embedding 生成
"""
import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
import time

load_dotenv()

print("="*60)
print("🧪 测试 Embedding 生成")
print("="*60 + "\n")

api_provider = os.getenv("API_PROVIDER", "openai")
token = os.getenv("MODELSCOPE_ACCESS_TOKEN", "")

print(f"API 提供商: {api_provider}")
print(f"Token: {token[:20]}...\n")

# 创建 Embeddings
print("1️⃣ 创建 Embeddings 对象...")
embeddings = OpenAIEmbeddings(
    openai_api_key=token,
    openai_api_base="https://api-inference.modelscope.cn/v1",
    model="Qwen/Qwen3-Embedding-8B"
)
print("✅ Embeddings 对象已创建\n")

# 测试单个文本
print("2️⃣ 测试生成单个向量...")
test_text = "这是一本测试书籍"
print(f"输入文本: {test_text}")

try:
    print("⏳ 调用 API...")
    start_time = time.time()
    
    vector = embeddings.embed_query(test_text)
    
    end_time = time.time()
    print(f"✅ 成功！耗时: {end_time - start_time:.2f}秒")
    print(f"向量维度: {len(vector)}")
    print(f"向量前10个值: {vector[:10]}\n")
    
    # 测试批量文本
    print("3️⃣ 测试生成批量向量...")
    test_texts = [
        "书名: 离散数学\n作者: 屈婉玲",
        "书名: 计算机系统\n作者: 袁春风",
        "书名: 线性代数\n作者: 居余马"
    ]
    
    print(f"输入 {len(test_texts)} 条文本")
    print("⏳ 调用 API...")
    start_time = time.time()
    
    vectors = embeddings.embed_documents(test_texts)
    
    end_time = time.time()
    print(f"✅ 成功！耗时: {end_time - start_time:.2f}秒")
    print(f"生成了 {len(vectors)} 个向量")
    print(f"每个向量维度: {len(vectors[0])}")
    
    print("\n" + "="*60)
    print("🎉 所有测试通过！")
    print("="*60)
    
except Exception as e:
    print(f"\n❌ 测试失败: {e}")
    import traceback
    print(f"\n详细错误:\n{traceback.format_exc()}")
