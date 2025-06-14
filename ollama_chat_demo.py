from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate

# 初始化Ollama本地模型
llm = Ollama(model="deepseek-r1:14b")

# 定义聊天提示模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant."),
    ("human", "{user_input}")
])

# 创建聊天链
chain = prompt | llm

# 与模型交互
while True:
    user_input = input("You: ")
    if user_input.lower() in ['exit', 'quit']:
        break
    
    response = chain.invoke({"user_input": user_input})
    print(f"AI: {response}")