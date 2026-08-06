import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Dict


load_dotenv()


class AgentsLLM:
    def __init__(self, model: str = None, apiKey: str = None, baseUrl: str = None, timeout: int = None):
        self.model = model or os.getenv("LLM_MODEL_ID")
        apiKey = apiKey or os.getenv("LLM_API_KEY")
        baseUrl = baseUrl or os.getenv("LLM_BASE_URL")
        timeout = timeout or int(os.getenv("LLM_TIMEOUT", 60))

        if not all([self.model, apiKey, baseUrl]):
            raise ValueError("模型ID、API秘钥、和服务器地址必须提供，或在.env文件中定义")

        self.client = OpenAI(api_key=apiKey, base_url=baseUrl, timeout=timeout)

    def think(self, msg: List[Dict[str, str]], temperature: float = 0) ->str:
        """"""
        print(f"🧠正在调用{self.model}模型...")
        try:
            response = self.client.chat.completions.create(model = self.model, messages = msg, temperature = temperature, stream = True)

            print("✅ 大语言模型响应成功:")
            result = []
            for chunk in response:
                if not chunk.choices:
                    continue
                content = chunk.choices[0].delta.content or ""
                print(content, end="", flush=True)
                result.append(content)

            print("")
            return "".join(result)

        except Exception as e:
            print(f"❌ 调用LLM API时发生错误: {e}")
            return None


if __name__ == "__main__":
    try:
        llm = AgentsLLM()

        exampleMessages = [
            {"role": "system", "content": "You are a helpful assistant that writes python code."},
            {"role": "user", "content": "写一个快速排序算法"}
        ]

        responseText = llm.think(exampleMessages)
        if responseText:
            print("\n\n--- 完整模型响应 ---")
            print(responseText)

    except ValueError as e:
        print(e)
