from fastapi import FastAPI, HTTPException
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_ollama import OllamaLLM
from pydantic import BaseModel

# 初始化Ollama聊天模型
llm = OllamaLLM(model="deepseek-r1:14b")

# 定义提示模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是乐于助人的AI助手"),
    MessagesPlaceholder(variable_name="history"),  # 历史对话记录
    ("human", "{input}")  # 用户输入
])

# 创建基础对话链
chain = prompt | llm

# 内存存储对话历史
store = {}


def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


# 创建带历史记录的对话链
conversation = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)

# 交互循环
# print("Ollama聊天demo (输入'exit'退出)")
# while True:
#     user_input = input("你: ")
#     if user_input.lower() in ['exit', 'quit']:
#         break
#
#     response = conversation.invoke(
#         {"input": user_input},
#         config={"configurable": {"session_id": "demo_session"}} # 会话ID
#     )
#     print(f"AI: {response}")

# 定义FastAPI应用
app = FastAPI()


# 定义聊天路由
class ChatRequest(BaseModel):
    message: str
    session_id: str = "default_session"


@app.post("/chat/memory")
async def chat_with_memory(request: ChatRequest):
    try:
        response = conversation.invoke(
            {"input": request.message},
            config={"configurable": {"session_id": request.session_id}}
        )
        return {"response": str(response)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 运行应用
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
