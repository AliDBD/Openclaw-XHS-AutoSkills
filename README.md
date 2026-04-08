# Openclaw-XHS-AutoSkills 🚀

让你的 OpenClaw 进化为小红书全自动运营专家。从图片识别到素材生产，再到浏览器自动化发布，一气呵成。

## 🌟 核心能力
1. **视觉驱动**：发送产品原图，AI 自动生成爆款标题、正文及 Tag。
2. **商业级配图**：联动 `social-media-marketing` 同步产出 4 张不同角度（侧面、正面、俯视、实景）的高清商业大片。
3. **真人模拟发布**：通过 Playwright/CDP 自动化操控内置 Chromium 浏览器，完美规避 API 限制。
4. **低频稳健运营**：支持登录态自动检测，过期自动提醒老板扫码，确保账号绝对安全。

## 🛠 如何复刻到你的小龙虾 (OpenClaw)

### 1. 环境准备
确保你的 OpenClaw 环境已安装 Chromium。如果是 Root 环境运行，请修改 `openclaw.json`：
```json
"browser": {
  "noSandbox": true
}
```

### 2. 安装技能
在你的 OpenClaw 终端执行：
```bash
clawhub install https://github.com/AliDBD/Openclaw-XHS-AutoSkills
```

### 3. 首次扫码
直接对小薇说“**运营小红书**”，在弹出的窗口或微信截图中完成首次扫码登录，身份令牌将安全加密保存在本地。

## 📁 目录结构
- `SKILL.md`: 核心运营逻辑 SOP。
- `scripts/`: 包含内容抓取及发布增强脚本。
- `_meta.json`: 技能定义文件。

---
*Powered by 小薇 🌸 - 基于 OpenClaw 架构开发*
