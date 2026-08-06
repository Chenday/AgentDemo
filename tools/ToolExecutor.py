

from typing import Dict, Any

class ToolExecutor:
    """
    工具执行器，负责管理和执行工具
    """
    _instance = None
    tools: Dict[str, Dict[str, Any]] = {} 

    def  __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def registerTool(cls, name: str, description: str, func: callable):
        """向工具注册一个新工具"""
        if name in cls.tools:
            print(f"Warming： 工具 '{name}' 已存在，将被覆盖。")
        cls.tools[name] = {"description": description, "func": func}
        print(f"工具 '{name}' 已注册。")

    def getTool(self, name: str) -> callable:
        """
        根据名称获取一个工具的执行函数
        """
        return self.tools.get(name, {}).get("func")

    def getAvailableTools(self) -> str:
        """
        获取所有可用工具的格式化描述字符串
        """
        return "\n".join([f"- {name} : {info['description']}"
            for name, info in self.tools.items()])

import tools.implement

if __name__ == '__main__':
    # 1. 初始化工具执行器
    from dotenv import load_dotenv
    load_dotenv()

    toolExecutor = ToolExecutor()

    from implement import serpApi
    toolExecutor.registerTool("Search", serpApi.description, serpApi.search)

    print("\n--- 可用的工具 ---")
    print(toolExecutor.getAvailableTools())

    print("\n--- 执行 Action: Search['英伟达最新的GPU型号是什么'] ---")
    tool_name = "Search"
    tool_input = "英伟达最新的GPU型号是什么"

    tool_function = toolExecutor.getTool(tool_name)
    if tool_function:
        observation = tool_function(tool_input)
        print("--- 观察 (Observation) ---")
        print(observation)
    else:
        print(f"错误:未找到名为 '{tool_name}' 的工具。")