# LangChain Ollama Demo

这是一个使用LangChain和本地Ollama模型进行交互的演示项目。

## 环境要求

- Python 3.8+
- Ollama 服务

## 设置开发环境

1. 创建Python虚拟环境：
```bash
cd langchain-demo
python3 -m venv .venv
source .venv/bin/activate
```

2. 安装Python依赖包：
```bash
pip install langchain-community langchain-core langchain-ollama
```

## 部署Ollama

1. 安装Ollama（MacOS）：
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

2. 下载并运行模型（例如llama2和deepseek）：
```bash
ollama pull qwen3
ollama pull deepseek-r1:14b
```

3. 启动Ollama服务：
```bash
ollama serve
```

## 运行演示

```bash
python ollama_chat_demo.py
```

## 项目结构

- `ollama_chat_demo.py` - 主演示文件
- `.gitignore` - Git忽略规则
