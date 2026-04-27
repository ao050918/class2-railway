from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import openai
import os

app = FastAPI()

# 挂载静态文件夹
app.mount("/static", StaticFiles(directory="static"), name="static")

# 阿里云百炼 API 密钥
api_key = os.getenv("DASHSCOPE_API_KEY")
client = openai.OpenAI(
    api_key=api_key,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)


# 主页
@app.get("/", response_class=HTMLResponse)
async def home():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()


# 聊天接口
@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    message = data.get("message", "")

    completion = client.chat.completions.create(
        model="qwen-turbo",
        messages=[{"role": "user", "content": message}]
    )
    reply = completion.choices[0].message.content
    return {"reply": reply}