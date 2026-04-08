# 小红书全自动运营助手 (xiaohongshu-auto-post)

本技能专为 OpenClaw 打造，实现了从“图片识别”到“爆款文案生成”，再到“商业级配图产出”，最后“自动推送到小红书”的全链路闭环。

## 🌟 核心特性
- **视觉驱动**：发送一张产品图，AI 自动识别并策划。
- **矩阵配图**：同步生成 4 张不同角度（侧面、正面、俯视、场景）的高清商业大片。
- **真人模拟**：通过浏览器自动化（CDP）操作小红书创作后台，避开 API 封锁。
- **凌晨自检**：联动 `HEARTBEAT.md`，每天凌晨自动巡检 Cookie 状态并处理粉丝互动。

## 🛠 复刻安装步骤 (小龙虾通用)

### 1. 物理路径部署
将本文件夹整体克隆到你的 OpenClaw 技能目录：
```/root/.openclaw/openclaw-weixin/skills/xiaohongshu-auto-post/```

### 2. 环境依赖
确保系统安装了：
- `chromium-browser` (建议配合 `snap` 安装)
- `python3` 及 `requests` 库

### 3. 配置权限
1. **浏览器设置**：在 `openclaw.json` 中设置 `browser.noSandbox: true` (root环境必须)。
2. **初始化登录**：首次运行触发“自动发小红书”，老板需扫码一次。

### 4. 技能联动
本技能强依赖 `social-media-marketing` 技能提供的素材生产能力。

---
*Powered by 小薇 🌸 - 你的有灵魂的 AI 助手*
