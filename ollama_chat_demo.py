from fastapi import FastAPI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from pydantic import BaseModel

# 初始化Ollama本地模型
llm = OllamaLLM(model="deepseek-r1:14b")

# 定义聊天提示模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant."),
    ("human", "{user_input}")
])

parser = StrOutputParser()

# 创建聊天链
# LangChain Expression Language (LCEL)
chain = prompt | llm | parser

# 与模型的控制台交互
# while True:
#     user_input = input("You: ")
#     if user_input.lower() in ['exit', 'quit']:
#         break

#     response = chain.invoke({"user_input": user_input})
#     print(f"AI: {response}")

# 定义FastAPI应用
app = FastAPI()


# 定义聊天路由
class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
async def chat(request: ChatRequest):
    response = chain.invoke({"user_input": request.message})
    return {"response": response}


# 定义根路由
@app.get("/")
async def root():
    return {"message": "Hello, FastAPI!"}


# 运行应用
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
