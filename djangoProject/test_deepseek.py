"""
测试 DeepSeek-V3.2 模型在 ModelScope API 上的连接
"""
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

print("="*60)
print("🔍 测试 DeepSeek-V3.2 模型")
print("="*60 + "\n")

# 读取配置
api_provider = os.getenv("API_PROVIDER", "openai")
modelscope_token = os.getenv("MODELSCOPE_ACCESS_TOKEN", "")

print(f"API 提供商: {api_provider}")
print(f"ModelScope Token: {modelscope_token[:20]}... (已隐藏)\n")

if api_provider == "modelscope" and modelscope_token:
    print("🧪 正在测试 DeepSeek-V3.2 模型...\n")
    
    try:
        # 创建客户端
        client = OpenAI(
            api_key=modelscope_token,
            base_url="https://api-inference.modelscope.cn/v1"
        )
        
        # 测试 DeepSeek-V3.2 对话模型
        print("1️⃣ 测试 DeepSeek-V3.2 对话模型...")
        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3.2",
            messages=[
                {"role": "user", "content": "你好，请用一句话介绍你自己"}
            ],
            max_tokens=100
        )
        print(f"✅ DeepSeek-V3.2 响应: {response.choices[0].message.content}")
        print(f"📊 模型: {response.model}")
        
        # 测试生成速度
        print("\n2️⃣ 测试响应速度...")
        import time
        start_time = time.time()
        
        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3.2",
            messages=[
                {"role": "user", "content": "推荐一本Python入门书籍"}
            ],
            max_tokens=150
        )
        
        elapsed_time = time.time() - start_time
        print(f"✅ 响应内容: {response.choices[0].message.content}")
        print(f"⏱️ 响应时间: {elapsed_time:.2f} 秒")
        
        # 测试 DeepSeek Embedding 模型
        print("\n3️⃣ 测试 DeepSeek Embedding 模型...")
        try:
            embedding_response = client.embeddings.create(
                model="deepseek-ai/DeepSeek-V3.2",
                input="测试文本"
            )
            embedding_dim = len(embedding_response.data[0].embedding)
            print(f"✅ DeepSeek Embedding 响应成功！向量维度: {embedding_dim}")
        except Exception as e:
            print(f"⚠️ DeepSeek 没有独立的 Embedding 模型: {str(e)}")
            print("💡 建议：使用 Qwen/Qwen3-Embedding-8B 作为 Embedding 模型")
        
        print("\n" + "="*60)
        print("🎉 DeepSeek-V3.2 测试成功！")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ DeepSeek-V3.2 测试失败: {str(e)}")
        print("\n可能的原因:")
        print("1. DeepSeek-V3.2 在 ModelScope 上可能不存在或名称不正确")
        print("2. 模型名称应该检查是否为: deepseek-ai/DeepSeek-V3 或其他版本")
        print("3. Access Token 不正确或已过期")
        print("4. 网络连接问题")
        print("\n建议:")
        print("- 访问 https://modelscope.cn/models 搜索 DeepSeek 查看可用模型")
        print("- 检查模型的正确名称和版本号")
        print("- 或者继续使用 Qwen 模型（已验证可用）")
else:
    print("⚠️  当前配置为 OpenAI API 或未配置 ModelScope Token")
    print("\n如果要使用 ModelScope:")
    print("1. 编辑 .env 文件")
    print("2. 设置 API_PROVIDER=modelscope")
    print("3. 填入你的 MODELSCOPE_ACCESS_TOKEN")
