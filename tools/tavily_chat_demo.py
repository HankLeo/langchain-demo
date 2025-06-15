import os

from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama
from langchain_tavily import TavilySearch

# 从环境变量获取Tavily API Key
tavily_api_key = os.getenv("TAVILY_API_KEY")
if not tavily_api_key:
    raise ValueError("请设置TAVILY_API_KEY环境变量")

# 创建Tavily搜索工具
search_tool = TavilySearch(tavily_api_key=tavily_api_key, max_results=3)

# 初始化Ollama聊天模型
llm = ChatOllama(model="qwen3:latest")

# 定义工具列表
tools = [search_tool]

# 创建提示模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个有用的助手，可以使用工具查询信息。"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# 创建代理
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 交互循环
print("Tavily搜索聊天demo (输入'exit'退出)")
while True:
    user_input = input("你: ")
    if user_input.lower() in ['exit', 'quit']:
        break

    response = agent_executor.invoke({"input": user_input})
    print(f"AI: {response['output']}")
