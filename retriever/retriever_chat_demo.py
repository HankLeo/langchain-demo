from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaEmbeddings, OllamaLLM

# 文档示例
documents = [
    Document(
        page_content="猫是独立的动物，通常喜欢自己的空间",
        metadata={"source": "哺乳动物宠物文档"},
    ),
    Document(
        page_content="狗是人类的好朋友",
        metadata={"source": "哺乳动物宠物文档"},
    ),
    Document(
        page_content="金鱼生活在鱼缸里",
        metadata={"source": "鱼类宠物文档"},
    )
]

# 实例化Chroma向量存储
vector_store = Chroma.from_documents(documents, embedding=OllamaEmbeddings(model="mxbai-embed-large:latest"))

# 执行查询
# query = "加菲猫"
# results = vector_store.similarity_search_with_score(query)
# print(results)

# 检索器
# retriever = RunnableLambda(vector_store.similarity_search).bind(k=1)
retriever = vector_store.as_retriever().bind(k=1)

# 测试查询
query = "加菲猫"
print(retriever.batch([query]))

# 定义提示模板
message = """
你是一个专业的宠物医生，你会根据用户的问题和上下文来回答。
请根据以下上下文回答用户的问题：
{context}
问题：{question}
"""
prompt = ChatPromptTemplate.from_messages([
    ("human", message)
])

# 初始化Ollama聊天模型
llm = OllamaLLM(model="qwen3:latest")

# 创建完整chain
chain = (
        {
            "context": lambda x: retriever.batch([x["question"]])[0],
            "question": lambda x: x["question"]
        }
        | prompt
        | llm
        | StrOutputParser()
)

# 交互循环
print("宠物知识问答系统 (输入'exit'退出)")
while True:
    user_input = input("你的问题: ")
    if user_input.lower() in ['exit', 'quit']:
        break

    response = chain.invoke({"question": user_input})
    print(f"AI: {response}")
