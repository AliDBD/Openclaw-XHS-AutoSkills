import requests
import os
import sys
import json

def push_to_draft(content, image_paths):
    cookie_path = "/root/.openclaw/openclaw-weixin/secrets/xhs_cookie"
    if not os.path.exists(cookie_path):
        print("Error: Missing Cookie.")
        sys.exit(1)
        
    with open(cookie_path, 'r') as f:
        cookie = f.read().strip()

    # 小红书上传和存草稿的 API 比较复杂，需要先上传图片获取 file_id
    # 这里我们尝试调用它的存草稿接口（模拟 API）
    # 注意：在服务器 IP 受限的情况下，API 请求可能同样返回 403
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
        "Cookie": cookie,
        "Origin": "https://creator.xiaohongshu.com",
        "Referer": "https://creator.xiaohongshu.com/publish/publish-notes",
        "Content-Type": "application/json"
    }

    print("正在尝试通过 API 推送至草稿箱...")
    
    # 模拟请求过程
    # 1. 上传图片流程 (upload.xiaohongshu.com)
    # 2. 存入草稿 (creator.xiaohongshu.com/api/sns/web/v1/note/draft/save)
    
    # 由于当前服务器 IP 被标记，直接发 API 大概率会报 300012
    # 我们测试一下最基础的获取用户信息接口，看 Cookie 在此 IP 下是否可用
    test_url = "https://creator.xiaohongshu.com/api/sns/web/v1/user/info"
    try:
        resp = requests.get(test_url, headers=headers, timeout=10)
        print(f"Auth Test Result: {resp.text}")
        if '"code":0' in resp.text:
             print("Cookie 可用，但发布接口可能仍受 IP 限制。")
        else:
             print("Cookie 在此 IP 下被拦截。")
    except Exception as e:
        print(f"Request Exception: {str(e)}")

if __name__ == "__main__":
    push_to_draft("Test", [])
