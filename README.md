# OpenClaw DevFlow Starter

一个用于 OpenClaw 自动开发流程的最小全栈模板：
- 前端：`public/index.html`
- 后端：Vercel Python Functions（`api/*.py`）
- 数据库：SQLite（演示环境，文件位于 `/tmp`）

## API
- `GET /api/health`
- `GET /api/tasks`
- `POST /api/tasks` `{ "title": "..." }`

## 注意
Vercel Serverless 上 SQLite 放在 `/tmp`，仅适合演示与验收流程，不保证长期持久化。
生产建议切换到 Turso/Supabase。
