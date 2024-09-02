FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y python3.9 python3-pip curl && \
    rm -rf /var/lib/apt/lists/*

RUN pip install playwright==1.44.0
# 安装浏览器和操作系统依赖项
RUN python3 -m playwright install --with-deps chromium

# 安装chrome
RUN curl -fsSL https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome-archive-keyring.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/google-chrome-archive-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" | tee /etc/apt/sources.list.d/google-chrome.list && \
    apt-get -y update && \
    apt-get -y install google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /plugin

ARG LIBRARY="-i https://pypi.tuna.tsinghua.edu.cn/simple"

COPY requirements.txt /plugin

RUN pip install -r requirements.txt ${LIBRARY}

COPY . /plugin

ARG PORT=8000

EXPOSE ${PORT}

ENV PORT=${PORT} WORKERS=4

CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port $PORT --workers $WORKERS"]