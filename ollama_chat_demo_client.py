import json

import requests

API_URL = "http://localhost:8000/chat"


def chat_with_ollama(message):
    """
    调用Ollama聊天API
    :param message: 用户输入的消息
    :return: API返回的响应内容
    """
    headers = {"Content-Type": "application/json"}
    data = {"message": message}

    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求出错: {e}")
        return None


if __name__ == "__main__":
    print("Ollama聊天客户端 (输入'exit'退出)")
    while True:
        user_input = input("你: ")
        if user_input.lower() == 'exit':
            break

        response = chat_with_ollama(user_input)
        if response:
            print(f"AI: {response.get('response')}")
        else:
            print("获取响应失败，请检查API服务是否运行")
