import json

import requests

API_URL = "http://localhost:8000/chat/memory"


def chat_with_ollama(message, stream=False):
    """
    调用Ollama聊天API
    :param message: 用户输入的消息
    :param stream: 是否使用流式响应
    :return: API返回的响应内容
    """
    headers = {"Content-Type": "application/json"}
    data = {"message": message, "session_id": "demo_session"}
    params = {"stream": "true"} if stream else {}

    try:
        response = requests.post(
            API_URL,
            headers=headers,
            params=params,
            data=json.dumps(data)
        )
        response.raise_for_status()
        return response.json() if not stream else response
    except requests.exceptions.RequestException as e:
        print(f"请求出错: {e}")
        return None


if __name__ == "__main__":
    print("Ollama聊天客户端 (输入'exit'退出)")
    while True:
        user_input = input("你: ")
        if user_input.lower() == 'exit':
            break

        response = chat_with_ollama(user_input, stream=True)  # 流式响应
        if response:
            print("AI: ", end="", flush=True)
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    print(chunk.decode('utf-8'), end="", flush=True)
            print()  # 换行
        else:
            print("获取响应失败，请检查API服务是否运行")
        # if response:
        #     print(f"AI: {response.get('response')}")
        # else:
        #     print("获取响应失败，请检查API服务是否运行")
