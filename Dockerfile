# 使用官方的轻量级 Python 环境
FROM python:3.11-slim

# 在容器里建一个叫 /app 的文件夹
WORKDIR /app

# 把你的代码复制进容器
COPY server.py .
COPY index.html .
COPY konva.min.js .

# 暴露 8000 端口
EXPOSE 8000

# 启动容器时运行你的代码
CMD ["python", "server.py"]