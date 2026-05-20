import os
import torch
import faiss
import numpy as np
from PIL import Image
from fastapi import FastAPI, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
from transformers import ChineseCLIPModel, ChineseCLIPProcessor

# ---------- 配置 ----------
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
LOCAL_MODEL_PATH = "chineseclip"  # 你的 Chinese-CLIP 本地路径
VEC_FILE = "second.pt"  # 保存的 torch 向量文件（可选，未直接使用）
FAISS_FILE = "second.faiss"  # FAISS 索引文件
POEM_LIST_FILE = "second.txt"  # 诗句列表文件
TOP_K_DEFAULT = 30  # 默认返回 top-k 条结果

# ---------- 加载模型 ----------
print("加载模型...")
model = ChineseCLIPModel.from_pretrained(LOCAL_MODEL_PATH).to(DEVICE)
processor = ChineseCLIPProcessor.from_pretrained(LOCAL_MODEL_PATH)
model.eval()

# ---------- 加载索引和诗句列表 ----------
print("加载 FAISS 索引...")
index = faiss.read_index(FAISS_FILE)

print("加载诗句列表...")
with open(POEM_LIST_FILE, "r", encoding="utf-8") as f:
    poem_list = [line.strip() for line in f]

print(f"准备就绪，共 {len(poem_list)} 句诗，设备：{DEVICE}")

# ---------- FastAPI 应用 ----------
app = FastAPI(title="中文诗歌检索 API", description="根据图片检索最相近的诗句")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境请替换为具体前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def search_poem(image: Image.Image, topk: int = TOP_K_DEFAULT):
    """检索相似诗句，返回列表"""
    # 图片预处理
    img_inputs = processor(images=image, return_tensors="pt").to(DEVICE)
    with torch.no_grad():
        img_feature = model.get_image_features(**img_inputs)
        if hasattr(img_feature, 'pooler_output'):
            img_feature = img_feature.pooler_output
        img_feature = img_feature / img_feature.norm(p=2, dim=-1, keepdim=True)
    query_vec = img_feature.cpu().numpy().astype('float32')
    scores, ids = index.search(query_vec, topk)
    results = []
    for i in range(topk):
        idx = ids[0][i]
        score = float(scores[0][i])
        results.append({
            "poem": poem_list[idx],
            "similarity": round(score, 4)
        })
    return results


@app.post("/search")
async def search(
        file: UploadFile = File(..., description="要检索的图片文件"),
        topk: int = Query(TOP_K_DEFAULT, ge=1, le=100, description="返回结果数量")
):
    """上传图片，返回最相似的诗句列表"""
    try:
        # 读取并验证图片
        image = Image.open(file.file).convert("RGB")
    except Exception:
        return {"error": "无效的图片文件"}

    results = search_poem(image, topk)
    return {"results": results}


@app.get("/health")
def health():
    return {"status": "ok", "poem_count": len(poem_list)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)