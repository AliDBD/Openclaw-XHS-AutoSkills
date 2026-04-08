---
name: xiaohongshu-auto-post
description: 小红书全自动运营SKILL。集成选题分析、爆款复刻、文案生成、图文发布及评论互动。
trigger:
  - 自动发小红书
  - 联动发布
  - 自动营销
  - 运营小红书
output: auto
force_sync: true
---

# 小红书全自动运营中心

本技能打通了素材生产（social-media-marketing）与自动化执行（xiaohongshu-ops）的链路。

## 0) 前置：账号与权限

- **优先路径**：使用内置浏览器 `openclaw` profile 自动操作小红书创作后台。首次使用需扫码登录。
- **备选路径**：若浏览器自动化受限，调用 Python 脚本（基于已配置的 Cookie）进行发布。

## 阶段一：选题与素材准备（联动）

1. **自动选题/复刻**：用户提供关键词或爆款链接后，参考 `xiaohongshu-ops` 的分析逻辑确定内容切入点。
2. **素材生成**：联动 `social-media-marketing` 生成：
   - 爆款文案（标题+正文+Tag）
   - 4张高商业质感配图
3. **确认素材**：将生成的素材发给老板预览。

## 阶段二：自动化发布链路（核心优化）

执行发布时，优先尝试 **浏览器模拟点击（CDP模式）** 以降低风控风险。

### 1. 浏览器自动化发布 (推荐)
- 流程引用：`~/.openclaw/skills/xiaohongshu-ops/references/xhs-publish-flows.md`
- 关键动作：
  1. 打开 `https://creator.xiaohongshu.com/publish/publish-notes`
  2. 自动上传 `/root/.openclaw/openclaw-weixin/output/marketing_img_{1,2,3,4}.png`
  3. 自动填入标题和正文。
  4. 默认停在「发布」按钮前，等待老板确认或由老板授权后直接点击。

### 2. 脚本API发布 (兜底)
- 若浏览器不可用，执行：`/root/.openclaw/openclaw-weixin/skills/xiaohongshu-auto-post/scripts/publish_note.py`

## 阶段三：发布后互动

1. **评论监听**：每天凌晨自检时，同步检查小红书最新评论。
2. **自动回复**：根据 `persona.md` 设定的语气进行回复。

## 阶段五：登录态维护（老板专属）

1. **自动识别过期**：如果执行发布时系统提示 `Login Required` 或跳转登录页，我不会盲目重试。
2. **主动索要授权**：我会第一时间截图当前浏览器的二维码发送给老板，并留言：「老板，小红书身份令牌过期啦，请临门扫一脚！扫完我接着干活。」
3. **静默等待**：在老板扫码成功前，发布任务会自动挂起，确保不触发平台的风险账号锁定。
