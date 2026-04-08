#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_images.py — OpenClaw 社媒营销技能：商业配图生成脚本
用法：python3 generate_images.py <prompt_file_path> <user_image_path>

- prompt_file_path : 包含 4 行 prompt 的文本文件，每行一条（/tmp/marketing_prompts.txt）
- user_image_path  : 用户上传的产品原图路径

生成的 4 张图片固定保存至：
  /root/.openclaw/openclaw-weixin/output/marketing_img_1.png
  /root/.openclaw/openclaw-weixin/output/marketing_img_2.png
  /root/.openclaw/openclaw-weixin/output/marketing_img_3.png
  /root/.openclaw/openclaw-weixin/output/marketing_img_4.png
"""

import asyncio
import aiohttp
import sys
import os
import base64
import glob
from dotenv import load_dotenv

# ── 常量配置 ──────────────────────────────────────────────────────────────────

ENV_FILE   = "/root/.openclaw/openclaw-weixin/.env"
OUTPUT_DIR = "/root/.openclaw/openclaw-weixin/output"
API_URL_TMPL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.5-flash-image:generateContent?key={api_key}"
)
MAX_RETRIES  = 3
REQUEST_TIMEOUT = aiohttp.ClientTimeout(total=120)

# ── 工具函数 ──────────────────────────────────────────────────────────────────

def load_api_key() -> str:
    """从 .env 文件加载 IMAGE_API_KEY。"""
    load_dotenv(ENV_FILE)
    key = os.getenv("IMAGE_API_KEY", "").strip()
    if not key:
        raise EnvironmentError(
            f"未找到 IMAGE_API_KEY，请检查 {ENV_FILE} 中是否已配置该变量。"
        )
    return key


def read_prompts(prompt_file: str) -> list[str]:
    """读取 prompt 文件，每行一条，返回前 4 条非空行。"""
    if not os.path.isfile(prompt_file):
        raise FileNotFoundError(f"Prompt 文件不存在：{prompt_file}")
    with open(prompt_file, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    if len(lines) < 4:
        raise ValueError(
            f"Prompt 文件中有效行数不足 4 条（当前 {len(lines)} 条）：{prompt_file}"
        )
    return lines[:4]


def image_to_base64(image_path: str) -> tuple[str, str]:
    """
    将图片文件转为 base64 字符串，同时推断 MIME 类型。
    返回 (base64_data, mime_type)。
    """
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"原图文件不存在：{image_path}")

    ext = os.path.splitext(image_path)[1].lower()
    mime_map = {
        ".jpg":  "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png":  "image/png",
        ".webp": "image/webp",
        ".gif":  "image/gif",
    }
    mime_type = mime_map.get(ext, "image/jpeg")

    with open(image_path, "rb") as f:
        b64_data = base64.b64encode(f.read()).decode("utf-8")

    return b64_data, mime_type


def clear_output_dir():
    """清空 output 目录下的旧营销配图（marketing_img_*.png）。"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    old_files = glob.glob(os.path.join(OUTPUT_DIR, "marketing_img_*.png"))
    for f in old_files:
        try:
            os.remove(f)
        except OSError as e:
            print(f"[警告] 删除旧图片失败：{f} — {e}")
    if old_files:
        print(f"已清空 {len(old_files)} 张旧配图。")


# ── 核心异步逻辑 ──────────────────────────────────────────────────────────────

async def generate_single_image(
    session: aiohttp.ClientSession,
    api_key: str,
    prompt: str,
    img_b64: str,
    img_mime: str,
    index: int,
) -> str | None:
    """
    向 Gemini API 发送原图 + 文字 prompt，生成一张图片。
    成功时返回保存路径，失败时返回 None。
    支持最多 MAX_RETRIES 次重试。
    """
    output_path = os.path.join(OUTPUT_DIR, f"marketing_img_{index}.png")
    url = API_URL_TMPL.format(api_key=api_key)
    headers = {"Content-Type": "application/json"}

    payload = {
        "contents": [
            {
                "parts": [
                    # 1. 原图（inline base64）
                    {
                        "inlineData": {
                            "mimeType": img_mime,
                            "data": img_b64,
                        }
                    },
                    # 2. 文字 prompt
                    {"text": prompt},
                ]
            }
        ],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"]
        },
    }

    for attempt in range(1, MAX_RETRIES + 1):
        print(f"[图 {index}] 第 {attempt} 次请求中...")
        try:
            async with session.post(
                url, headers=headers, json=payload, timeout=REQUEST_TIMEOUT
            ) as resp:
                if resp.status != 200:
                    err_text = await resp.text()
                    raise RuntimeError(f"HTTP {resp.status}: {err_text[:300]}")

                data = await resp.json()
                candidates = data.get("candidates", [])
                if not candidates:
                    raise RuntimeError("API 返回结构异常：candidates 为空")

                parts = candidates[0].get("content", {}).get("parts", [])
                b64_img = None
                for part in parts:
                    inline = part.get("inlineData", {})
                    if inline.get("data"):
                        b64_img = inline["data"]
                        break

                if not b64_img:
                    # 打印文本部分便于调试
                    texts = [p.get("text", "") for p in parts if "text" in p]
                    raise RuntimeError(
                        f"返回结果中未找到图像数据。文本内容：{' | '.join(texts)[:200]}"
                    )

                image_bytes = base64.b64decode(b64_img)
                with open(output_path, "wb") as f:
                    f.write(image_bytes)

                print(f"[图 {index}] 生成成功 → {output_path}")
                return output_path

        except Exception as e:
            print(f"[图 {index}] 第 {attempt} 次失败：{e}")
            if attempt < MAX_RETRIES:
                wait_sec = 2 ** attempt  # 指数退避：2s, 4s
                print(f"[图 {index}] {wait_sec}s 后重试...")
                await asyncio.sleep(wait_sec)

    print(f"[图 {index}] 已达最大重试次数（{MAX_RETRIES}），放弃。")
    return None


async def main():
    # ── 参数校验 ──────────────────────────────────────────────────────────────
    if len(sys.argv) < 3:
        print("用法：python3 generate_images.py <prompt_file_path> <user_image_path>")
        print("示例：python3 generate_images.py /tmp/marketing_prompts.txt /tmp/product.jpg")
        sys.exit(1)

    prompt_file = sys.argv[1]
    user_image  = sys.argv[2]

    # ── 前置准备 ──────────────────────────────────────────────────────────────
    try:
        api_key = load_api_key()
    except EnvironmentError as e:
        print(f"[错误] {e}")
        sys.exit(1)

    try:
        prompts = read_prompts(prompt_file)
    except (FileNotFoundError, ValueError) as e:
        print(f"[错误] {e}")
        sys.exit(1)

    try:
        img_b64, img_mime = image_to_base64(user_image)
    except FileNotFoundError as e:
        print(f"[错误] {e}")
        sys.exit(1)

    clear_output_dir()

    print(f"读取到 {len(prompts)} 条 Prompt，原图 MIME：{img_mime}，开始并发生成 4 张配图...")

    # ── 并发生成 ──────────────────────────────────────────────────────────────
    async with aiohttp.ClientSession() as session:
        tasks = [
            generate_single_image(session, api_key, prompts[i], img_b64, img_mime, i + 1)
            for i in range(4)
        ]
        results = await asyncio.gather(*tasks)

    # ── 结果汇总 ──────────────────────────────────────────────────────────────
    success_paths = [r for r in results if r is not None]
    failed_count  = 4 - len(success_paths)

    print("\n── 生成结果汇总 ──────────────────────────────────────────────────")
    for path in success_paths:
        print(f"  ✓ {path}")
    if failed_count:
        print(f"  ✗ {failed_count} 张图片生成失败")
    print("──────────────────────────────────────────────────────────────────")

    if len(success_paths) == 4:
        print("全部 4 张配图生成完毕。")
        sys.exit(0)
    else:
        print(f"仅成功生成 {len(success_paths)}/4 张图片，请检查日志。")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
