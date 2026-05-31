# PersonalAutonomy

Multi-tenant AI agent platform that gives non-technical users personalized AI workspaces via a web chat interface.

## What It Does

Create Linux-isolated workspaces per user — each with its own agent role, skills, and tools. Users chat with their AI agents through a browser. Admins manage everything from a web panel.

Built on a fork of [OpenCode Portal](https://github.com/hosenur/portal).

## Architecture

```
User → Vercel (React frontend) → VPS (Nitro API + PostgreSQL) → Workspace (OpenCode process)
```

- **Frontend:** React 19, Tailwind CSS, React Router, IntentUI — hosted on Vercel
- **Backend:** Nitro (Bun) API on VPS, JWT auth, SSE streaming
- **Database:** PostgreSQL 16 + Drizzle ORM
- **AI Engine:** OpenCode SDK — one process per user, resource-limited
- **Isolation:** Linux users (`ws-*`), per-user directories, `chmod 700`, POSIX resource limits

## Key Features

- **Multi-tenant** — each user gets a sandboxed workspace with its own OpenCode process
- **Role templates** — pre-configured agent packages (marketing-agent, historian, etc.) with custom skills and MCP servers
- **Admin panel** — user/workspace/session management, audit logs, file browser
- **SSE streaming** — real-time agent responses with reconnection
- **Security** — no root processes, bcrypt passwords, rate limiting, JWT auth, soft-delete

## Project Status

Early development. See `docs/superpowers/plans/` for implementation plan and `docs/superpowers/specs/` for design doc.

## Deploy

1. Fork `hosenur/portal`
2. Set up a VPS (Ubuntu 24.04) with Docker for PostgreSQL
3. Install Bun, PM2, Nginx, OpenCode CLI
4. Copy `.env.example` to `.env`, fill secrets
5. Run `bun install` + `bun run build`
6. Push migrations with `bun drizzle-kit migrate`
7. Deploy frontend to Vercel, backend via PM2 on VPS

Full setup guide: `docs/superpowers/plans/2026-05-27-personalautonomy-plan.md`

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 19, React Router, IntentUI, Tailwind CSS |
| Backend | Nitro (Bun), Drizzle ORM |
| Database | PostgreSQL 16 |
| AI Engine | OpenCode SDK |
| Reverse Proxy | Nginx |
| Process Manager | PM2 |
| Hosting | Vercel (frontend) + VPS (backend) |
| CI/CD | GitHub Actions |

## License

MIT
