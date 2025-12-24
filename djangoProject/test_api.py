"""
测试 ModelScope API 连接
"""
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

print("="*60)
print("🔍 测试 ModelScope API 连接")
print("="*60 + "\n")

# 读取配置
api_provider = os.getenv("API_PROVIDER", "openai")
modelscope_token = os.getenv("MODELSCOPE_ACCESS_TOKEN", "")

print(f"API 提供商: {api_provider}")
print(f"ModelScope Token: {modelscope_token[:20]}... (已隐藏)\n")

if api_provider == "modelscope" and modelscope_token:
    print("🧪 正在测试 ModelScope API...")
    
    try:
        # 创建客户端
        client = OpenAI(
            api_key=modelscope_token,
            base_url="https://api-inference.modelscope.cn/v1"
        )
        
        # 测试对话模型
        print("\n1️⃣ 测试对话模型 (Qwen/Qwen2.5-Coder-32B-Instruct)...")
        response = client.chat.completions.create(
            model="Qwen/Qwen2.5-Coder-32B-Instruct",
            messages=[
                {"role": "user", "content": "你好，请回复'测试成功'"}
            ],
            max_tokens=10
        )
        print(f"✅ 对话模型响应: {response.choices[0].message.content}")
        
        # 测试向量模型
        print("\n2️⃣ 测试向量模型 (Qwen/Qwen3-Embedding-8B)...")
        response = client.embeddings.create(
            model="Qwen/Qwen3-Embedding-8B",
            input="测试文本"
        )
        embedding_dim = len(response.data[0].embedding)
        print(f"✅ 向量模型响应成功！向量维度: {embedding_dim}")
        
        print("\n" + "="*60)
        print("🎉 ModelScope API 连接测试成功！")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ API 测试失败: {str(e)}")
        print("\n可能的原因:")
        print("1. Access Token 不正确或已过期")
        print("2. 模型名称错误")
        print("3. 网络连接问题")
        print("4. API 配额用尽")
        print("\n建议:")
        print("- 访问 https://modelscope.cn/ 检查你的 Access Token")
        print("- 尝试重新生成 Access Token")
        print("- 或者切换到 OpenAI API")
else:
    print("⚠️  当前配置为 OpenAI API 或未配置 ModelScope Token")
    print("\n如果要使用 ModelScope:")
    print("1. 编辑 .env 文件")
    print("2. 设置 API_PROVIDER=modelscope")
    print("3. 填入你的 MODELSCOPE_ACCESS_TOKEN")
