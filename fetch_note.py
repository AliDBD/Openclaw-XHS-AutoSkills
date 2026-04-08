import requests
import json
import os
import sys

def fetch_note(url):
    cookie_path = "/root/.openclaw/openclaw-weixin/secrets/xhs_cookie"
    if not os.path.exists(cookie_path):
        print("Error: Missing Cookie.")
        return
        
    with open(cookie_path, 'r') as f:
        cookie = f.read().strip()
    
    note_id = url.split("/")[-1].split("?")[0]
    api_url = "https://edith.xiaohongshu.com/api/sns/web/v1/feed"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
        "Cookie": cookie,
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "https://www.xiaohongshu.com",
        "Referer": f"https://www.xiaohongshu.com/explore/{note_id}"
    }
    
    try:
        resp = requests.post(api_url, headers=headers, json={"source_note_id": note_id}, timeout=10)
        data = resp.json()
        
        if data.get("code") == 0:
             note = data.get("data", {}).get("items", [{}])[0].get("note_card", {})
             print(json.dumps({
                 "title": note.get("title", ""),
                 "desc": note.get("desc", ""),
                 "images": [img.get("url_default") for img in note.get("image_list", [])]
             }, ensure_ascii=False))
        else:
             print(json.dumps({
                 "title": "触发验证码/风控",
                 "desc": f"小红书 API 返回 code {data.get('code')}。单凭 Cookie 无法绕过当前服务器 IP 的风控。建议老板直接发笔记截图。",
                 "images": []
             }, ensure_ascii=False))

    except Exception as e:
        print(f"Exception: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        fetch_note(sys.argv[1])
