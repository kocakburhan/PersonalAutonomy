# PersonalAutonomy Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a multi-tenant web platform on top of forked OpenCode Portal that provides non-technical users with personalized AI agent workspaces via a web chat interface.

**Architecture:** Fork hosenur/portal (React 19 + Nitro + OpenCode SDK + Tailwind), extend with PostgreSQL + Drizzle ORM for auth/users/workspaces, add JWT-based auth, per-user POSIX-isolated workspace directories with resource limits, and a full admin panel.

**Tech Stack:** React 19, React Router, IntentUI, Tailwind CSS, Nitro (Bun), Drizzle ORM, PostgreSQL 16, OpenCode SDK, PM2, Nginx, Docker

**Spec:** `docs/superpowers/specs/2026-05-27-personalautonomy-design.md`

> **NOT (important!!!):** Bu plandaki tüm kodlar tamamen referans olması içindir. Proje geliştirilirken yazılacak olan kodların tamamı projenin o anki durumuna, mevcut kod yapısına ve bağımlılık versiyonlarına göre yazılmalıdır. Buradaki kodlar yalnızca mimarinin anlaşılması ve implementasyon sırasında referans alınması içindir.

---

## Implementasyona Başlamadan Önce Yapılacaklar

> **Önemli:** Bu bölümdeki tüm maddeler kod yazmaya başlamadan **önce** tamamlanmalıdır. Bunlar senin manuel olarak yapman gereken işlemlerdir — agent otomatik yapamaz.

### 1. GitHub: Fork Portal Repository

- [ ] **1a.** Tarayıcıdan https://github.com/hosenur/portal adresine git
- [ ] **1b.** Sağ üstte **"Fork"** butonuna tıkla → **"Create fork"**
- [ ] **1c.** Fork tamamlanınca `https://github.com/KULLANICIADIN/portal` adresinde fork'un oluştu
- [ ] **1d.** Fork Settings → Default branch'in `main` olduğundan emin ol
- [ ] **1e.** Lokale clone: `git clone https://github.com/kocakburhan/portal.git D:\Projects\PersonalAutonomy`

### 2. VPS: Satın Al ve Temel Kurulum

- [ ] **2a.** [Hetzner Cloud](https://hetzner.com/cloud) hesabı aç
- [ ] **2b.** **"Add Server"** → şu ayarlarla sunucu oluştur:
  - Location: **Nuremberg** veya **Falkenstein** (Almanya)
  - Image: **Ubuntu 24.04 LTS**
  - Type: **CX22** (2 vCPU, 4 GB RAM, 40 GB SSD, 20 TB trafik, ~4€/ay)
  - IPv4: **Açık**
- [ ] **2c.** Sunucu IP adresini ve root şifresini kaydet
- [ ] **2d.** VPS'e SSH ile bağlan ve aşağıdaki temel kurulumları yap (Task 6.0):
  - `apt update && apt upgrade -y`
  - Zaman dilimi: `timedatectl set-timezone Europe/Istanbul`
  - Hostname: `hostnamectl set-hostname pa-vps`
  - Swap: 2 GB oluştur
  - SSH güvenliği: `PermitRootLogin prohibit-password`, `PasswordAuthentication no`
  - `nitro-runner` sistem kullanıcısı oluştur
  - Gerekli yazılımları kur: Docker, Docker Compose, Bun, OpenCode, PM2, Nginx, certbot, git, curl, unzip, cron
  - Dizin yapısını oluştur: `/opt/personalautonomy/`, `/opt/personalautonomy/workspaces/`, `/opt/personalautonomy/templates/roles/`, `/opt/personalautonomy/scripts/`, `/opt/personalautonomy/logs/`, `/opt/backups/db/`
  - UFW firewall: 22, 80, 443 aç; 5432 kapat

### 3. Domain ve DNS

- [ ] **3a.** Domain satın al (Namecheap, Cloudflare, GoDaddy vb.) → örn: `personalautonomy.com`
- [ ] **3b.** DNS yönetiminde A kaydı ekle: `api.SITEN.COM → VPS_IP_ADRESI`
- [ ] **3c.** DNS yönetiminde A kaydı ekle (frontend Vercel'de olacaksa): `SITEN.COM → Vercel IP` veya CNAME
- [ ] **3d.** DNS propagation'ı bekle (5-30 dk) → `nslookup api.SITEN.COM` ile doğrula

### 4. Kendi Bilgisayarında (Windows) SSH + rclone

- [ ] **4a.** OpenSSH Client'ın yüklü olduğunu doğrula:
  ```powershell
  Get-WindowsCapability -Online | Where-Object Name -like "OpenSSH.Client*"
  ```
  `State: NotPresent` ise: `Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0`
- [ ] **4b.** VPS için SSH anahtarı oluştur:
  ```powershell
  ssh-keygen -t ed25519 -f "$env:USERPROFILE\.ssh\vps_root" -N '""'
  ```
- [ ] **4c.** Açık anahtarı Hetzner panelinde SSH Keys'e ekle:
  - `Get-Content "$env:USERPROFILE\.ssh\vps_root.pub"` → çıkan metni kopyala
  - Hetzner Cloud Console → SSH Keys → Add SSH Key → Name: `kendi-pc`, Key: kopyaladığın anahtar
  - VPS sunucusunu Rebuild et (SSH Key: `kendi-pc` seçili)
- [ ] **4d.** Şifresiz bağlantıyı test et: `ssh -i "$env:USERPROFILE\.ssh\vps_root" root@VPS_IP "echo OK"`
- [ ] **4e.** SSH config dosyasına kolay bağlantı ekle:
  ```powershell
  @"
  Host pa-vps
      HostName VPS_IP_ADRESI
      User root
      IdentityFile ~/.ssh/vps_root
  "@ | Out-File -Append "$env:USERPROFILE\.ssh\config"
  ```
- [ ] **4f.** rclone kur: `winget install rclone` → `rclone version` ile doğrula
- [ ] **4g.** rclone'ı VPS'e bağlanacak şekilde yapılandır (`rclone config`):
  - Remote name: `vps`
  - Storage type: `sftp`
  - Host: VPS IP adresi
  - User: `root`
  - key_file: `C:\Users\KULLANICIADIN\.ssh\vps_yedek` (Task 6.2'deki yedek anahtarı)
- [ ] **4h.** rclone bağlantısını test et: `rclone lsd vps:/opt`

### 5. CI/CD ve Servis Hesapları (Ücretsiz)

- [ ] **5a.** [Vercel](https://vercel.com) hesabı aç (GitHub ile sign up)
- [ ] **5b.** Vercel'de token oluştur: Settings → Tokens → Create Token → adı `personalautonomy-ci` → token'ı kaydet
- [ ] **5c.** [UptimeRobot](https://uptimerobot.com) hesabı aç (Google ile sign up) → monitoring için
- [ ] **5d.** [healthchecks.io](https://healthchecks.io) hesabı aç (email ile sign up) → cron monitoring için

### 6. Telegram Uyarı Botu (Opsiyonel — Alarmlar İçin Önerilir)

- [ ] **6a.** Telegram'da `@BotFather` ile bot oluştur:
  - `/start` → `/newbot` → isim ver (örn: `PersonalAutonomy Uyari`) → kullanıcı adı ver (örn: `pa_uyari_bot`)
  - BotFather'ın verdiği **token'ı** kaydet
- [ ] **6b.** Yeni bot'una mesaj at (`/start` veya "merhaba")
- [ ] **6c.** Chat ID'ni öğren: tarayıcıdan `https://api.telegram.org/botTOKEN/getUpdates` → `"chat":{"id":123456789}` → bu numarayı kaydet
- [ ] **6d.** UptimeRobot'a Telegram entegrasyonu ekle (Alert Contacts → Telegram → Token + Chat ID)
- [ ] **6e.** healthchecks.io'ya Telegram entegrasyonu ekle (Integrations → Telegram → Token + Chat ID)

### 7. GitHub Secrets (Settings → Secrets and variables → Actions)

- [ ] **7a.** `VPS_HOST` → VPS IP adresi (örn: `5.161.142.10`)
- [ ] **7b.** `VPS_USER` → `root`
- [ ] **7c.** `VPS_SSH_KEY` → `vps_root` özel anahtarının **tam içeriği** (`Get-Content "$env:USERPROFILE\.ssh\vps_root"`)
- [ ] **7d.** `VERCEL_TOKEN` → Adım 5b'de oluşturduğun Vercel token

### 8. Karar Verilmesi Gereken Değerler (`.env` için)

| Değişken | Açıklama | Örnek |
|----------|----------|-------|
| `DB_PASSWORD` | PostgreSQL şifresi (güçlü olsun) | `r4nd0m-s3cur3-p4ss` |
| `DATABASE_URL` | PostgreSQL bağlantı URL'i | `postgresql://postgres:PAROLA@localhost:5432/personalautonomy` |
| `JWT_SECRET` | 64 karakter rastgele string | `openssl rand -base64 64` ile üret |
| `VITE_API_URL` | Production'da API adresi | `https://api.SITEN.COM` |
| `OPENCODE_PATH` | OpenCode binary yolu | `/usr/local/bin/opencode` |
| `WORKSPACES_ROOT` | Workspace dizinleri root | `/opt/personalautonomy/workspaces` |
| `TEMPLATES_ROOT` | Rol template dizini | `./templates/roles` |
| `WORKSPACE_SCRIPT_PATH` | Workspace script yolu | `/opt/personalautonomy/scripts/manage-workspace.sh` |
| `MINIMAX_API_KEY` | Görsel üretimi için (Task 7.9) | Minimax API key (sonradan eklenecek) |

- [ ] **8a.** `JWT_SECRET` üret: VPS'te `openssl rand -base64 64` veya lokalde PowerShell ile rastgele string oluştur
- [ ] **8b.** `DB_PASSWORD` belirle (güçlü, en az 16 karakter)

### 9. Ön Kontrol Listesi (Her Şey Tamam mı?)

Kod yazmaya başlamadan önce aşağıdakilerin hepsi **✅** olmalı:

| # | Kontrol | Durum |
|---|---------|-------|
| 1 | Portal fork'landı ve lokale clone'landı | ☐ |
| 2 | VPS satın alındı, IP ve root erişimi hazır | ☐ |
| 3 | VPS temel kurulumları yapıldı (yazılımlar, dizinler, firewall) | ☐ |
| 4 | Domain satın alındı, DNS A kaydı eklendi | ☐ |
| 5 | SSH anahtarı oluşturuldu, VPS'e şifresiz bağlanılıyor | ☐ |
| 6 | rclone kuruldu ve VPS bağlantısı test edildi | ☐ |
| 7 | Vercel hesabı açıldı, token alındı | ☐ |
| 8 | UptimeRobot hesabı açıldı | ☐ |
| 9 | healthchecks.io hesabı açıldı | ☐ |
| 10 | Telegram bot oluşturuldu, token + chat ID kaydedildi | ☐ |
| 11 | GitHub Secrets (VPS_HOST, VPS_USER, VPS_SSH_KEY, VERCEL_TOKEN) eklendi | ☐ |
| 12 | `.env` değerleri (DB_PASSWORD, JWT_SECRET, VITE_API_URL) belirlendi | ☐ |

> **Tahmini süre:** Tüm bu adımlar 1-2 saat sürer (VPS kurulumu + DNS propagation bekleme süresi dahil).

---

## File Structure

> **Note:** Portal'da Nitro v3 server kodu `apps/web/src/server/` altındadır (eski `apps/web/server/` değil). Bu plandaki tüm server dosya yolları bu yapıya göredir. Portal'ın mevcut OpenCode proxy route'ları `src/server/opencode/` altında korunur, yeni route'lar yanına eklenir.

```
portal/                                    (fork of hosenur/portal)
├── apps/web/
│   ├── src/server/                        # Nitro API layer (NEW — portal uses src/server/, not server/)
│   │   ├── api/
│   │   │   ├── auth/
│   │   │   │   ├── login.post.ts
│   │   │   │   ├── me.get.ts
│   │   │   │   └── logout.post.ts
│   │   │   ├── users/
│   │   │   │   ├── index.get.ts           # Admin: list all
│   │   │   │   ├── index.post.ts          # Admin: create user
│   │   │   │   └── [id].ts                # Admin: get/update/delete user
│   │   │   ├── workspaces/
│   │   │   │   ├── index.get.ts
│   │   │   │   └── [id].ts
│   │   │   ├── sessions/
│   │   │   │   ├── start.post.ts
│   │   │   │   ├── [id]/
│   │   │   │   │   ├── index.get.ts
│   │   │   │   │   ├── message.post.ts
│   │   │   │   │   ├── stream.get.ts
│   │   │   │   │   └── index.delete.ts
│   │   │   │   └── index.get.ts           # Admin: list all sessions
│   │   │   ├── admin/
│   │   │   │   ├── logs.get.ts
│   │   │   │   ├── files.get.ts
│   │   │   │   ├── stats.get.ts
│   │   │   │   ├── roles/
│   │   │   │   │   ├── index.get.ts
│   │   │   │   │   ├── index.post.ts
│   │   │   │   │   └── [id].ts
│   │   │   │   └── users/
│   │   │   │       └── [id]/
│   │   │   │           ├── workspace-files.get.ts
│   │   │   │           └── workspace-files/
│   │   │   │               └── index.put.ts
│   │   │   └── health.get.ts
│   │   ├── middleware/
│   │   │   ├── auth.ts                    # JWT verification
│   │   │   └── admin.ts                   # Role check
│   │   ├── services/
│   │   │   ├── workspace-manager.ts       # Linux user/dir management
│   │   │   ├── opencode-manager.ts        # Process spawn, SDK, resource limits
│   │   │   ├── session-manager.ts         # Session lifecycle
│   │   │   └── audit-logger.ts            # Audit trail
│   │   ├── db/
│   │   │   ├── index.ts                   # Drizzle connection + client
│   │   │   └── schema.ts                  # All table definitions
│   │   ├── lib/
│   │   │   └── opencode-client.ts          # OpenCode SDK wrapper (NEW)
│   │   └── utils/
│   │       ├── password.ts                # bcrypt hash/verify
│   │       ├── jwt.ts                     # JWT sign/verify
│   │       └── rate-limit.ts              # Login rate limiter
│   └── src/
│       ├── routes/
│       │   ├── login.tsx                  # Login page (NEW)
│       │   ├── chat.tsx                   # Chat page (MODIFIED - add auth)
│       │   └── admin/
│       │       ├── index.tsx              # Admin dashboard (NEW)
│       │       ├── users.tsx              # User management (NEW)
│       │       ├── roles.tsx              # Role management (NEW)
│       │       ├── sessions.tsx           # Session monitor (NEW)
│       │       ├── logs.tsx               # Log viewer (NEW)
│       │       └── files.tsx              # File browser (NEW)
│       ├── components/
│       │   ├── auth/
│       │   │   ├── login-form.tsx         (NEW)
│       │   │   └── protected-route.tsx    (NEW)
│       │   ├── layout/
│       │   │   ├── app-header.tsx         (NEW - user info, logout)
│       │   │   └── session-sidebar.tsx    (NEW - session list)
│       │   └── admin/
│       │       ├── admin-layout.tsx       (NEW)
│       │       ├── user-table.tsx         (NEW)
│       │       ├── user-form.tsx          (NEW)
│       │       ├── session-table.tsx      (NEW)
│       │       └── log-viewer.tsx         (NEW)
│       ├── context/
│       │   └── auth-context.tsx           (NEW)
│       └── lib/
│           ├── api-client.ts              (NEW - fetch wrapper with JWT)
│           └── sse-client.ts              (NEW - SSE with reconnect)
├── scripts/
│   └── manage-workspace.sh               (NEW - sudoers wrapper)
├── templates/
│   └── roles/
│       ├── admin/
│       │   ├── AGENTS.md
│       │   └── mcps.json
│       └── marketing-agent/
│           ├── AGENTS.md
│           ├── skills/
│           └── mcps.json
├── docker-compose.yml                     (NEW - PostgreSQL only)
├── nginx/
│   └── api.conf                           (NEW)
├── ecosystem.config.cjs                   (NEW - PM2 config)
├── .env.example                           (NEW)
├── drizzle.config.ts                      (NEW)
└── package.json                           (MODIFIED - add deps)
```

---

## Phase 1: Project Foundation

### Task 1.1: Fork Portal and Initialize Project

**Files:**
- Clone: fork of `hosenur/portal` into workspace
- Create: `drizzle.config.ts`
- Create: `.env.example`
- Modify: `apps/web/package.json`

- [ ] **Step 0: Fork the portal repository (1 kerelik, sen yapacaksın)**

1. Tarayıcıdan https://github.com/hosenur/portal adresine git
2. Sağ üstte **"Fork"** butonuna tıkla → **"Create fork"**
3. Fork tamamlanınca `https://github.com/KULLANICIADIN/portal` adresinde senin fork'un olacak
4. **ÖNEMLİ:** Fork'tan sonra GitHub'da Settings → "Default branch" ayarının `main` olduğundan emin ol

- [ ] **Step 1: Clone the portal fork**

```bash
git clone https://github.com/kocakburhan/portal.git D:\Projects\PersonalAutonomy
```

> `KULLANICIADIN` yerine kendi GitHub kullanıcı adını yaz. Fork'u oluşturduktan sonra bu URL çalışacak.

- [ ] **Step 2: Install Bun dependencies**

```bash
cd D:\Projects\PersonalAutonomy
bun install
```

- [ ] **Step 3: Add new dependencies**

```bash
bun add drizzle-orm postgres
bun add -d drizzle-kit @types/bcryptjs
```

- [ ] **Step 4: Create `drizzle.config.ts`** in project root

```typescript
import { defineConfig } from "drizzle-kit";

export default defineConfig({
  schema: "./apps/web/src/server/db/schema.ts",
  out: "./apps/web/src/server/db/migrations",
  dialect: "postgresql",
  dbCredentials: {
    url: process.env.DATABASE_URL!,
  },
});
```

- [ ] **Step 5: Create `.env.example`**

```env
DB_PASSWORD=password
DATABASE_URL=postgresql://postgres:password@localhost:5432/personalautonomy
JWT_SECRET=change-me-to-random-64-chars
OPENCODE_PATH=/usr/local/bin/opencode
WORKSPACES_ROOT=/opt/personalautonomy/workspaces
TEMPLATES_ROOT=./templates/roles
WORKSPACE_SCRIPT_PATH=/opt/personalautonomy/scripts/manage-workspace.sh
VITE_API_URL=http://localhost:3000
```

> **.env dosyasını oluştur:** `.env.example`'ı kopyalayıp değerleri kendi ortamına göre doldur:
> ```bash
> cp .env.example .env
> # Şimdi .env dosyasını aç ve şu değerleri gerçek bilgilerinle değiştir:
> #   DB_PASSWORD → güçlü bir şifre
> #   JWT_SECRET → rastgele 64 karakter (openssl rand -base64 64 ile üretebilirsin)
> #   VITE_API_URL → production'da https://api.PERSONALAUTONOMY.COM
> ```

- [ ] **Step 6: Verify project builds**

```bash
bun run build
```
Expected: Build succeeds.

- [ ] **Step 7: Commit**

```bash
git add -A
git commit -m "chore: initialize project with drizzle-orm and env config"
```

---

### Task 1.2: Database Schema

**Files:**
- Create: `apps/web/src/server/db/schema.ts`
- Create: `apps/web/src/server/db/index.ts`

- [ ] **Step 1: Write the full Drizzle schema**

Create `apps/web/src/server/db/schema.ts`:

```typescript
import {
  pgTable,
  uuid,
  varchar,
  text,
  boolean,
  timestamp,
  jsonb,
  serial,
  integer,
  bigint,
  uniqueIndex,
  index,
} from "drizzle-orm/pg-core";
import { relations } from "drizzle-orm";

export const roles = pgTable("roles", {
  id: serial("id").primaryKey(),
  name: varchar("name", { length: 50 }).notNull().unique(),
  description: text("description"),
  templatePath: varchar("template_path", { length: 255 }).notNull(),
  isDefault: boolean("is_default").default(false),
});

export const users = pgTable(
  "users",
  {
    id: uuid("id").defaultRandom().primaryKey(),
    username: varchar("username", { length: 50 }).notNull().unique(),
    email: varchar("email", { length: 255 }).unique(),
    passwordHash: varchar("password_hash", { length: 255 }).notNull(),
    displayName: varchar("display_name", { length: 100 }).notNull(),
    isActive: boolean("is_active").default(true),
    roleId: integer("role_id")
      .notNull()
      .references(() => roles.id),
    resourceLimitsOverride: jsonb("resource_limits_override"),
    createdAt: timestamp("created_at").defaultNow(),
    updatedAt: timestamp("updated_at").defaultNow(),
    deletedAt: timestamp("deleted_at"),
  },
  (t) => [index("users_username_idx").on(t.username), index("users_email_idx").on(t.email)]
);

export const rolePermissions = pgTable("role_permissions", {
  id: uuid("id").defaultRandom().primaryKey(),
  roleId: integer("role_id")
    .notNull()
    .references(() => roles.id),
  permission: varchar("permission", { length: 100 }).notNull(),
});

export const workspaces = pgTable("workspaces", {
  id: uuid("id").defaultRandom().primaryKey(),
  userId: uuid("user_id")
    .notNull()
    .references(() => users.id, { onDelete: "cascade" }),
  name: varchar("name", { length: 100 }).notNull(),
  slug: varchar("slug", { length: 100 }).notNull(),
  linuxUser: varchar("linux_user", { length: 50 }).notNull(),
  workspacePath: varchar("workspace_path", { length: 500 }).notNull(),
  isActive: boolean("is_active").default(true),
  createdAt: timestamp("created_at").defaultNow(),
  updatedAt: timestamp("updated_at").defaultNow(),
  deletedAt: timestamp("deleted_at"),
});

export const workspaceConfigs = pgTable("workspace_config", {
  // Note: agents_json, skills_json, mcps_json hold the DB representation.
  // The filesystem (agents/, skills/ dirs) is the source of truth at runtime.
  // On workspace creation, manage-workspace.sh copies dirs from templates;
  // agents_json is populated from template data for admin panel reference only.
  id: uuid("id").defaultRandom().primaryKey(),
  workspaceId: uuid("workspace_id")
    .notNull()
    .references(() => workspaces.id, { onDelete: "cascade" })
    .unique(),
  agentsJson: jsonb("agents_json"),
  skillsJson: jsonb("skills_json"),
  mcpsJson: jsonb("mcps_json"),
  agentsMdText: text("agents_md_text"),
  resourceLimits: jsonb("resource_limits").notNull().default({
    maxRam: 4 * 1024 * 1024 * 1024,
    maxProcess: 30,
    maxOpenFiles: 256,
    executionTimeout: 15 * 60 * 1000,
  }),
});

export const authSessions = pgTable("sessions", {
  id: uuid("id").defaultRandom().primaryKey(),
  userId: uuid("user_id")
    .notNull()
    .references(() => users.id, { onDelete: "cascade" }),
  token: varchar("token", { length: 500 }).notNull(),
  expiresAt: timestamp("expires_at").notNull(),
  createdAt: timestamp("created_at").defaultNow(),
});

export const opencodeSessions = pgTable("opencode_sessions", {
  id: uuid("id").defaultRandom().primaryKey(),
  workspaceId: uuid("workspace_id")
    .notNull()
    .references(() => workspaces.id, { onDelete: "cascade" }),
  userId: uuid("user_id")
    .notNull()
    .references(() => users.id, { onDelete: "cascade" }),
  opencodeSid: varchar("opencode_sid", { length: 100 }),
  status: varchar("status", { length: 20 }).notNull().default("active"),
  model: varchar("model", { length: 50 }),
  port: integer("port"),
  pid: integer("pid"),
  createdAt: timestamp("created_at").defaultNow(),
  lastActive: timestamp("last_active").defaultNow(),
});

export const chatMessages = pgTable("chat_messages", {
  id: uuid("id").defaultRandom().primaryKey(),
  sessionId: uuid("session_id")
    .notNull()
    .references(() => opencodeSessions.id, { onDelete: "cascade" }),
  role: varchar("role", { length: 10 }).notNull(),
  content: text("content").notNull(),
  createdAt: timestamp("created_at").defaultNow(),
});

export const userFiles = pgTable("user_files", {
  id: uuid("id").defaultRandom().primaryKey(),
  userId: uuid("user_id")
    .notNull()
    .references(() => users.id, { onDelete: "cascade" }),
  workspaceId: uuid("workspace_id")
    .notNull()
    .references(() => workspaces.id, { onDelete: "cascade" }),
  filename: varchar("filename", { length: 255 }).notNull(),
  filePath: varchar("file_path", { length: 500 }).notNull(),
  fileSize: bigint("file_size", { mode: "number" }).notNull(),
  mimeType: varchar("mime_type", { length: 100 }),
  createdAt: timestamp("created_at").defaultNow(),
  updatedAt: timestamp("updated_at").defaultNow(),
});

export const auditLogs = pgTable("audit_logs", {
  id: uuid("id").defaultRandom().primaryKey(),
  userId: uuid("user_id").references(() => users.id, { onDelete: "set null" }),
  action: varchar("action", { length: 100 }).notNull(),
  entityType: varchar("entity_type", { length: 50 }).notNull(),
  entityId: varchar("entity_id", { length: 36 }).notNull(),
  oldValue: jsonb("old_value"),
  newValue: jsonb("new_value"),
  ipAddress: varchar("ip_address", { length: 45 }),
  createdAt: timestamp("created_at").defaultNow(),
});

// Relations
export const usersRelations = relations(users, ({ one, many }) => ({
  role: one(roles, { fields: [users.roleId], references: [roles.id] }),
  workspaces: many(workspaces),
  authSessions: many(authSessions),
}));

export const workspacesRelations = relations(workspaces, ({ one, many }) => ({
  user: one(users, { fields: [workspaces.userId], references: [users.id] }),
  config: one(workspaceConfigs, {
    fields: [workspaces.id],
    references: [workspaceConfigs.workspaceId],
  }),
  opencodeSessions: many(opencodeSessions),
}));

export const opencodeSessionsRelations = relations(opencodeSessions, ({ one, many }) => ({
  workspace: one(workspaces, {
    fields: [opencodeSessions.workspaceId],
    references: [workspaces.id],
  }),
  user: one(users, { fields: [opencodeSessions.userId], references: [users.id] }),
  messages: many(chatMessages),
}));
```

- [ ] **Step 2: Create Drizzle client**

Create `apps/web/src/server/db/index.ts`:

```typescript
import { drizzle } from "drizzle-orm/postgres-js";
import postgres from "postgres";
import * as schema from "./schema";

const connectionString = process.env.DATABASE_URL;
if (!connectionString) {
  throw new Error("DATABASE_URL environment variable is required. Copy .env.example to .env and fill in values.");
}

const client = postgres(connectionString, { max: 5 });
export const db = drizzle(client, { schema });
export { schema };
```

- [ ] **Step 3: Generate initial migration**

```bash
bun drizzle-kit generate
```
Expected: Migration files created in `apps/web/src/server/db/migrations/`.

- [ ] **Step 4: Commit**

```bash
git add apps/web/src/server/db/ drizzle.config.ts
git commit -m "feat: add database schema with all tables"
```

---

## Phase 2: Auth System

> **NOT — Nitro v3 API:** Portal Nitro v3 kullanır. Bu plandaki kodların tamamında aşağıdaki dönüşüm uygulanmalıdır:
> - `import { createError, ... } from "h3"` → `import { HTTPError, ... } from "nitro/h3"`
> - `import { defineEventHandler } from "h3"` → `import { defineHandler } from "nitro/h3"`
> - `throw createError({ statusCode: 400, statusMessage: "..." })` → `throw new HTTPError("...", { status: 400 })`
> - `import { getRouterParam, readBody, getHeaders, ... } from "h3"` → `import { ... } from "nitro/h3"`
>
> Aşağıdaki kod blokları bu dönüşümleri göstermek içindir. Gerçek implementasyonda tüm endpoint'lerde bu API kullanılmalıdır.

### Task 2.1: Password and JWT Utilities

**Files:**
- Create: `apps/web/src/server/utils/password.ts`
- Create: `apps/web/src/server/utils/jwt.ts`
- Create: `apps/web/src/server/utils/rate-limit.ts`
- Test: `apps/web/src/server/utils/__tests__/password.test.ts`
- Test: `apps/web/src/server/utils/__tests__/jwt.test.ts`

- [ ] **Step 1: Write tests for password utilities**

Create `apps/web/src/server/utils/__tests__/password.test.ts`:

```typescript
import { describe, it, expect } from "bun:test";
import { hashPassword, verifyPassword } from "../password";

describe("password", () => {
  it("hashes and verifies a password", async () => {
    const hash = await hashPassword("test1234");
    expect(hash).not.toBe("test1234");
    expect(await verifyPassword("test1234", hash)).toBe(true);
  });

  it("rejects wrong password", async () => {
    const hash = await hashPassword("test1234");
    expect(await verifyPassword("wrong", hash)).toBe(false);
  });
});
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
bun test apps/web/src/server/utils/__tests__/password.test.ts
```
Expected: FAIL (module not found)

- [ ] **Step 3: Implement password utilities**

Create `apps/web/src/server/utils/password.ts`:

```typescript
import Bun from "bun";

export async function hashPassword(password: string): Promise<string> {
  if (typeof Bun !== "undefined" && Bun.password) {
    return Bun.password.hash(password, { algorithm: "bcrypt", cost: 12 });
  }
  // Fallback for environments without Bun (e.g., Node.js runtime)
  const bcrypt = await import("bcryptjs");
  return bcrypt.hash(password, 12);
}

export async function verifyPassword(password: string, hash: string): Promise<boolean> {
  if (typeof Bun !== "undefined" && Bun.password) {
    return Bun.password.verify(password, hash);
  }
  const bcrypt = await import("bcryptjs");
  return bcrypt.compare(password, hash);
}
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
bun test apps/web/src/server/utils/__tests__/password.test.ts
```
Expected: 2 PASS

- [ ] **Step 5: Write tests for JWT utilities**

Create `apps/web/src/server/utils/__tests__/jwt.test.ts`:

```typescript
import { describe, it, expect } from "bun:test";
import { signToken, verifyToken } from "../jwt";

describe("jwt", () => {
  it("signs and verifies a token", async () => {
    const payload = { userId: "abc", role: "marketing-agent", workspaceId: "xyz" };
    const token = await signToken(payload);
    const decoded = await verifyToken(token);
    expect(decoded.userId).toBe("abc");
    expect(decoded.role).toBe("marketing-agent");
  });

  it("rejects expired token", async () => {
    const token = await signToken({ userId: "abc" }, "0s");
    await expect(verifyToken(token)).rejects.toThrow();
  });

  it("rejects invalid token", async () => {
    await expect(verifyToken("garbage")).rejects.toThrow();
  });
});
```

- [ ] **Step 6: Run tests to verify they fail**

```bash
bun test apps/web/src/server/utils/__tests__/jwt.test.ts
```
Expected: FAIL

- [ ] **Step 7: Implement JWT utilities**

Create `apps/web/src/server/utils/jwt.ts`:

```typescript
import { SignJWT, jwtVerify } from "jose";

const jwtSecret = process.env.JWT_SECRET;
if (!jwtSecret) {
  throw new Error("JWT_SECRET environment variable is required. Copy .env.example to .env and fill in values.");
}
const secret = new TextEncoder().encode(jwtSecret);

export interface TokenPayload {
  userId: string;
  role: string;
  workspaceId: string;
}

export async function signToken(
  payload: Partial<TokenPayload>,
  expiresIn: string = "24h"
): Promise<string> {
  return new SignJWT({ ...payload })
    .setProtectedHeader({ alg: "HS256" })
    .setExpirationTime(expiresIn)
    .setIssuedAt()
    .sign(secret);
}

export async function verifyToken(token: string): Promise<TokenPayload> {
  const { payload } = await jwtVerify(token, secret);
  return payload as unknown as TokenPayload;
}
```

- [ ] **Step 8: Run tests to verify they pass**

```bash
bun test apps/web/src/server/utils/__tests__/jwt.test.ts
```
Expected: 3 PASS

- [ ] **Step 9: Implement rate limiter**

Create `apps/web/src/server/utils/rate-limit.ts`:

```typescript
// In-memory rate limiter. Works for single process (MVP).
// NOTE: If scaling to PM2 cluster mode later, migrate to Redis-backed storage.
const attempts = new Map<string, { count: number; blockedUntil: number }>();

const MAX_ATTEMPTS = 15;
const BLOCK_DURATION = 15 * 60 * 1000; // 15 minutes

export function checkRateLimit(key: string): { allowed: boolean; remaining: number } {
  const now = Date.now();
  const record = attempts.get(key);

  if (record && record.blockedUntil > now) {
    return { allowed: false, remaining: 0 };
  }

  if (!record || record.blockedUntil <= now) {
    attempts.set(key, { count: 0, blockedUntil: 0 });
  }

  return { allowed: true, remaining: MAX_ATTEMPTS - (record?.count ?? 0) };
}

export function recordFailedAttempt(key: string): void {
  const record = attempts.get(key);
  if (!record) {
    attempts.set(key, { count: 1, blockedUntil: 0 });
    return;
  }
  record.count++;
  if (record.count >= MAX_ATTEMPTS) {
    record.blockedUntil = Date.now() + BLOCK_DURATION;
  }
}

export function resetAttempts(key: string): void {
  attempts.delete(key);
}

// Cleanup stale entries every hour to prevent memory leak
const cleanupTimer = setInterval(() => {
  const now = Date.now();
  for (const [key, record] of attempts) {
    // Remove expired blocks AND stale non-blocked entries (no activity for 1 hour)
    if (record.blockedUntil > 0 && now > record.blockedUntil + 3600000) {
      attempts.delete(key);
    } else if (record.blockedUntil === 0 && record.count > 0) {
      // Remove entries that were never blocked but are sitting idle
      attempts.delete(key);
    }
  }
}, 3600000);

// Allow graceful shutdown
if (typeof process !== "undefined") {
  process.on("SIGTERM", () => clearInterval(cleanupTimer));
}
```

- [ ] **Step 10: Install jose dependency**

```bash
cd apps/web && bun add jose
```

- [ ] **Step 11: Commit**

```bash
git add apps/web/src/server/utils/
git commit -m "feat: add password, jwt, and rate-limit utilities"
```

---

### Task 2.2: Auth Middleware

**Files:**
- Create: `apps/web/src/server/middleware/auth.ts`
- Create: `apps/web/src/server/middleware/admin.ts`

- [ ] **Step 1: Write auth middleware**

Create `apps/web/src/server/middleware/auth.ts`:

```typescript
import { eq } from "drizzle-orm";
import { HTTPError } from "nitro/h3";
import { getHeader } from "nitro/h3";
import { verifyToken, TokenPayload } from "../utils/jwt";
import { db, schema } from "../db";

export interface AuthContext {
  user: TokenPayload & { isActive: boolean };
}

export async function authMiddleware(
  headers: Record<string, string | undefined>,
  cookies?: Record<string, string>
): Promise<AuthContext> {
  let token: string | undefined;

  // Try Authorization header first
  const authHeader = headers["authorization"];
  if (authHeader?.startsWith("Bearer ")) {
    token = authHeader.slice(7);
  }

  // Fall back to httpOnly cookie
  if (!token && cookies?.token) {
    token = cookies.token;
  }

  if (!token) {
    throw createError({ statusCode: 401, statusMessage: "Missing authorization header or cookie" });
  }
  let payload: TokenPayload;

  try {
    payload = await verifyToken(token);
  } catch {
    throw createError({ statusCode: 401, statusMessage: "Invalid or expired token" });
  }

  const [user] = await db
    .select({ isActive: schema.users.isActive, roleId: schema.users.roleId })
    .from(schema.users)
    .where(eq(schema.users.id, payload.userId))
    .limit(1);

  if (!user || !user.isActive) {
    throw createError({ statusCode: 403, statusMessage: "Account inactive or deleted" });
  }

  return { user: { ...payload, isActive: true } };
}
```

- [ ] **Step 2: Write admin middleware**

Create `apps/web/src/server/middleware/admin.ts`:

```typescript
import { HTTPError } from "nitro/h3";
import { AuthContext } from "./auth";

export function requireAdmin(ctx: AuthContext): void {
  if (ctx.user.role !== "admin") {
    throw createError({
      statusCode: 403,
      statusMessage: "Admin access required",
    });
  }
}
```

- [ ] **Step 3: Commit**

```bash
git add apps/web/src/server/middleware/
git commit -m "feat: add auth and admin middleware"
```

---

### Task 2.3: Login and Me Endpoints

**Files:**
- Create: `apps/web/src/server/api/auth/login.post.ts`
- Create: `apps/web/src/server/api/auth/me.get.ts`

- [ ] **Step 1: Write login endpoint**

Create `apps/web/src/server/api/auth/login.post.ts`:

```typescript
import { eq, or } from "drizzle-orm";
import { db, schema } from "../../db";
import { hashPassword, verifyPassword } from "../../utils/password";
import { signToken } from "../../utils/jwt";
import { checkRateLimit, recordFailedAttempt, resetAttempts } from "../../utils/rate-limit";

export default defineEventHandler(async (event) => {
  const body = await readBody(event);
  const { login, password } = body;

  if (!login || !password) {
    throw createError({ statusCode: 400, statusMessage: "Login and password required" });
  }

  const rateCheck = checkRateLimit(login);
  if (!rateCheck.allowed) {
    throw createError({
      statusCode: 429,
      statusMessage: "Too many attempts. Try again in 15 minutes.",
    });
  }

  const [user] = await db
    .select({
      id: schema.users.id,
      username: schema.users.username,
      passwordHash: schema.users.passwordHash,
      displayName: schema.users.displayName,
      isActive: schema.users.isActive,
      roleName: schema.roles.name,
    })
    .from(schema.users)
    .innerJoin(schema.roles, eq(schema.users.roleId, schema.roles.id))
    .where(
      or(
        eq(schema.users.username, login),
        eq(schema.users.email, login)
      )
    )
    .limit(1);

  if (!user || !user.isActive) {
    recordFailedAttempt(login);
    throw createError({ statusCode: 401, statusMessage: "Invalid credentials" });
  }

  const valid = await verifyPassword(password, user.passwordHash);
  if (!valid) {
    recordFailedAttempt(login);
    throw createError({ statusCode: 401, statusMessage: "Invalid credentials" });
  }

  resetAttempts(login);

  const [workspace] = await db
    .select({ id: schema.workspaces.id })
    .from(schema.workspaces)
    .where(eq(schema.workspaces.userId, user.id))
    .limit(1);

  const token = await signToken({
    userId: user.id,
    role: user.roleName,
    workspaceId: workspace?.id,
  });

  const expiresAt = new Date(Date.now() + 24 * 60 * 60 * 1000);
  await db.insert(schema.authSessions).values({
    userId: user.id,
    token,
    expiresAt,
  });

  setCookie(event, "token", token, {
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    sameSite: process.env.NODE_ENV === "production" ? "none" : "lax", // "none" for cross-origin (Vercel frontend + VPS backend)
    maxAge: 24 * 60 * 60, // 24 hours
    path: "/",
  });

  return {
    user: {
      id: user.id,
      username: user.username,
      displayName: user.displayName,
      role: user.roleName,
      workspaceId: workspace?.id,
    },
  };
});
```

- [ ] **Step 2: Write me endpoint**

Create `apps/web/src/server/api/auth/me.get.ts`:

```typescript
import { authMiddleware } from "../../middleware/auth";
import { db, schema } from "../../db";
import { eq } from "drizzle-orm";

export default defineEventHandler(async (event) => {
  const ctx = await authMiddleware(getHeaders(event), parseCookies(event));

  const [user] = await db
    .select({
      id: schema.users.id,
      username: schema.users.username,
      displayName: schema.users.displayName,
      roleName: schema.roles.name,
      workspaceId: schema.workspaces.id,
    })
    .from(schema.users)
    .innerJoin(schema.roles, eq(schema.users.roleId, schema.roles.id))
    .leftJoin(schema.workspaces, eq(schema.users.id, schema.workspaces.userId))
    .where(eq(schema.users.id, ctx.user.userId))
    .limit(1);

  return { user };
});
```

- [ ] **Step 3: Write logout endpoint (clears cookie and invalidates token)**

Create `apps/web/src/server/api/auth/logout.post.ts`:

```typescript
import { eq } from "drizzle-orm";
import { db, schema } from "../../db";
import { authMiddleware } from "../../middleware/auth";

export default defineEventHandler(async (event) => {
  try {
    const ctx = await authMiddleware(getHeaders(event), parseCookies(event));

    // Invalidate the auth session in DB so token can't be reused via Authorization header
    const token = parseCookies(event).token || getHeader(event, "authorization")?.slice(7);
    if (token) {
      await db.delete(schema.authSessions).where(eq(schema.authSessions.token, token));
    }
  } catch {
    // If token is already invalid, still clear the cookie
  }

  deleteCookie(event, "token", { path: "/" });
  return { success: true };
});
```

- [ ] **Step 4: Commit**

```bash
git add apps/web/src/server/api/auth/
git commit -m "feat: add login and me endpoints"
```

---

## Phase 3: User & Workspace Management

### Task 3.1: manage-workspace.sh Script

**Files:**
- Create: `scripts/manage-workspace.sh`

- [ ] **Step 1: Write the wrapper script**

Create `scripts/manage-workspace.sh`:

```bash
#!/bin/bash
set -e

ACTION=$1
USER_ID=$2
WORKSPACES_ROOT="/opt/personalautonomy/workspaces"
TEMPLATES_ROOT="/opt/personalautonomy/templates/roles"

if [[ ! "$USER_ID" =~ ^ws-[a-f0-9-]+$ ]]; then
  echo "Error: invalid user ID format. Must be ws-{uuid}"
  exit 1
fi

case $ACTION in
  "create")
    ROLE_NAME=$3
    if [[ -n "$ROLE_NAME" && ! "$ROLE_NAME" =~ ^[a-zA-Z0-9_-]+$ ]]; then
      echo "Error: invalid role name. Only alphanumeric, hyphens, and underscores allowed."
      exit 1
    fi

    if id "$USER_ID" &>/dev/null; then
      echo "Error: user $USER_ID already exists"
      exit 1
    fi

    useradd -M -s /sbin/nologin "$USER_ID"
    mkdir -p "$WORKSPACES_ROOT/$USER_ID"

    mkdir -p "$WORKSPACES_ROOT/$USER_ID/data"
    mkdir -p "$WORKSPACES_ROOT/$USER_ID/logs"

    # Symlink template dosyalarını workspace'e bağla.
    # cp yerine ln -s kullanılır: template güncellenince tüm workspace'ler otomatik görür.
    # Template'ler git'te olduğu ve deploy'da geldiği için silinme riski yoktur.
    # Workspace kullanıcısı symlink'i takip edebilir (template dizini chmod 755). Değiştiremez (read-only).
    if [ -n "$ROLE_NAME" ] && [ -d "$TEMPLATES_ROOT/$ROLE_NAME" ]; then
      ln -sfn "$TEMPLATES_ROOT/$ROLE_NAME/AGENTS.md" "$WORKSPACES_ROOT/$USER_ID/AGENTS.md" 2>/dev/null || true
      ln -sfn "$TEMPLATES_ROOT/$ROLE_NAME/skills" "$WORKSPACES_ROOT/$USER_ID/skills" 2>/dev/null || true
      ln -sfn "$TEMPLATES_ROOT/$ROLE_NAME/agents" "$WORKSPACES_ROOT/$USER_ID/agents" 2>/dev/null || true
      ln -sfn "$TEMPLATES_ROOT/$ROLE_NAME/mcps.json" "$WORKSPACES_ROOT/$USER_ID/mcps.json" 2>/dev/null || true
    fi

    # User-owned writable dirs — also accessible to nitro-runner group for file uploads
    chown "$USER_ID:nitro-runner" "$WORKSPACES_ROOT/$USER_ID/data"
    chmod 770 "$WORKSPACES_ROOT/$USER_ID/data"
    chown "$USER_ID:$USER_ID" "$WORKSPACES_ROOT/$USER_ID/logs"
    chmod 700 "$WORKSPACES_ROOT/$USER_ID/logs"

    chown "$USER_ID:$USER_ID" "$WORKSPACES_ROOT/$USER_ID"
    chmod 700 "$WORKSPACES_ROOT/$USER_ID"

    echo "Workspace created: $WORKSPACES_ROOT/$USER_ID"
    exit 0
    ;;

  "delete")
    if ! id "$USER_ID" &>/dev/null; then
      echo "Warning: user $USER_ID does not exist, cleaning up files"
    else
      userdel "$USER_ID" 2>/dev/null || true
    fi

    if [ -d "$WORKSPACES_ROOT/$USER_ID" ]; then
      rm -rf "$WORKSPACES_ROOT/$USER_ID"
    fi

    echo "Workspace deleted: $USER_ID"
    exit 0
    ;;

  "chown-file")
    FILE_PATH=$3  # For chown-file, $3 is the file path (not role name)
    if [ -z "$FILE_PATH" ]; then
      echo "Error: file path required"
      exit 1
    fi

    # Verify file is within the workspace directory
    if [[ ! "$FILE_PATH" =~ ^$WORKSPACES_ROOT/$USER_ID/ ]]; then
      echo "Error: file path must be within workspace directory"
      exit 1
    fi

    if [ ! -f "$FILE_PATH" ]; then
      echo "Error: file not found: $FILE_PATH"
      exit 1
    fi

    chown "$USER_ID:$USER_ID" "$FILE_PATH"
    echo "Ownership transferred: $FILE_PATH -> $USER_ID"
    exit 0
    ;;

  *)
    echo "Usage: $0 create <ws-user-id> <role-name>"
    echo "       $0 delete <ws-user-id>"
    echo "       $0 chown-file <ws-user-id> <file-path>"
    exit 1
    ;;
esac
```

- [ ] **Step 2: Make script executable**

```bash
chmod +x scripts/manage-workspace.sh
```

- [ ] **Step 3: Configure sudoers for nitro-runner (server setup)**

On the production VPS, create `/etc/sudoers.d/nitro-runner`:

```bash
echo 'nitro-runner ALL=(ALL) NOPASSWD: /opt/personalautonomy/scripts/manage-workspace.sh, /usr/bin/kill' | sudo tee /etc/sudoers.d/nitro-runner
sudo chmod 440 /etc/sudoers.d/nitro-runner
sudo visudo -cf /etc/sudoers.d/nitro-runner
```

This allows `nitro-runner` to:
- Run `manage-workspace.sh` with sudo (for workspace creation/deletion)
- Send kill signals via `sudo kill` to OpenCode processes owned by `ws-xxx` users

- [ ] **Step 4: Commit**

```bash
git add scripts/manage-workspace.sh
git commit -m "feat: add workspace management wrapper script"
```

---

### Task 3.2: Workspace Manager Service

**Files:**
- Create: `apps/web/src/server/services/workspace-manager.ts`

- [ ] **Step 1: Write workspace manager**

Create `apps/web/src/server/services/workspace-manager.ts`:

```typescript
import { exec } from "child_process";
import { promisify } from "util";
import { db, schema } from "../db";
import { eq } from "drizzle-orm";

const execAsync = promisify(exec);

const SCRIPT_PATH = process.env.WORKSPACE_SCRIPT_PATH || "/opt/personalautonomy/scripts/manage-workspace.sh";

export interface CreateWorkspaceInput {
  userId: string;
  name: string;
  slug: string;
  roleName: string;
}

export async function createWorkspace(input: CreateWorkspaceInput) {
  const linuxUser = `ws-${input.userId.replace(/-/g, "").slice(0, 16)}`;

  const [workspace] = await db
    .insert(schema.workspaces)
    .values({
      userId: input.userId,
      name: input.name,
      slug: input.slug,
      linuxUser,
      workspacePath: `${process.env.WORKSPACES_ROOT || "/opt/personalautonomy/workspaces"}/${linuxUser}`,
    })
    .returning();

  const [role] = await db
    .select({ templatePath: schema.roles.templatePath })
    .from(schema.roles)
    .where(eq(schema.roles.name, input.roleName))
    .limit(1);

  const roleDir = role?.templatePath?.split("/").pop() || input.roleName;

  try {
    await execAsync(`sudo ${SCRIPT_PATH} create ${linuxUser} ${roleDir}`, {
      timeout: 10000,
    });
  } catch (error: unknown) {
    await db.delete(schema.workspaces).where(eq(schema.workspaces.id, workspace.id));
    const msg = error instanceof Error ? error.message : String(error);
    throw new Error(`Failed to create workspace: ${msg}`);
  }

  const defaultLimits = {
    maxRam: 4 * 1024 * 1024 * 1024,
    maxProcess: 30,
    maxOpenFiles: 256,
    executionTimeout: 15 * 60 * 1000,
  };

  await db.insert(schema.workspaceConfigs).values({
    workspaceId: workspace.id,
    resourceLimits: defaultLimits,
  });

  return workspace;
}

export async function deleteWorkspace(workspaceId: string) {
  const [workspace] = await db
    .select({ linuxUser: schema.workspaces.linuxUser })
    .from(schema.workspaces)
    .where(eq(schema.workspaces.id, workspaceId))
    .limit(1);

  if (!workspace) throw new Error("Workspace not found");

  try {
    await execAsync(`sudo ${SCRIPT_PATH} delete ${workspace.linuxUser}`, {
      timeout: 10000,
    });
  } catch (error: unknown) {
    const msg = error instanceof Error ? error.message : String(error);
    throw new Error(`Failed to delete workspace: ${msg}`);
  }

  await db
    .update(schema.workspaces)
    .set({ deletedAt: new Date(), isActive: false })
    .where(eq(schema.workspaces.id, workspaceId));
}
```

- [ ] **Step 2: Commit**

```bash
git add apps/web/src/server/services/workspace-manager.ts
git commit -m "feat: add workspace manager service"
```

---

### Task 3.3: User Management API (Admin)

**Files:**
- Create: `apps/web/src/server/api/users/index.get.ts`
- Create: `apps/web/src/server/api/users/index.post.ts`
- Create: `apps/web/src/server/api/users/[id].ts`
- Create: `apps/web/src/server/services/audit-logger.ts`

- [ ] **Step 1: Write audit logger**

Create `apps/web/src/server/services/audit-logger.ts`:

```typescript
import { db, schema } from "../db";

export async function logAudit(input: {
  userId?: string;
  action: string;
  entityType: string;
  entityId: string;
  oldValue?: Record<string, unknown>;
  newValue?: Record<string, unknown>;
  ipAddress?: string;
}) {
  await db.insert(schema.auditLogs).values({
    userId: input.userId,
    action: input.action,
    entityType: input.entityType,
    entityId: input.entityId,
    oldValue: input.oldValue,
    newValue: input.newValue,
    ipAddress: input.ipAddress,
  });
}
```

- [ ] **Step 2: Write admin list users endpoint**

Create `apps/web/src/server/api/users/index.get.ts`:

```typescript
import { db, schema } from "../../db";
import { eq, isNull } from "drizzle-orm";
import { authMiddleware } from "../../middleware/auth";
import { requireAdmin } from "../../middleware/admin";

export default defineEventHandler(async (event) => {
  const ctx = await authMiddleware(getHeaders(event), parseCookies(event));
  requireAdmin(ctx);

  const users = await db
    .select({
      id: schema.users.id,
      username: schema.users.username,
      email: schema.users.email,
      displayName: schema.users.displayName,
      isActive: schema.users.isActive,
      roleName: schema.roles.name,
      createdAt: schema.users.createdAt,
    })
    .from(schema.users)
    .innerJoin(schema.roles, eq(schema.users.roleId, schema.roles.id))
    .where(isNull(schema.users.deletedAt))
    .orderBy(schema.users.createdAt);

  return { users };
});
```

- [ ] **Step 3: Write admin create user endpoint**

Create `apps/web/src/server/api/users/index.post.ts`:

```typescript
import { db, schema } from "../../db";
import { eq } from "drizzle-orm";
import { authMiddleware } from "../../middleware/auth";
import { requireAdmin } from "../../middleware/admin";
import { hashPassword } from "../../utils/password";
import { createWorkspace } from "../../services/workspace-manager";
import { logAudit } from "../../services/audit-logger";

export default defineEventHandler(async (event) => {
  const ctx = await authMiddleware(getHeaders(event), parseCookies(event));
  requireAdmin(ctx);

  const body = await readBody(event);
  const { username, email, displayName, password, roleName } = body;

  if (!username || !displayName || !password || !roleName) {
    throw createError({ statusCode: 400, statusMessage: "Missing required fields" });
  }

  const [existing] = await db
    .select({ id: schema.users.id })
    .from(schema.users)
    .where(eq(schema.users.username, username))
    .limit(1);

  if (existing) {
    throw createError({ statusCode: 409, statusMessage: "Username already taken" });
  }

  const [role] = await db
    .select({ id: schema.roles.id })
    .from(schema.roles)
    .where(eq(schema.roles.name, roleName))
    .limit(1);

  if (!role) {
    throw createError({ statusCode: 400, statusMessage: "Invalid role" });
  }

  const passwordHash = await hashPassword(password);

  const [user] = await db
    .insert(schema.users)
    .values({
      username,
      email: email || null,
      passwordHash,
      displayName,
      roleId: role.id,
    })
    .returning();

  const slug = username.toLowerCase().replace(/[^a-z0-9-]/g, "-");
  await createWorkspace({
    userId: user.id,
    name: `${displayName}'s Workspace`,
    slug,
    roleName,
  });

  await logAudit({
    userId: ctx.user.userId,
    action: "user.created",
    entityType: "user",
    entityId: user.id,
    newValue: { username, displayName, roleName },
  });

  return { user };
});
```

- [ ] **Step 4: Write admin user detail/update/delete endpoint**

Create `apps/web/src/server/api/users/[id].ts`:

```typescript
import { db, schema } from "../../db";
import { eq } from "drizzle-orm";
import { authMiddleware } from "../../middleware/auth";
import { requireAdmin } from "../../middleware/admin";
import { deleteWorkspace } from "../../services/workspace-manager";
import { logAudit } from "../../services/audit-logger";

export default defineEventHandler(async (event) => {
  const ctx = await authMiddleware(getHeaders(event), parseCookies(event));
  requireAdmin(ctx);

  const userId = getRouterParam(event, "id");
  if (!userId) throw createError({ statusCode: 400, statusMessage: "Missing user ID" });

  const method = event.method;

  if (method === "GET") {
    const [user] = await db
      .select({
        id: schema.users.id,
        username: schema.users.username,
        email: schema.users.email,
        displayName: schema.users.displayName,
        isActive: schema.users.isActive,
        roleName: schema.roles.name,
        resourceLimitsOverride: schema.users.resourceLimitsOverride,
        workspaceId: schema.workspaces.id,
        workspacePath: schema.workspaces.workspacePath,
        linuxUser: schema.workspaces.linuxUser,
      })
      .from(schema.users)
      .innerJoin(schema.roles, eq(schema.users.roleId, schema.roles.id))
      .leftJoin(schema.workspaces, eq(schema.users.id, schema.workspaces.userId))
      .where(eq(schema.users.id, userId))
      .limit(1);

    if (!user) throw createError({ statusCode: 404, statusMessage: "User not found" });
    return { user };
  }

  if (method === "PUT") {
    const body = await readBody(event);
    const updates: Record<string, unknown> = { updatedAt: new Date() };

    if (body.displayName !== undefined) updates.displayName = body.displayName;
    if (body.email !== undefined) updates.email = body.email;
    if (body.isActive !== undefined) updates.isActive = body.isActive;
    if (body.resourceLimitsOverride !== undefined) {
      updates.resourceLimitsOverride = body.resourceLimitsOverride;
    }

    const [updated] = await db
      .update(schema.users)
      .set(updates)
      .where(eq(schema.users.id, userId))
      .returning();

    await logAudit({
      userId: ctx.user.userId,
      action: "user.updated",
      entityType: "user",
      entityId: userId,
      newValue: updates,
    });

    return { user: updated };
  }

  if (method === "DELETE") {
    const [workspace] = await db
      .select({ id: schema.workspaces.id })
      .from(schema.workspaces)
      .where(eq(schema.workspaces.userId, userId))
      .limit(1);

    if (workspace) {
      await deleteWorkspace(workspace.id);
    }

    await db
      .update(schema.users)
      .set({ deletedAt: new Date(), isActive: false })
      .where(eq(schema.users.id, userId));

    await logAudit({
      userId: ctx.user.userId,
      action: "user.deleted",
      entityType: "user",
      entityId: userId,
    });

    return { success: true };
  }

  throw createError({ statusCode: 405, statusMessage: "Method not allowed" });
});
```

- [ ] **Step 5: Commit**

```bash
git add apps/web/src/server/api/users/ apps/web/src/server/services/audit-logger.ts
git commit -m "feat: add user management API with audit logging"
```

---

## Phase 4: OpenCode Integration

### Task 4.1: OpenCode Process Manager

**Files:**
- Create: `apps/web/src/server/services/opencode-manager.ts`

- [ ] **Step 1: Write OpenCode process manager**

Create `apps/web/src/server/services/opencode-manager.ts`:

```typescript
import { spawn, exec, ChildProcess } from "child_process";
import { promisify } from "util";

const execAsync = promisify(exec);
import { createServer } from "net";

const OPENCODE_PATH = process.env.OPENCODE_PATH || "opencode";

// Global port tracker to prevent TOCTOU race conditions
const usedPorts = new Set<number>();

function holdPort(): Promise<{ port: number; release: () => void }> {
  return new Promise((resolve, reject) => {
    const server = createServer();
    server.listen(0, () => {
      const addr = server.address();
      const port = typeof addr === "object" && addr !== null ? addr.port : 0;
      usedPorts.add(port);
      resolve({
        port,
        release: () => {
          server.close();
          usedPorts.delete(port);
        },
      });
    });
    server.on("error", reject);
  });
}

export interface SpawnOptions {
  workspacePath: string;
  linuxUser: string;
  limits?: {
    maxRam?: number;
    maxProcess?: number;
    maxOpenFiles?: number;
  };
}

export async function spawnOpenCode(options: SpawnOptions): Promise<{
  process: ChildProcess;
  port: number;
  releasePort: () => void;
}> {
  const { port, release: releasePort } = await holdPort();

  const defaultLimits = {
    maxRam: 4 * 1024 * 1024 * 1024,
    maxProcess: 30,
    maxOpenFiles: 256,
    ...options.limits,
  };

  const maxRamKb = Math.floor(defaultLimits.maxRam / 1024);
  const maxFileSize = Math.floor(500 * 1024 * 1024 / 512); // 500MB in 512-byte blocks

  // Use bash -c with ulimit to avoid sudo PID mismatch (ulimit is shell built-in, not a separate process)
  const proc = spawn(
    "sudo",
    [
      "-u",
      options.linuxUser,
      "bash",
      "-c",
      `ulimit -v ${maxRamKb} -n ${defaultLimits.maxOpenFiles} -u ${defaultLimits.maxProcess} -t 600 -f ${maxFileSize}; exec ${OPENCODE_PATH} --port ${port}`,
    ],
    {
      cwd: options.workspacePath,
      detached: true,
      stdio: ["ignore", "pipe", "pipe"],
      env: {
        ...process.env,
        HOME: options.workspacePath,
        USER: options.linuxUser,
      },
    }
  );

  const { createWriteStream } = await import("fs");
  const logDir = `${options.workspacePath}/logs`;
  const outStream = createWriteStream(`${logDir}/agent.log`, { flags: "a" });
  const errStream = createWriteStream(`${logDir}/agent.error.log`, { flags: "a" });

  proc.stdout?.pipe(outStream);
  proc.stderr?.pipe(errStream);

  proc.on("error", (err) => {
    errStream.write(`Process error: ${err.message}\n`);
  });

  return { process: proc, port, releasePort };
}

export async function killOpenCode(proc: ChildProcess): Promise<void> {
  try {
    await execAsync(`sudo kill -TERM -${proc.pid}`, { timeout: 5000 });
  } catch {
    try {
      await execAsync(`sudo kill -KILL -${proc.pid}`, { timeout: 5000 });
    } catch {
      // Process already dead
    }
  }
}
```

- [ ] **Step 2: Commit**

```bash
git add apps/web/src/server/services/opencode-manager.ts
git commit -m "feat: add OpenCode process manager with resource limits"
```

---

### Task 4.2: Session Management API

**Files:**
- Create: `apps/web/src/server/services/session-manager.ts`
- Create: `apps/web/src/server/api/sessions/start.post.ts`
- Create: `apps/web/src/server/api/sessions/[id]/message.post.ts`
- Create: `apps/web/src/server/api/sessions/[id]/stream.get.ts`
- Create: `apps/web/src/server/api/sessions/[id]/index.delete.ts`
- Create: `apps/web/src/server/api/sessions/index.get.ts`

- [ ] **Step 1.5: Write OpenCode SDK client wrapper**

Create `apps/web/src/server/lib/opencode-client.ts`:

```typescript
// Thin wrapper around @opencode-ai/sdk for PersonalAutonomy's multi-tenant use.
// Pattern follows upstream portal's lib/opencode-client.ts but adapted for server-side
// process management where we spawn opencode per workspace user.
import { createOpencodeClient } from "@opencode-ai/sdk/v2/client";

const clientCache = new Map<number, ReturnType<typeof createOpencodeClient>>();

export function getOpencodeClient(port: number) {
  const cached = clientCache.get(port);
  if (cached) return cached;

  const client = createOpencodeClient({
    baseUrl: `http://127.0.0.1:${port}`,
  });

  clientCache.set(port, client);
  return client;
}

export function clearOpencodeClient(port: number) {
  clientCache.delete(port);
}
```

> **Note:** The portal already has `@opencode-ai/sdk` as a dependency (v1.14.41+). No extra `bun add` needed.

- [ ] **Step 2: Write session manager service**

Create `apps/web/src/server/services/session-manager.ts`:

```typescript
import { db, schema } from "../db";
import { eq, and, lt, isNull } from "drizzle-orm";
import { spawnOpenCode, killOpenCode } from "./opencode-manager";
import { ChildProcess } from "child_process";

const activeProcesses = new Map<string, { proc: ChildProcess; port: number }>();

export async function startSession(userId: string, workspaceId: string, model?: string) {
  const [workspace] = await db
    .select({
      workspacePath: schema.workspaces.workspacePath,
      linuxUser: schema.workspaces.linuxUser,
      limits: schema.workspaceConfigs.resourceLimits,
    })
    .from(schema.workspaces)
    .innerJoin(
      schema.workspaceConfigs,
      eq(schema.workspaces.id, schema.workspaceConfigs.workspaceId)
    )
    .where(eq(schema.workspaces.id, workspaceId))
    .limit(1);

  if (!workspace) throw new Error("Workspace not found");

  // Check workspace active status from the workspaces table
  const [wsStatus] = await db
    .select({ isActive: schema.workspaces.isActive })
    .from(schema.workspaces)
    .where(eq(schema.workspaces.id, workspaceId))
    .limit(1);
  if (!wsStatus?.isActive) throw new Error("Workspace is deactivated");

  const { process: proc, port, releasePort } = await spawnOpenCode({
    workspacePath: workspace.workspacePath,
    linuxUser: workspace.linuxUser,
    limits: workspace.limits as SpawnOptions["limits"],
  });

  // Wait for OpenCode to be ready (10 second timeout)
  const ready = await waitForReady(port, 10000);
  if (!ready) {
    await killOpenCode(proc);
    releasePort();
    throw new Error("OpenCode failed to start within timeout");
  }

  // Release the held port now that OpenCode has bound it
  releasePort();

  const [session] = await db
    .insert(schema.opencodeSessions)
    .values({
      workspaceId,
      userId,
      status: "active",
      model: model || null,
      port,
      pid: proc.pid,
    })
    .returning();

  activeProcesses.set(session.id, { proc, port });

  return { session, port };
}

export async function sendMessage(sessionId: string, message: string) {
  const [session] = await db
    .select()
    .from(schema.opencodeSessions)
    .where(eq(schema.opencodeSessions.id, sessionId))
    .limit(1);

  if (!session || session.status === "closed") {
    throw new Error("Session not found or closed");
  }

  const active = activeProcesses.get(sessionId);
  if (!active) throw new Error("Process not running");

  await db.insert(schema.chatMessages).values({
    sessionId,
    role: "user",
    content: message,
  });

  // Store for SSE streaming
  return { sessionId, port: active.port, message };
}

export async function stopSession(sessionId: string) {
  const active = activeProcesses.get(sessionId);
  if (active) {
    await killOpenCode(active.proc);
    activeProcesses.delete(sessionId);
  }

  await db
    .update(schema.opencodeSessions)
    .set({ status: "closed" })
    .where(eq(schema.opencodeSessions.id, sessionId));
}

export async function listSessions(workspaceId?: string) {
  const where = workspaceId
    ? eq(schema.opencodeSessions.workspaceId, workspaceId)
    : undefined;

  return db
    .select({
      id: schema.opencodeSessions.id,
      workspaceId: schema.opencodeSessions.workspaceId,
      userId: schema.opencodeSessions.userId,
      status: schema.opencodeSessions.status,
      model: schema.opencodeSessions.model,
      createdAt: schema.opencodeSessions.createdAt,
      lastActive: schema.opencodeSessions.lastActive,
      username: schema.users.username,
      displayName: schema.users.displayName,
    })
    .from(schema.opencodeSessions)
    .innerJoin(schema.users, eq(schema.opencodeSessions.userId, schema.users.id))
    .where(where)
    .orderBy(schema.opencodeSessions.createdAt);
}

export async function cleanupIdleSessions(maxIdleMs: number = 30 * 60 * 1000) {
  const cutoff = new Date(Date.now() - maxIdleMs);

  for (const [id, active] of activeProcesses) {
    const [stale] = await db
      .select({ lastActive: schema.opencodeSessions.lastActive })
      .from(schema.opencodeSessions)
      .where(
        and(
          eq(schema.opencodeSessions.id, id),
          eq(schema.opencodeSessions.status, "active"),
          lt(schema.opencodeSessions.lastActive, cutoff)
        )
      )
      .limit(1);

    if (stale) {
      await killOpenCode(active.proc);
      activeProcesses.delete(id);
      await db
        .update(schema.opencodeSessions)
        .set({ status: "closed" })
        .where(eq(schema.opencodeSessions.id, id));
    }
  }
}

async function waitForReady(port: number, timeout: number): Promise<boolean> {
  const { createConnection } = await import("net");
  const start = Date.now();
  while (Date.now() - start < timeout) {
    try {
      await new Promise<void>((resolve, reject) => {
        const socket = createConnection({ host: "127.0.0.1", port }, () => {
          socket.destroy();
          resolve();
        });
        socket.on("error", reject);
        socket.setTimeout(500, () => {
          socket.destroy();
          reject(new Error("timeout"));
        });
      });
      // Additional grace period for OpenCode to finish initializing after port opens
      await new Promise((r) => setTimeout(r, 500));
      return true;
    } catch {
      await new Promise((r) => setTimeout(r, 500));
    }
  }
  return false;
}

// Run cleanup every 5 minutes
const sessionCleanupTimer = setInterval(() => {
  cleanupIdleSessions();
}, 5 * 60 * 1000);

// Graceful shutdown: clear interval
if (typeof process !== "undefined") {
  process.on("SIGTERM", () => clearInterval(sessionCleanupTimer));
}

// Recovery: on startup, mark orphaned "active" sessions as "closed"
// This handles PM2 restart scenarios where in-memory activeProcesses map is lost
(async () => {
  const orphaned = await db
    .select({ id: schema.opencodeSessions.id, pid: schema.opencodeSessions.pid })
    .from(schema.opencodeSessions)
    .where(eq(schema.opencodeSessions.status, "active"));

  for (const session of orphaned) {
    // Check if the PID is actually running
    if (session.pid) {
      try {
        process.kill(session.pid, 0); // Signal 0 = check existence
        // Process is still alive — leave it, skip marking as closed
        continue;
      } catch {
        // Process is dead — fall through, will be marked as closed below
      }
    }
    await db
      .update(schema.opencodeSessions)
      .set({ status: "closed" })
      .where(eq(schema.opencodeSessions.id, session.id));
  }
})();
```

- [ ] **Step 3: Write session start endpoint**

Create `apps/web/src/server/api/sessions/start.post.ts`:

```typescript
import { authMiddleware } from "../../middleware/auth";
import { startSession } from "../../services/session-manager";

export default defineEventHandler(async (event) => {
  const ctx = await authMiddleware(getHeaders(event), parseCookies(event));
  const body = await readBody(event);
  const { workspaceId, model } = body;

  const wsId = workspaceId || ctx.user.workspaceId;
  if (!wsId) throw createError({ statusCode: 400, statusMessage: "No workspace available" });

  try {
    const { session, port } = await startSession(ctx.user.userId, wsId, model);
    return { session, port };
  } catch (error: unknown) {
    throw createError({
      statusCode: 500,
      statusMessage: `Failed to start agent: ${error instanceof Error ? error.message : String(error)}`,
    });
  }
});
```

- [ ] **Step 4: Write message endpoint**

Create `apps/web/src/server/api/sessions/[id]/message.post.ts`:

```typescript
import { eq } from "drizzle-orm";
import { authMiddleware } from "../../../middleware/auth";
import { sendMessage } from "../../../services/session-manager";
import { db, schema } from "../../../db";

export default defineEventHandler(async (event) => {
  const ctx = await authMiddleware(getHeaders(event), parseCookies(event));
  const sessionId = getRouterParam(event, "id");
  if (!sessionId) throw createError({ statusCode: 400 });

  const [session] = await db
    .select({ userId: schema.opencodeSessions.userId })
    .from(schema.opencodeSessions)
    .where(eq(schema.opencodeSessions.id, sessionId))
    .limit(1);

  if (!session) throw createError({ statusCode: 404, statusMessage: "Session not found" });
  if (session.userId !== ctx.user.userId) {
    throw createError({ statusCode: 403, statusMessage: "Not your session" });
  }

  const body = await readBody(event);
  const { message } = body;

  const { port } = await sendMessage(sessionId, message);

  // Use OpenCode SDK to send prompt asynchronously (returns immediately).
  // The SSE stream endpoint handles delivering the response back to the client.
  const { getOpencodeClient } = await import("../../../lib/opencode-client");
  const client = getOpencodeClient(port);
  await client.session.promptAsync({
    sessionID: sessionId,
    parts: [{ type: "text" as const, text: message }],
  });

  return { accepted: true };
});
```

- [ ] **Step 5: Write session SSE stream endpoint**

Create `apps/web/src/server/api/sessions/[id]/stream.get.ts`:

```typescript
import { eq } from "drizzle-orm";
import { authMiddleware } from "../../../middleware/auth";
import { db, schema } from "../../../db";

export default defineEventHandler(async (event) => {
  const ctx = await authMiddleware(getHeaders(event), parseCookies(event));
  const sessionId = getRouterParam(event, "id");
  if (!sessionId) throw createError({ statusCode: 400 });

  const [session] = await db
    .select({
      userId: schema.opencodeSessions.userId,
      port: schema.opencodeSessions.port,
      status: schema.opencodeSessions.status,
    })
    .from(schema.opencodeSessions)
    .where(eq(schema.opencodeSessions.id, sessionId))
    .limit(1);

  if (!session) throw createError({ statusCode: 404, statusMessage: "Session not found" });
  if (session.userId !== ctx.user.userId && ctx.user.role !== "admin") {
    throw createError({ statusCode: 403, statusMessage: "Not your session" });
  }
  if (session.status !== "active" || !session.port) {
    throw createError({ statusCode: 400, statusMessage: "Session not active" });
  }

  // Update last active timestamp
  await db
    .update(schema.opencodeSessions)
    .set({ lastActive: new Date() })
    .where(eq(schema.opencodeSessions.id, sessionId));

  // Subscribe to OpenCode SDK event stream instead of raw HTTP fetch
  const { getOpencodeClient } = await import("../../../lib/opencode-client");
  const client = getOpencodeClient(session.port);

  const abort = new AbortController();
  const encoder = new TextEncoder();

  setHeader(event, "Content-Type", "text/event-stream");
  setHeader(event, "Cache-Control", "no-cache, no-transform");
  setHeader(event, "Connection", "keep-alive");
  setHeader(event, "X-Accel-Buffering", "no");

  // Close the event subscription when the client disconnects
  event.node.req.on("close", () => abort.abort());

  return new ReadableStream<Uint8Array>({
    async start(controller) {
      try {
        const events = await client.event.subscribe(undefined, {
          signal: abort.signal,
          sseMaxRetryAttempts: 0,
        });

        for await (const item of events.stream) {
          if (abort.signal.aborted) break;
          controller.enqueue(
            encoder.encode(`event: message\ndata: ${JSON.stringify(item)}\n\n`)
          );
        }
      } catch (_error) {
        if (!abort.signal.aborted) {
          controller.enqueue(
            encoder.encode(
              `event: error\ndata: ${JSON.stringify({ message: "Event stream disconnected" })}\n\n`
            )
          );
        }
      } finally {
        try { controller.close(); } catch { /* already closed */ }
      }
    },
    cancel() {
      abort.abort();
    },
  });
});
```

- [ ] **Step 6: Write session stop endpoint**

Create `apps/web/src/server/api/sessions/[id]/index.delete.ts`:

```typescript
import { eq } from "drizzle-orm";
import { authMiddleware } from "../../../middleware/auth";
import { stopSession } from "../../../services/session-manager";
import { db, schema } from "../../../db";

export default defineEventHandler(async (event) => {
  const ctx = await authMiddleware(getHeaders(event), parseCookies(event));
  const sessionId = getRouterParam(event, "id");
  if (!sessionId) throw createError({ statusCode: 400 });

  const [session] = await db
    .select({ userId: schema.opencodeSessions.userId })
    .from(schema.opencodeSessions)
    .where(eq(schema.opencodeSessions.id, sessionId))
    .limit(1);

  if (!session) throw createError({ statusCode: 404, statusMessage: "Session not found" });
  if (session.userId !== ctx.user.userId && ctx.user.role !== "admin") {
    throw createError({ statusCode: 403, statusMessage: "Not your session" });
  }

  await stopSession(sessionId);
  return { success: true };
});
```

- [ ] **Step 7: Write sessions list endpoint**

Create `apps/web/src/server/api/sessions/index.get.ts`:

```typescript
import { eq } from "drizzle-orm";
import { authMiddleware } from "../../middleware/auth";
import { listSessions } from "../../services/session-manager";
import { db, schema } from "../../db";

export default defineEventHandler(async (event) => {
  const ctx = await authMiddleware(getHeaders(event), parseCookies(event));

  let workspaceId: string | undefined;
  if (ctx.user.role !== "admin") {
    // Normal users only see their own sessions
    workspaceId = ctx.user.workspaceId;
  } else {
    const query = getQuery(event);
    workspaceId = query.workspaceId as string;
  }

  const sessions = await listSessions(workspaceId);
  return { sessions };
});
```

- [ ] **Step 8: Commit**

```bash
git add apps/web/src/server/services/session-manager.ts apps/web/src/server/api/sessions/ apps/web/src/server/lib/opencode-client.ts
git commit -m "feat: add session management API with OpenCode SDK integration"
```

---

### Task 4.2.5: Workspace Endpoints

> **Motivation:** File Structure'da `workspaces/index.get.ts` ve `workspaces/[id].ts` tanımlı ama hiçbir task oluşturmuyor.

**Files:**
- Create: `apps/web/src/server/api/workspaces/index.get.ts`
- Create: `apps/web/src/server/api/workspaces/[id].ts`

- [ ] **Step 1: Write workspace list endpoint**

Create `apps/web/src/server/api/workspaces/index.get.ts`:

```typescript
import { eq, isNull } from "drizzle-orm";
import { authMiddleware } from "../../middleware/auth";
import { requireAdmin } from "../../middleware/admin";
import { db, schema } from "../../db";

export default defineEventHandler(async (event) => {
  const ctx = await authMiddleware(getHeaders(event), parseCookies(event));

  if (ctx.user.role === "admin") {
    // Admin sees all workspaces
    const workspaces = await db
      .select({
        id: schema.workspaces.id,
        name: schema.workspaces.name,
        slug: schema.workspaces.slug,
        linuxUser: schema.workspaces.linuxUser,
        workspacePath: schema.workspaces.workspacePath,
        isActive: schema.workspaces.isActive,
        createdAt: schema.workspaces.createdAt,
        username: schema.users.username,
        displayName: schema.users.displayName,
      })
      .from(schema.workspaces)
      .innerJoin(schema.users, eq(schema.workspaces.userId, schema.users.id))
      .where(isNull(schema.workspaces.deletedAt))
      .orderBy(schema.workspaces.createdAt);

    return { workspaces };
  }

  // Normal users see only their own workspace
  const workspaces = await db
    .select()
    .from(schema.workspaces)
    .where(eq(schema.workspaces.userId, ctx.user.userId));

  return { workspaces };
});
```

- [ ] **Step 2: Write workspace detail endpoint**

Create `apps/web/src/server/api/workspaces/[id].ts`:

```typescript
import { eq } from "drizzle-orm";
import { authMiddleware } from "../../middleware/auth";
import { requireAdmin } from "../../middleware/admin";
import { db, schema } from "../../db";

export default defineEventHandler(async (event) => {
  const ctx = await authMiddleware(getHeaders(event), parseCookies(event));
  const workspaceId = getRouterParam(event, "id");
  if (!workspaceId) throw createError({ statusCode: 400, statusMessage: "Missing workspace ID" });

  const [workspace] = await db
    .select({
      id: schema.workspaces.id,
      name: schema.workspaces.name,
      slug: schema.workspaces.slug,
      linuxUser: schema.workspaces.linuxUser,
      workspacePath: schema.workspaces.workspacePath,
      isActive: schema.workspaces.isActive,
      createdAt: schema.workspaces.createdAt,
    })
    .from(schema.workspaces)
    .where(eq(schema.workspaces.id, workspaceId))
    .limit(1);

  if (!workspace) throw createError({ statusCode: 404, statusMessage: "Workspace not found" });

  // Non-admin users can only access their own workspace
  if (ctx.user.role !== "admin" && ctx.user.workspaceId !== workspaceId) {
    throw createError({ statusCode: 403, statusMessage: "Access denied" });
  }

  return { workspace };
});
```

- [ ] **Step 3: Commit**

```bash
git add apps/web/src/server/api/workspaces/index.get.ts apps/web/src/server/api/workspaces/[id].ts
git commit -m "feat: add workspace list and detail endpoints"
```

---

### Task 4.3: File Upload

**Files:**
- Create: `apps/web/src/server/api/workspaces/[id]/upload.post.ts`

- [ ] **Step 1: Write file upload endpoint**

Create `apps/web/src/server/api/workspaces/[id]/upload.post.ts`:

```typescript
import { eq } from "drizzle-orm";
import { writeFile } from "fs/promises";
import { join } from "path";
import { authMiddleware } from "../../../middleware/auth";
import { db, schema } from "../../../db";

const MAX_FILE_SIZE = 50 * 1024 * 1024; // 50 MB

export default defineEventHandler(async (event) => {
  const ctx = await authMiddleware(getHeaders(event), parseCookies(event));
  const workspaceId = getRouterParam(event, "id");
  if (!workspaceId) throw createError({ statusCode: 400 });

  const [workspace] = await db
    .select({
      workspacePath: schema.workspaces.workspacePath,
      linuxUser: schema.workspaces.linuxUser,
    })
    .from(schema.workspaces)
    .where(eq(schema.workspaces.id, workspaceId))
    .limit(1);

  if (!workspace) throw createError({ statusCode: 404, statusMessage: "Workspace not found" });

  const formData = await readMultipartFormData(event);
  if (!formData?.length) throw createError({ statusCode: 400, statusMessage: "No file uploaded" });

  const file = formData[0];
  if (!file.filename) throw createError({ statusCode: 400, statusMessage: "Invalid file" });

  // File size check to prevent disk exhaustion and OOM
  if (file.data.length > MAX_FILE_SIZE) {
    throw createError({ statusCode: 413, statusMessage: `File too large. Maximum: ${MAX_FILE_SIZE / 1024 / 1024} MB` });
  }

  const dataDir = join(workspace.workspacePath, "data");
  const safeName = file.filename.replace(/[^a-zA-Z0-9._-]/g, "_");
  if (!safeName || safeName.startsWith(".")) {
    throw createError({ statusCode: 400, statusMessage: "Invalid filename" });
  }
  const filePath = join(dataDir, safeName);
  await writeFile(filePath, file.data);

  // Transfer ownership to workspace user so OpenCode agent can modify/delete
  const { exec } = await import("child_process");
  const { promisify } = await import("util");
  const execAsync = promisify(exec);
  const scriptPath = process.env.WORKSPACE_SCRIPT_PATH || "/opt/personalautonomy/scripts/manage-workspace.sh";
  await execAsync(`sudo ${scriptPath} chown-file ${workspace.linuxUser} ${filePath}`, { timeout: 5000 });

  const [record] = await db
    .insert(schema.userFiles)
    .values({
      userId: ctx.user.userId,
      workspaceId,
      filename: file.filename,
      filePath,
      fileSize: file.data.length,
      mimeType: file.type || "application/octet-stream",
    })
    .returning();

  return { file: record };
});
```

- [ ] **Step 2: Commit**

```bash
git add apps/web/src/server/api/workspaces/
git commit -m "feat: add file upload endpoint"
```

---

## Phase 5: Frontend

### Task 5.1: Auth Context and API Client

**Files:**
- Create: `apps/web/src/lib/api-client.ts`
- Create: `apps/web/src/lib/sse-client.ts`
- Create: `apps/web/src/context/auth-context.tsx`
- Modify: `apps/web/src/routes/__root.tsx` (wrap with AuthProvider)

- [ ] **Step 1: Write API client**

Create `apps/web/src/lib/api-client.ts`:

```typescript
const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:3000";

export async function apiFetch(path: string, options: RequestInit = {}) {
  const headers: Record<string, string> = {
    ...(options.headers as Record<string, string>),
  };

  // Don't set Content-Type for FormData (browser sets with boundary)
  if (!(options.body instanceof FormData)) {
    headers["Content-Type"] = "application/json";
  }

  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
    credentials: "include", // Send httpOnly cookie
  });

  if (response.status === 401) {
    if (typeof window !== "undefined") {
      window.location.href = "/login";
    }
    throw new Error("Unauthorized");
  }

  if (!response.ok) {
    const error = await response.json().catch(() => ({ error: "Request failed" }));
    throw new Error(error.error || `HTTP ${response.status}`);
  }

  return response.json();
}

export function apiPost(path: string, body?: Record<string, unknown>) {
  return apiFetch(path, { method: "POST", body: body ? JSON.stringify(body) : undefined });
}

export function apiGet(path: string) {
  return apiFetch(path);
}

export function apiPut(path: string, body: Record<string, unknown>) {
  return apiFetch(path, { method: "PUT", body: JSON.stringify(body) });
}

export function apiDelete(path: string, body?: Record<string, unknown>) {
  return apiFetch(path, {
    method: "DELETE",
    body: body ? JSON.stringify(body) : undefined,
  });
}
```

- [ ] **Step 2: Write SSE client with reconnect**

Create `apps/web/src/lib/sse-client.ts`:

```typescript
export class SSEClient {
  private abortController: AbortController | null = null;
  private reconnectDelay = 1000;
  private maxReconnectDelay = 30000;
  private lastEventId: string | null = null;
  private url: string;
  private onMessage: (data: string) => void;
  private onStatusChange?: (status: string) => void;

  constructor(
    url: string,
    onMessage: (data: string) => void,
    onStatusChange?: (status: string) => void
  ) {
    this.url = url;
    this.onMessage = onMessage;
    this.onStatusChange = onStatusChange;
  }

  async connect() {
    this.abortController = new AbortController();

    try {
      const headers: Record<string, string> = {};
      if (this.lastEventId) {
        headers["Last-Event-ID"] = this.lastEventId;
      }

      const response = await fetch(this.url, {
        headers,
        credentials: "include", // Send httpOnly cookie for cross-origin auth
        signal: this.abortController.signal,
      });

      if (!response.body) throw new Error("No response body");

      this.onStatusChange?.("connected");
      this.reconnectDelay = 1000; // Reset on success

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n");
        buffer = lines.pop() || "";

        for (const line of lines) {
          if (line.startsWith("id:")) {
            this.lastEventId = line.slice(3).trim();
          } else if (line.startsWith("data:")) {
            const data = line.slice(5).trim();
            if (data === "[DONE]") return;
            this.onMessage(data);
          }
        }
      }
    } catch (error: unknown) {
      if (error instanceof Error && error.name === "AbortError") return;

      this.onStatusChange?.("reconnecting");
      await this.reconnect();
    }
  }

  private async reconnect() {
    await new Promise((r) => setTimeout(r, this.reconnectDelay));
    this.reconnectDelay = Math.min(this.reconnectDelay * 2, this.maxReconnectDelay);

    if (!this.abortController?.signal.aborted) {
      this.connect();
    }
  }

  disconnect() {
    this.abortController?.abort();
    this.onStatusChange?.("disconnected");
  }
}
```

- [ ] **Step 3: Write auth context**

Create `apps/web/src/context/auth-context.tsx`:

```typescript
import { createContext, useContext, useState, useEffect, ReactNode } from "react";
import { apiPost, apiGet } from "../lib/api-client";

interface User {
  id: string;
  username: string;
  displayName: string;
  role: string;
  workspaceId: string;
}

interface AuthState {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (login: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthState | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    apiGet("/api/auth/me")
      .then((data) => setUser(data.user))
      .catch(() => setUser(null))
      .finally(() => setIsLoading(false));
  }, []);

  const login = async (login: string, password: string) => {
    const data = await apiPost("/api/auth/login", { login, password });
    setUser(data.user);
  };

  const logout = async () => {
    await apiPost("/api/auth/logout");
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{ user, isLoading, isAuthenticated: !!user, login, logout }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
```

- [ ] **Step 4: Modify root route to wrap with AuthProvider**

The portal uses `createRootRoute` (TanStack Router). Open `apps/web/src/routes/__root.tsx`. You'll see something like:

```tsx
import { createRootRoute, Outlet } from "@tanstack/react-router";
import { ThemeProvider } from "@/providers/theme-provider";
// ... other imports

export const Route = createRootRoute({
  component: RootComponent,
});

function RootComponent() {
  // ... existing providers and layout
}
```

The fix: import `AuthProvider` and wrap it around the outermost provider layer:

```tsx
import { AuthProvider } from "@/context/auth-context";

// Inside RootComponent, wrap the existing JSX with AuthProvider:
function RootComponent() {
  return (
    <AuthProvider>
      <ThemeProvider>
        {/* ... existing providers and <Outlet /> ... */}
      </ThemeProvider>
    </AuthProvider>
  );
}
```

> **Note:** AuthProvider should be the outermost so all child routes have access to auth state.

- [ ] **Step 5: Commit**

```bash
git add apps/web/src/lib/ apps/web/src/context/ apps/web/src/routes/__root.tsx
git commit -m "feat: add auth context, API client, and SSE client"
```

---

### Task 5.2: Login Page

**Files:**
- Create: `apps/web/src/routes/login.tsx`
- Create: `apps/web/src/components/auth/login-form.tsx`

- [ ] **Step 1: Write login form component**

Create `apps/web/src/components/auth/login-form.tsx`:

```tsx
import { useState, FormEvent } from "react";
import { useAuth } from "../../context/auth-context";
import { useNavigate } from "@tanstack/react-router";

export function LoginForm() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError("");
    setIsSubmitting(true);

    try {
      await login(username, password);
      navigate({ to: "/chat" });
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Giriş başarısız. Lütfen tekrar deneyin.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900">
      <div className="w-full max-w-md p-8 space-y-6 bg-white dark:bg-gray-800 rounded-xl shadow-lg">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            PersonalAutonomy
          </h1>
          <p className="mt-2 text-gray-600 dark:text-gray-400">
            Kişisel AI asistanınıza giriş yapın
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Kullanıcı adı veya email
            </label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="mt-1 w-full px-3 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600 dark:text-white"
              required
              autoFocus
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Şifre
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="mt-1 w-full px-3 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600 dark:text-white"
              required
            />
          </div>

          {error && (
            <div className="p-3 text-sm text-red-600 bg-red-50 dark:bg-red-900/20 rounded-lg">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full py-2 px-4 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg disabled:opacity-50"
          >
            {isSubmitting ? "Giriş yapılıyor..." : "Giriş Yap"}
          </button>
        </form>
      </div>
    </div>
  );
}
```

- [ ] **Step 2: Write login route**

Create `apps/web/src/routes/login.tsx`:

```tsx
import { createFileRoute } from "@tanstack/react-router";
import { LoginForm } from "../components/auth/login-form";

export const Route = createFileRoute("/login")({
  component: LoginPage,
});

function LoginPage() {
  return <LoginForm />;
}
```

- [ ] **Step 3: Commit**

```bash
git add apps/web/src/routes/login.tsx apps/web/src/components/auth/login-form.tsx
git commit -m "feat: add login page with form"
```

---

### Task 5.3: Chat Page with Auth Guard

**Files:**
- Modify: `apps/web/src/routes/chat.tsx` (or existing home route)
- Create: `apps/web/src/components/layout/app-header.tsx`
- Create: `apps/web/src/components/layout/session-sidebar.tsx`
- Create: `apps/web/src/components/chat/chat-view.tsx` (SSE integration stub)

- [ ] **Step 1: Write auth-protected route wrapper**

Create `apps/web/src/components/auth/protected-route.tsx`:

```tsx
import { Navigate } from "@tanstack/react-router";
import { useAuth } from "../../context/auth-context";

export function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin h-8 w-8 border-4 border-blue-600 border-t-transparent rounded-full" />
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" />;
  }

  return <>{children}</>;
}
```

- [ ] **Step 2: Write app header**

Create `apps/web/src/components/layout/app-header.tsx`:

```tsx
import { useAuth } from "../../context/auth-context";
import { useNavigate } from "@tanstack/react-router";

export function AppHeader() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate({ to: "/login" });
  };

  return (
    <header className="flex items-center justify-between px-4 py-2 border-b bg-white dark:bg-gray-800 dark:border-gray-700">
      <div className="flex items-center gap-3">
        <span className="font-semibold text-gray-900 dark:text-white">
          PersonalAutonomy
        </span>
      </div>

      <div className="flex items-center gap-4">
        <span className="text-sm text-gray-600 dark:text-gray-400">
          {user?.displayName}
        </span>
        <span className="px-2 py-0.5 text-xs bg-blue-100 text-blue-700 rounded-full dark:bg-blue-900 dark:text-blue-300">
          {user?.role}
        </span>
        {user?.role === "admin" && (
          <button
            onClick={() => navigate({ to: "/admin" })}
            className="text-sm text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white"
          >
            Admin
          </button>
        )}
        <button
          onClick={handleLogout}
          className="text-sm text-red-600 hover:text-red-800 dark:text-red-400"
        >
          Çıkış
        </button>
      </div>
    </header>
  );
}
```

- [ ] **Step 3: Write session sidebar**

Create `apps/web/src/components/layout/session-sidebar.tsx`:

```tsx
import { useState, useEffect } from "react";
import { apiGet, apiPost, apiDelete } from "../../lib/api-client";
import { PlusIcon, TrashIcon } from "lucide-react";

interface Session {
  id: string;
  status: string;
  model: string;
  createdAt: string;
}

export function SessionSidebar({
  activeSessionId,
  onSelectSession,
}: {
  activeSessionId: string | null;
  onSelectSession: (id: string) => void;
}) {
  const [sessions, setSessions] = useState<Session[]>([]);

  const loadSessions = async () => {
    const data = await apiGet("/api/sessions");
    setSessions(data.sessions || []);
  };

  useEffect(() => {
    loadSessions();
  }, []);

  const startNewSession = async () => {
    const data = await apiPost("/api/sessions/start", {});
    setSessions((prev) => [data.session, ...prev]);
    onSelectSession(data.session.id);
  };

  const deleteSession = async (id: string) => {
    await apiDelete(`/api/sessions/${id}`);
    setSessions((prev) => prev.filter((s) => s.id !== id));
    if (activeSessionId === id) onSelectSession("");
  };

  return (
    <div className="w-64 border-r bg-gray-50 dark:bg-gray-900 dark:border-gray-700 flex flex-col">
      <div className="p-3">
        <button
          onClick={startNewSession}
          className="w-full flex items-center gap-2 px-3 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm"
        >
          <PlusIcon size={16} />
          Yeni Sohbet
        </button>
      </div>

      <div className="flex-1 overflow-y-auto">
        {sessions.map((session) => (
          <div
            key={session.id}
            onClick={() => onSelectSession(session.id)}
            className={`group flex items-center justify-between px-3 py-2 cursor-pointer text-sm ${
              activeSessionId === session.id
                ? "bg-blue-50 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300"
                : "hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-700 dark:text-gray-300"
            }`}
          >
            <span className="truncate">
              {new Date(session.createdAt).toLocaleDateString()}
            </span>
            <button
              onClick={(e) => {
                e.stopPropagation();
                deleteSession(session.id);
              }}
              className="opacity-0 group-hover:opacity-100 hover:text-red-500"
            >
              <TrashIcon size={14} />
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
```

- [ ] **Step 4: Write ChatView component with SSE integration**

Create `apps/web/src/components/chat/chat-view.tsx`:

```tsx
import { useState, useEffect, useRef, FormEvent } from "react";
import { apiPost } from "../../lib/api-client";
import { SSEClient } from "../../lib/sse-client";

interface Message {
  role: "user" | "assistant";
  content: string;
}

export function ChatView({ sessionId }: { sessionId: string }) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [status, setStatus] = useState("connecting");
  const sseRef = useRef<SSEClient | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const sse = new SSEClient(
      `${import.meta.env.VITE_API_URL || "http://localhost:3000"}/api/sessions/${sessionId}/stream`,
      (data) => {
        try {
          const parsed = JSON.parse(data);
          setMessages((prev) => [...prev, { role: "assistant", content: parsed.content || parsed }]);
        } catch {
          setMessages((prev) => [...prev, { role: "assistant", content: data }]);
        }
      },
      setStatus
    );

    sse.connect();
    sseRef.current = sse;

    return () => {
      sse.disconnect();
    };
  }, [sessionId]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async (e: FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    setMessages((prev) => [...prev, { role: "user", content: input }]);
    await apiPost(`/api/sessions/${sessionId}/message`, { message: input });
    setInput("");
  };

  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {status === "reconnecting" && (
          <div className="text-center text-sm text-yellow-600 bg-yellow-50 rounded-lg p-2">
            Bağlantı koptu, yeniden bağlanılıyor...
          </div>
        )}
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`p-3 rounded-lg max-w-[80%] ${
              msg.role === "user"
                ? "bg-blue-600 text-white ml-auto"
                : "bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white"
            }`}
          >
            {msg.content}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSend} className="border-t p-3 flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Mesaj yazın..."
          className="flex-1 px-3 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600 dark:text-white"
        />
        <button
          type="submit"
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          Gönder
        </button>
      </form>
    </div>
  );
}
```

- [ ] **Step 5: Update chat route to use auth and layout**

Update the main chat route (e.g., `apps/web/src/routes/home.tsx` or create `apps/web/src/routes/chat.tsx`):

```tsx
import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import { ProtectedRoute } from "../components/auth/protected-route";
import { AppHeader } from "../components/layout/app-header";
import { SessionSidebar } from "../components/layout/session-sidebar";
import { ChatView } from "../components/chat/chat-view";

export const Route = createFileRoute("/chat")({
  component: ChatPage,
});

function ChatPage() {
  const [activeSessionId, setActiveSessionId] = useState<string | null>(null);

  return (
    <ProtectedRoute>
      <div className="h-screen flex flex-col">
        <AppHeader />
        <div className="flex-1 flex overflow-hidden">
          <SessionSidebar
            activeSessionId={activeSessionId}
            onSelectSession={setActiveSessionId}
          />
          <main className="flex-1">
            {activeSessionId ? (
              <ChatView sessionId={activeSessionId} />
            ) : (
              <div className="flex items-center justify-center h-full text-gray-500">
                Sohbete başlamak için sol panelden bir oturum seçin
              </div>
            )}
          </main>
        </div>
      </div>
    </ProtectedRoute>
  );
}
```

- [ ] **Step 6: Commit**

```bash
git add apps/web/src/routes/chat.tsx apps/web/src/components/auth/protected-route.tsx apps/web/src/components/layout/
git commit -m "feat: add protected chat route with session sidebar"
```

---

### Task 5.4: Admin Panel

**Files:**
- Create: `apps/web/src/routes/admin/index.tsx`
- Create: `apps/web/src/routes/admin/users.tsx`
- Create: `apps/web/src/components/admin/admin-layout.tsx`
- Create: `apps/web/src/components/admin/user-table.tsx`
- Create: `apps/web/src/components/admin/user-form.tsx`

- [ ] **Step 1: Write admin layout**

Create `apps/web/src/components/admin/admin-layout.tsx`:

```tsx
import { Link, Outlet, useLocation } from "@tanstack/react-router";
import { AppHeader } from "../layout/app-header";
import { ProtectedRoute } from "../auth/protected-route";
import { useAuth } from "../../context/auth-context";

const navItems = [
  { label: "Dashboard", to: "/admin" },
  { label: "Kullanıcılar", to: "/admin/users" },
  { label: "Roller", to: "/admin/roles" },
  { label: "Session'lar", to: "/admin/sessions" },
  { label: "Log'lar", to: "/admin/logs" },
  { label: "Dosyalar", to: "/admin/files" },
];

export function AdminLayout() {
  const { user } = useAuth();
  const pathname = useLocation().pathname;

  if (user?.role !== "admin") {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <p className="text-gray-600">Bu sayfaya erişim yetkiniz yok.</p>
      </div>
    );
  }

  return (
    <ProtectedRoute>
      <div className="h-screen flex flex-col">
        <AppHeader />
        <div className="flex-1 flex">
          <nav className="w-56 border-r bg-gray-50 dark:bg-gray-900 dark:border-gray-700 p-3 space-y-1">
            {navItems.map((item) => (
              <Link
                key={item.to}
                to={item.to}
                className={`block px-3 py-2 rounded-lg text-sm ${
                  pathname === item.to
                    ? "bg-blue-50 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300"
                    : "text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-800"
                }`}
              >
                {item.label}
              </Link>
            ))}
          </nav>
          <main className="flex-1 p-6 overflow-y-auto">
            <Outlet />
          </main>
        </div>
      </div>
    </ProtectedRoute>
  );
}
```

- [ ] **Step 2: Write user table component**

Create `apps/web/src/components/admin/user-table.tsx`:

```tsx
import { useState, useEffect } from "react";
import { apiGet, apiDelete } from "../../lib/api-client";

interface User {
  id: string;
  username: string;
  email: string | null;
  displayName: string;
  isActive: boolean;
  roleName: string;
  createdAt: string;
}

export function UserTable({ onEdit }: { onEdit: (user: User) => void }) {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);

  const loadUsers = async () => {
    const data = await apiGet("/api/users");
    setUsers(data.users);
    setLoading(false);
  };

  useEffect(() => { loadUsers(); }, []);

  const handleDeactivate = async (id: string) => {
    if (!confirm("Bu kullanıcıyı pasif yapmak istediğinize emin misiniz?")) return;
    await apiDelete(`/api/users/${id}`);
    setUsers((prev) => prev.filter((u) => u.id !== id));
  };

  if (loading) return <p>Yükleniyor...</p>;

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow">
      <table className="w-full text-sm">
        <thead className="border-b dark:border-gray-700">
          <tr className="text-left text-gray-500 dark:text-gray-400">
            <th className="px-4 py-3">Kullanıcı</th>
            <th className="px-4 py-3">Rol</th>
            <th className="px-4 py-3">Durum</th>
            <th className="px-4 py-3">İşlemler</th>
          </tr>
        </thead>
        <tbody>
          {users.map((user) => (
            <tr key={user.id} className="border-b dark:border-gray-700">
              <td className="px-4 py-3">
                <div className="font-medium text-gray-900 dark:text-white">
                  {user.displayName}
                </div>
                <div className="text-gray-500">{user.username}</div>
              </td>
              <td className="px-4 py-3">
                <span className="px-2 py-0.5 bg-gray-100 dark:bg-gray-700 rounded text-xs">
                  {user.roleName}
                </span>
              </td>
              <td className="px-4 py-3">
                <span
                  className={`px-2 py-0.5 rounded text-xs ${
                    user.isActive
                      ? "bg-green-100 text-green-700"
                      : "bg-red-100 text-red-700"
                  }`}
                >
                  {user.isActive ? "Aktif" : "Pasif"}
                </span>
              </td>
              <td className="px-4 py-3 space-x-2">
                <button
                  onClick={() => onEdit(user)}
                  className="text-blue-600 hover:underline text-xs"
                >
                  Düzenle
                </button>
                <button
                  onClick={() => handleDeactivate(user.id)}
                  className="text-red-600 hover:underline text-xs"
                >
                  Pasif Yap
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
```

- [ ] **Step 3: Write user form component**

Create `apps/web/src/components/admin/user-form.tsx`:

```tsx
import { useState, FormEvent } from "react";
import { apiPost } from "../../lib/api-client";

export function UserForm({ onSuccess }: { onSuccess: () => void }) {
  const [form, setForm] = useState({
    username: "",
    email: "",
    displayName: "",
    password: "",
    roleName: "marketing-agent",
  });
  const [error, setError] = useState("");

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError("");

    try {
      await apiPost("/api/users", form);
      onSuccess();
      setForm({ username: "", email: "", displayName: "", password: "", roleName: "marketing-agent" });
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : String(err));
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 p-6 bg-white dark:bg-gray-800 rounded-lg shadow">
      <h3 className="font-semibold text-gray-900 dark:text-white">Yeni Kullanıcı Ekle</h3>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm text-gray-600 dark:text-gray-400">Kullanıcı Adı</label>
          <input
            type="text"
            value={form.username}
            onChange={(e) => setForm({ ...form, username: e.target.value })}
            className="mt-1 w-full px-3 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600 dark:text-white"
            required
          />
        </div>

        <div>
          <label className="block text-sm text-gray-600 dark:text-gray-400">Email (opsiyonel)</label>
          <input
            type="email"
            value={form.email}
            onChange={(e) => setForm({ ...form, email: e.target.value })}
            className="mt-1 w-full px-3 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600 dark:text-white"
          />
        </div>

        <div>
          <label className="block text-sm text-gray-600 dark:text-gray-400">Görünen İsim</label>
          <input
            type="text"
            value={form.displayName}
            onChange={(e) => setForm({ ...form, displayName: e.target.value })}
            className="mt-1 w-full px-3 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600 dark:text-white"
            required
          />
        </div>

        <div>
          <label className="block text-sm text-gray-600 dark:text-gray-400">Şifre</label>
          <input
            type="password"
            value={form.password}
            onChange={(e) => setForm({ ...form, password: e.target.value })}
            className="mt-1 w-full px-3 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600 dark:text-white"
            required
          />
        </div>

        <div>
          <label className="block text-sm text-gray-600 dark:text-gray-400">Rol</label>
          <select
            value={form.roleName}
            onChange={(e) => setForm({ ...form, roleName: e.target.value })}
            className="mt-1 w-full px-3 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600 dark:text-white"
          >
            <option value="marketing-agent">Pazarlama Asistanı</option>
            <option value="admin">Admin</option>
          </select>
        </div>
      </div>

      {error && (
        <div className="p-3 text-sm text-red-600 bg-red-50 rounded-lg">{error}</div>
      )}

      <button
        type="submit"
        className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm"
      >
        Kullanıcı Oluştur
      </button>
    </form>
  );
}
```

- [ ] **Step 4: Write admin users page**

Create `apps/web/src/routes/admin/users.tsx`:

```tsx
import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import { UserTable } from "../../components/admin/user-table";
import { UserForm } from "../../components/admin/user-form";

export const Route = createFileRoute("/admin/users")({
  component: AdminUsersPage,
});

function AdminUsersPage() {
  const [refreshKey, setRefreshKey] = useState(0);

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Kullanıcı Yönetimi</h2>
      <UserForm onSuccess={() => setRefreshKey((k) => k + 1)} />
      <UserTable key={refreshKey} onEdit={() => {}} />
    </div>
  );
}
```

- [ ] **Step 5: Write admin layout route (required for TanStack Router nested routes)**

Create `apps/web/src/routes/admin.tsx`:

```tsx
import { createFileRoute } from "@tanstack/react-router";
import { AdminLayout } from "../components/admin/admin-layout";

export const Route = createFileRoute("/admin")({
  component: AdminLayout,
});
```

- [ ] **Step 6: Write admin index page**

Create `apps/web/src/routes/admin/index.tsx`:

```tsx
import { createFileRoute } from "@tanstack/react-router";
import { useState, useEffect } from "react";
import { apiGet } from "../../lib/api-client";

export const Route = createFileRoute("/admin/")({
  component: AdminDashboard,
});

interface AdminStats {
  totalUsers: number;
  activeSessions: number;
  totalFiles: number;
  activeWorkspaces: number;
}

function AdminDashboard() {
  const [stats, setStats] = useState<AdminStats | null>(null);

  useEffect(() => {
    apiGet("/api/admin/stats").then((d) => setStats(d.stats));
  }, []);

  const cards = [
    { label: "Toplam Kullanıcı", value: stats?.totalUsers ?? "—" },
    { label: "Aktif Oturum", value: stats?.activeSessions ?? "—" },
    { label: "Aktif Workspace", value: stats?.activeWorkspaces ?? "—" },
    { label: "Toplam Dosya", value: stats?.totalFiles ?? "—" },
  ];

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Admin Dashboard</h2>
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {cards.map((card) => (
          <div key={card.label} className="p-4 bg-white dark:bg-gray-800 rounded-lg shadow">
            <div className="text-sm text-gray-500 dark:text-gray-400">{card.label}</div>
            <div className="mt-1 text-2xl font-bold text-gray-900 dark:text-white">{card.value}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
```

- [ ] **Step 7: Write admin roles page**

Create `apps/web/src/routes/admin/roles.tsx`:

```tsx
import { createFileRoute } from "@tanstack/react-router";
import { useState, useEffect } from "react";
import { apiGet } from "../../lib/api-client";

export const Route = createFileRoute("/admin/roles")({
  component: AdminRolesPage,
});

function AdminRolesPage() {
  const [roles, setRoles] = useState<Array<Record<string, unknown>>>([]);

  useEffect(() => {
    apiGet("/api/admin/roles").then((d) => setRoles(d.roles));
  }, []);

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Roller</h2>
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow">
        <table className="w-full text-sm">
          <thead className="border-b dark:border-gray-700">
            <tr className="text-left text-gray-500 dark:text-gray-400">
              <th className="px-4 py-3">Rol</th>
              <th className="px-4 py-3">Template</th>
              <th className="px-4 py-3">Varsayılan</th>
            </tr>
          </thead>
          <tbody>
            {roles.map((r: Record<string, unknown>) => (
              <tr key={r.id} className="border-b dark:border-gray-700">
                <td className="px-4 py-3 font-medium">{r.name}</td>
                <td className="px-4 py-3 text-gray-500">{r.templatePath}</td>
                <td className="px-4 py-3">
                  {r.isDefault ? (
                    <span className="px-2 py-0.5 bg-green-100 text-green-700 text-xs rounded">Evet</span>
                  ) : (
                    <span className="px-2 py-0.5 bg-gray-100 text-gray-600 text-xs rounded">Hayır</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
```

- [ ] **Step 8: Write admin sessions page**

Create `apps/web/src/routes/admin/sessions.tsx`:

```tsx
import { createFileRoute } from "@tanstack/react-router";
import { useState, useEffect } from "react";
import { apiGet, apiDelete } from "../../lib/api-client";

export const Route = createFileRoute("/admin/sessions")({
  component: AdminSessionsPage,
});

function AdminSessionsPage() {
  const [sessions, setSessions] = useState<Array<Record<string, unknown>>>([]);

  useEffect(() => {
    apiGet("/api/sessions").then((d) => setSessions(d.sessions));
  }, []);

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Aktif Oturumlar</h2>
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow">
        <table className="w-full text-sm">
          <thead className="border-b dark:border-gray-700">
            <tr className="text-left text-gray-500 dark:text-gray-400">
              <th className="px-4 py-3">Kullanıcı</th>
              <th className="px-4 py-3">Model</th>
              <th className="px-4 py-3">Durum</th>
              <th className="px-4 py-3">Başlangıç</th>
              <th className="px-4 py-3">İşlem</th>
            </tr>
          </thead>
          <tbody>
            {sessions.map((s: Record<string, unknown>) => (
              <tr key={s.id} className="border-b dark:border-gray-700">
                <td className="px-4 py-3">{s.displayName}</td>
                <td className="px-4 py-3">{s.model || "-"}</td>
                <td className="px-4 py-3">
                  <span className={`px-2 py-0.5 rounded text-xs ${s.status === "active" ? "bg-green-100 text-green-700" : "bg-gray-100 text-gray-600"}`}>{s.status}</span>
                </td>
                <td className="px-4 py-3 text-gray-500">{new Date(s.createdAt).toLocaleString()}</td>
                <td className="px-4 py-3">
                  <button onClick={async () => { await apiDelete(`/api/sessions/${s.id}`); setSessions((p) => p.filter((x) => x.id !== s.id)); }} className="text-red-600 hover:underline text-xs">Kapat</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
```

- [ ] **Step 9: Write admin logs page**

Create `apps/web/src/routes/admin/logs.tsx`:

```tsx
import { createFileRoute } from "@tanstack/react-router";
import { useState, useEffect } from "react";
import { apiGet } from "../../lib/api-client";

export const Route = createFileRoute("/admin/logs")({
  component: AdminLogsPage,
});

function AdminLogsPage() {
  const [logs, setLogs] = useState<Array<Record<string, unknown>>>([]);

  useEffect(() => {
    apiGet("/api/admin/logs").then((d) => setLogs(d.logs));
  }, []);

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Denetim Kayıtları</h2>
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow">
        <table className="w-full text-sm">
          <thead className="border-b dark:border-gray-700">
            <tr className="text-left text-gray-500 dark:text-gray-400">
              <th className="px-4 py-3">İşlem</th>
              <th className="px-4 py-3">Varlık</th>
              <th className="px-4 py-3">IP</th>
              <th className="px-4 py-3">Tarih</th>
            </tr>
          </thead>
          <tbody>
            {logs.map((l: Record<string, unknown>) => (
              <tr key={l.id} className="border-b dark:border-gray-700">
                <td className="px-4 py-3">{l.action}</td>
                <td className="px-4 py-3 text-gray-500">{l.entityType}/{l.entityId}</td>
                <td className="px-4 py-3 text-gray-500">{l.ipAddress || "-"}</td>
                <td className="px-4 py-3 text-gray-500">{new Date(l.createdAt).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
```

- [ ] **Step 10: Write admin files page**

Create `apps/web/src/routes/admin/files.tsx`:

```tsx
import { createFileRoute } from "@tanstack/react-router";
import { useState, useEffect } from "react";
import { apiGet } from "../../lib/api-client";

export const Route = createFileRoute("/admin/files")({
  component: AdminFilesPage,
});

function AdminFilesPage() {
  const [files, setFiles] = useState<Array<Record<string, unknown>>>([]);

  useEffect(() => {
    apiGet("/api/admin/files").then((d) => setFiles(d.files));
  }, []);

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Kullanıcı Dosyaları</h2>
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow">
        <table className="w-full text-sm">
          <thead className="border-b dark:border-gray-700">
            <tr className="text-left text-gray-500 dark:text-gray-400">
              <th className="px-4 py-3">Dosya</th>
              <th className="px-4 py-3">Boyut</th>
              <th className="px-4 py-3">Tip</th>
              <th className="px-4 py-3">Tarih</th>
            </tr>
          </thead>
          <tbody>
            {files.map((f: Record<string, unknown>) => (
              <tr key={f.id} className="border-b dark:border-gray-700">
                <td className="px-4 py-3">{f.filename}</td>
                <td className="px-4 py-3 text-gray-500">{(f.fileSize / 1024).toFixed(1)} KB</td>
                <td className="px-4 py-3 text-gray-500">{f.mimeType || "-"}</td>
                <td className="px-4 py-3 text-gray-500">{new Date(f.createdAt).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
```

- [ ] **Step 11: Write roles API endpoint**

Create `apps/web/src/server/api/admin/roles.get.ts`:

```typescript
import { authMiddleware } from "../../middleware/auth";
import { requireAdmin } from "../../middleware/admin";
import { db, schema } from "../../db";

export default defineEventHandler(async (event) => {
  const ctx = await authMiddleware(getHeaders(event), parseCookies(event));
  requireAdmin(ctx);

  const roles = await db.select().from(schema.roles);
  return { roles };
});
```

- [ ] **Step 12: Write admin logs API endpoint**

Create `apps/web/src/server/api/admin/logs.get.ts`:

```typescript
import { desc } from "drizzle-orm";
import { authMiddleware } from "../../middleware/auth";
import { requireAdmin } from "../../middleware/admin";
import { db, schema } from "../../db";

export default defineEventHandler(async (event) => {
  const ctx = await authMiddleware(getHeaders(event), parseCookies(event));
  requireAdmin(ctx);

  const logs = await db
    .select()
    .from(schema.auditLogs)
    .orderBy(desc(schema.auditLogs.createdAt))
    .limit(100);

  return { logs };
});
```

- [ ] **Step 13: Write admin files API endpoint**

Create `apps/web/src/server/api/admin/files.get.ts`:

```typescript
import { desc } from "drizzle-orm";
import { authMiddleware } from "../../middleware/auth";
import { requireAdmin } from "../../middleware/admin";
import { db, schema } from "../../db";

export default defineEventHandler(async (event) => {
  const ctx = await authMiddleware(getHeaders(event), parseCookies(event));
  requireAdmin(ctx);

  const files = await db
    .select()
    .from(schema.userFiles)
    .orderBy(desc(schema.userFiles.createdAt))
    .limit(200);

  return { files };
});
```

- [ ] **Step 14: Write admin stats API endpoint**

Create `apps/web/src/server/api/admin/stats.get.ts`:

```typescript
import { count, eq } from "drizzle-orm";
import { authMiddleware } from "../../middleware/auth";
import { requireAdmin } from "../../middleware/admin";
import { db, schema } from "../../db";

export default defineEventHandler(async (event) => {
  const ctx = await authMiddleware(getHeaders(event), parseCookies(event));
  requireAdmin(ctx);

  const [userCount] = await db.select({ value: count() }).from(schema.users);
  const [sessionCount] = await db
    .select({ value: count() })
    .from(schema.opencodeSessions)
    .where(eq(schema.opencodeSessions.status, "active"));
  const [fileCount] = await db.select({ value: count() }).from(schema.userFiles);
  const [workspaceCount] = await db
    .select({ value: count() })
    .from(schema.workspaces)
    .where(eq(schema.workspaces.isActive, true));

  return {
    stats: {
      totalUsers: userCount.value,
      activeSessions: sessionCount.value,
      totalFiles: fileCount.value,
      activeWorkspaces: workspaceCount.value,
    },
  };
});
```

- [ ] **Step 15: Commit**

```bash
git add apps/web/src/routes/admin/ apps/web/src/server/api/admin/
git commit -m "feat: add admin sessions/logs/files pages and roles API"
```

---

### Task 5.5: Role Management CRUD

**Files:**
- Create: `apps/web/src/server/api/admin/roles/[id].ts`
- Modify: `apps/web/src/server/api/admin/roles.get.ts` → `apps/web/src/server/api/admin/roles/index.get.ts`
- Create: `apps/web/src/server/api/admin/roles/index.post.ts`
- Create: `apps/web/src/components/admin/role-table.tsx`
- Create: `apps/web/src/components/admin/role-form.tsx`
- Modify: `apps/web/src/routes/admin/roles.tsx`

- [ ] **Step 1: Write role list endpoint (update existing)**

Rename `apps/web/src/server/api/admin/roles.get.ts` to `apps/web/src/server/api/admin/roles/index.get.ts` (no code change needed, Nitro handles file-based routing).

- [ ] **Step 2: Write role create endpoint**

Create `apps/web/src/server/api/admin/roles/index.post.ts`:

```typescript
import { authMiddleware } from "../../../middleware/auth";
import { requireAdmin } from "../../../middleware/admin";
import { db, schema } from "../../../db";
import { logAudit } from "../../../services/audit-logger";

export default defineEventHandler(async (event) => {
  const ctx = await authMiddleware(getHeaders(event), parseCookies(event));
  requireAdmin(ctx);

  const body = await readBody(event);
  const { name, description, templatePath, isDefault } = body;

  if (!name || !templatePath) {
    throw createError({ statusCode: 400, statusMessage: "Name and templatePath required" });
  }

  const [existing] = await db
    .select({ id: schema.roles.id })
    .from(schema.roles)
    .where(eq(schema.roles.name, name))
    .limit(1);

  if (existing) {
    throw createError({ statusCode: 409, statusMessage: "Role name already exists" });
  }

  const [role] = await db
    .insert(schema.roles)
    .values({ name, description, templatePath, isDefault: isDefault || false })
    .returning();

  await logAudit({
    userId: ctx.user.userId,
    action: "role.created",
    entityType: "role",
    entityId: String(role.id),
    newValue: { name, templatePath },
  });

  return { role };
});
```

- [ ] **Step 3: Write role update/delete endpoint**

Create `apps/web/src/server/api/admin/roles/[id].ts`:

```typescript
import { eq } from "drizzle-orm";
import { authMiddleware } from "../../../middleware/auth";
import { requireAdmin } from "../../../middleware/admin";
import { db, schema } from "../../../db";
import { logAudit } from "../../../services/audit-logger";

export default defineEventHandler(async (event) => {
  const ctx = await authMiddleware(getHeaders(event), parseCookies(event));
  requireAdmin(ctx);

  const roleId = getRouterParam(event, "id");
  if (!roleId) throw createError({ statusCode: 400, statusMessage: "Missing role ID" });

  const method = event.method;

  if (method === "GET") {
    const [role] = await db
      .select()
      .from(schema.roles)
      .where(eq(schema.roles.id, Number(roleId)))
      .limit(1);

    if (!role) throw createError({ statusCode: 404, statusMessage: "Role not found" });

    const permissions = await db
      .select()
      .from(schema.rolePermissions)
      .where(eq(schema.rolePermissions.roleId, Number(roleId)));

    return { role, permissions };
  }

  if (method === "PUT") {
    const body = await readBody(event);
    const updates: Record<string, unknown> = {};

    if (body.name !== undefined) updates.name = body.name;
    if (body.description !== undefined) updates.description = body.description;
    if (body.templatePath !== undefined) updates.templatePath = body.templatePath;
    if (body.isDefault !== undefined) updates.isDefault = body.isDefault;

    const [updated] = await db
      .update(schema.roles)
      .set(updates)
      .where(eq(schema.roles.id, Number(roleId)))
      .returning();

    await logAudit({
      userId: ctx.user.userId,
      action: "role.updated",
      entityType: "role",
      entityId: roleId,
      newValue: updates,
    });

    return { role: updated };
  }

  if (method === "DELETE") {
    const [role] = await db
      .select({ id: schema.roles.id })
      .from(schema.roles)
      .where(eq(schema.roles.id, Number(roleId)))
      .limit(1);

    if (!role) throw createError({ statusCode: 404, statusMessage: "Role not found" });

    // Check if role is in use
    const [userWithRole] = await db
      .select({ id: schema.users.id })
      .from(schema.users)
      .where(eq(schema.users.roleId, Number(roleId)))
      .limit(1);

    if (userWithRole) {
      throw createError({
        statusCode: 409,
        statusMessage: "Cannot delete role: users are assigned to it",
      });
    }

    await db.delete(schema.rolePermissions).where(eq(schema.rolePermissions.roleId, Number(roleId)));
    await db.delete(schema.roles).where(eq(schema.roles.id, Number(roleId)));

    await logAudit({
      userId: ctx.user.userId,
      action: "role.deleted",
      entityType: "role",
      entityId: roleId,
    });

    return { success: true };
  }

  throw createError({ statusCode: 405, statusMessage: "Method not allowed" });
});
```

- [ ] **Step 4: Write role table component**

Create `apps/web/src/components/admin/role-table.tsx`:

```tsx
import { useState, useEffect } from "react";
import { apiGet, apiDelete } from "../../lib/api-client";

interface Role {
  id: number;
  name: string;
  description: string | null;
  templatePath: string;
  isDefault: boolean;
}

export function RoleTable({ onEdit, refreshKey }: { onEdit: (role: Role) => void; refreshKey: number }) {
  const [roles, setRoles] = useState<Role[]>([]);
  const [loading, setLoading] = useState(true);

  const loadRoles = async () => {
    const data = await apiGet("/api/admin/roles");
    setRoles(data.roles);
    setLoading(false);
  };

  useEffect(() => { loadRoles(); }, [refreshKey]);

  const handleDelete = async (id: number) => {
    if (!confirm("Bu rolü silmek istediğinize emin misiniz? Kullanıcıları olan roller silinemez.")) return;
    try {
      await apiDelete(`/api/admin/roles/${id}`);
      setRoles((prev) => prev.filter((r) => r.id !== id));
    } catch (err: unknown) {
      alert(err instanceof Error ? err.message : "İşlem başarısız");
    }
  };

  if (loading) return <p>Yükleniyor...</p>;

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow">
      <table className="w-full text-sm">
        <thead className="border-b dark:border-gray-700">
          <tr className="text-left text-gray-500 dark:text-gray-400">
            <th className="px-4 py-3">Rol</th>
            <th className="px-4 py-3">Açıklama</th>
            <th className="px-4 py-3">Template</th>
            <th className="px-4 py-3">Varsayılan</th>
            <th className="px-4 py-3">İşlemler</th>
          </tr>
        </thead>
        <tbody>
          {roles.map((role) => (
            <tr key={role.id} className="border-b dark:border-gray-700">
              <td className="px-4 py-3 font-medium text-gray-900 dark:text-white">{role.name}</td>
              <td className="px-4 py-3 text-gray-500">{role.description || "-"}</td>
              <td className="px-4 py-3 text-gray-500 font-mono text-xs">{role.templatePath}</td>
              <td className="px-4 py-3">
                {role.isDefault ? (
                  <span className="px-2 py-0.5 bg-green-100 text-green-700 text-xs rounded">Evet</span>
                ) : (
                  <span className="px-2 py-0.5 bg-gray-100 text-gray-600 text-xs rounded">Hayır</span>
                )}
              </td>
              <td className="px-4 py-3 space-x-2">
                <button onClick={() => onEdit(role)} className="text-blue-600 hover:underline text-xs">Düzenle</button>
                {!role.isDefault && (
                  <button onClick={() => handleDelete(role.id)} className="text-red-600 hover:underline text-xs">Sil</button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
```

- [ ] **Step 5: Write role form component**

Create `apps/web/src/components/admin/role-form.tsx`:

```tsx
import { useState, FormEvent } from "react";
import { apiPost, apiPut } from "../../lib/api-client";

interface Role {
  id?: number;
  name: string;
  description: string;
  templatePath: string;
  isDefault: boolean;
}

export function RoleForm({
  role,
  onSuccess,
  onCancel,
}: {
  role?: Role;
  onSuccess: () => void;
  onCancel: () => void;
}) {
  const [form, setForm] = useState<Role>({
    name: role?.name || "",
    description: role?.description || "",
    templatePath: role?.templatePath || "templates/roles/",
    isDefault: role?.isDefault || false,
  });
  const [error, setError] = useState("");
  const isEditing = !!role?.id;

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError("");

    try {
      if (isEditing) {
        await apiPut(`/api/admin/roles/${role.id}`, form);
      } else {
        await apiPost("/api/admin/roles", form);
      }
      onSuccess();
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "İşlem başarısız");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 p-6 bg-white dark:bg-gray-800 rounded-lg shadow">
      <h3 className="font-semibold text-gray-900 dark:text-white">
        {isEditing ? "Rol Düzenle" : "Yeni Rol Oluştur"}
      </h3>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm text-gray-600 dark:text-gray-400">Rol Adı</label>
          <input
            type="text"
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
            className="mt-1 w-full px-3 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600 dark:text-white"
            required
            disabled={isEditing}
          />
        </div>

        <div>
          <label className="block text-sm text-gray-600 dark:text-gray-400">Template Yolu</label>
          <input
            type="text"
            value={form.templatePath}
            onChange={(e) => setForm({ ...form, templatePath: e.target.value })}
            className="mt-1 w-full px-3 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600 dark:text-white font-mono text-sm"
            required
          />
        </div>

        <div className="col-span-2">
          <label className="block text-sm text-gray-600 dark:text-gray-400">Açıklama</label>
          <textarea
            value={form.description}
            onChange={(e) => setForm({ ...form, description: e.target.value })}
            className="mt-1 w-full px-3 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600 dark:text-white"
            rows={2}
          />
        </div>

        <div className="flex items-center gap-2">
          <input
            type="checkbox"
            id="isDefault"
            checked={form.isDefault}
            onChange={(e) => setForm({ ...form, isDefault: e.target.checked })}
            className="rounded"
          />
          <label htmlFor="isDefault" className="text-sm text-gray-600 dark:text-gray-400">
            Varsayılan rol olarak ata
          </label>
        </div>
      </div>

      {error && (
        <div className="p-3 text-sm text-red-600 bg-red-50 rounded-lg">{error}</div>
      )}

      <div className="flex gap-2">
        <button type="submit" className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm">
          {isEditing ? "Güncelle" : "Oluştur"}
        </button>
        <button type="button" onClick={onCancel} className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 text-sm">
          İptal
        </button>
      </div>
    </form>
  );
}
```

- [ ] **Step 6: Update admin roles page**

Update `apps/web/src/routes/admin/roles.tsx`:

```tsx
import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import { RoleTable } from "../../components/admin/role-table";
import { RoleForm } from "../../components/admin/role-form";

export const Route = createFileRoute("/admin/roles")({
  component: AdminRolesPage,
});

function AdminRolesPage() {
  const [refreshKey, setRefreshKey] = useState(0);
  const [editingRole, setEditingRole] = useState<{ id: number; name: string; description: string | null; templatePath: string; isDefault: boolean } | null>(null);
  const [showForm, setShowForm] = useState(false);

  const handleSuccess = () => {
    setRefreshKey((k) => k + 1);
    setShowForm(false);
    setEditingRole(null);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Rol Yönetimi</h2>
        <button
          onClick={() => { setEditingRole(null); setShowForm(true); }}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm"
        >
          Yeni Rol Ekle
        </button>
      </div>

      {showForm && (
        <RoleForm
          role={editingRole}
          onSuccess={handleSuccess}
          onCancel={() => { setShowForm(false); setEditingRole(null); }}
        />
      )}

      <RoleTable
        key={refreshKey}
        onEdit={(role) => { setEditingRole(role); setShowForm(true); }}
        refreshKey={refreshKey}
      />
    </div>
  );
}
```

- [ ] **Step 7: Commit**

```bash
git add apps/web/src/server/api/admin/roles/ apps/web/src/components/admin/role-*.tsx apps/web/src/routes/admin/roles.tsx
git commit -m "feat: add role management CRUD with create/edit/delete"
```

---

### Task 5.6: Session Detail View

**Files:**
- Create: `apps/web/src/server/api/sessions/[id]/index.get.ts` (detail with messages)
- Create: `apps/web/src/components/admin/session-detail.tsx`
- Modify: `apps/web/src/routes/admin/sessions.tsx`

- [ ] **Step 1: Write session detail endpoint**

Create `apps/web/src/server/api/sessions/[id]/index.get.ts`:

```typescript
import { eq } from "drizzle-orm";
import { authMiddleware } from "../../../middleware/auth";
import { db, schema } from "../../../db";

export default defineEventHandler(async (event) => {
  const ctx = await authMiddleware(getHeaders(event), parseCookies(event));
  const sessionId = getRouterParam(event, "id");
  if (!sessionId) throw createError({ statusCode: 400 });

  const [session] = await db
    .select({
      id: schema.opencodeSessions.id,
      workspaceId: schema.opencodeSessions.workspaceId,
      userId: schema.opencodeSessions.userId,
      status: schema.opencodeSessions.status,
      model: schema.opencodeSessions.model,
      port: schema.opencodeSessions.port,
      pid: schema.opencodeSessions.pid,
      createdAt: schema.opencodeSessions.createdAt,
      lastActive: schema.opencodeSessions.lastActive,
      username: schema.users.username,
      displayName: schema.users.displayName,
      workspacePath: schema.workspaces.workspacePath,
    })
    .from(schema.opencodeSessions)
    .innerJoin(schema.users, eq(schema.opencodeSessions.userId, schema.users.id))
    .innerJoin(schema.workspaces, eq(schema.opencodeSessions.workspaceId, schema.workspaces.id))
    .where(eq(schema.opencodeSessions.id, sessionId))
    .limit(1);

  if (!session) throw createError({ statusCode: 404, statusMessage: "Session not found" });

  // Admin or owner can view
  if (session.userId !== ctx.user.userId && ctx.user.role !== "admin") {
    throw createError({ statusCode: 403, statusMessage: "Access denied" });
  }

  const messages = await db
    .select()
    .from(schema.chatMessages)
    .where(eq(schema.chatMessages.sessionId, sessionId))
    .orderBy(schema.chatMessages.createdAt);

  return { session, messages };
});
```

- [ ] **Step 2: Write session detail component**

Create `apps/web/src/components/admin/session-detail.tsx`:

```tsx
import { useState, useEffect } from "react";
import { apiGet } from "../../lib/api-client";

interface Message {
  id: string;
  role: string;
  content: string;
  createdAt: string;
}

interface SessionDetail {
  id: string;
  status: string;
  model: string | null;
  createdAt: string;
  lastActive: string;
  username: string;
  displayName: string;
  workspacePath: string;
  messages: Message[];
}

export function SessionDetail({ sessionId, onClose }: { sessionId: string; onClose: () => void }) {
  const [detail, setDetail] = useState<SessionDetail | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiGet(`/api/sessions/${sessionId}`).then((data) => {
      setDetail(data.session ? { ...data.session, messages: data.messages } : null);
      setLoading(false);
    });
  }, [sessionId]);

  if (loading) return <div className="p-4">Yükleniyor...</div>;
  if (!detail) return <div className="p-4 text-red-600">Oturum bulunamadı</div>;

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-xl w-full max-w-3xl max-h-[80vh] flex flex-col">
        <div className="flex items-center justify-between p-4 border-b dark:border-gray-700">
          <div>
            <h3 className="font-semibold text-gray-900 dark:text-white">Oturum Detayı</h3>
            <p className="text-sm text-gray-500">{detail.displayName} • {detail.model || "Varsayılan model"}</p>
          </div>
          <button onClick={onClose} className="text-gray-500 hover:text-gray-700">✕</button>
        </div>

        <div className="flex-1 overflow-y-auto p-4 space-y-3">
          {detail.messages.length === 0 ? (
            <p className="text-gray-500 text-center py-8">Henüz mesaj yok</p>
          ) : (
            detail.messages.map((msg) => (
              <div
                key={msg.id}
                className={`p-3 rounded-lg max-w-[85%] ${
                  msg.role === "user"
                    ? "bg-blue-100 dark:bg-blue-900/30 ml-auto text-right"
                    : "bg-gray-100 dark:bg-gray-700"
                }`}
              >
                <div className="text-xs text-gray-500 mb-1">
                  {msg.role === "user" ? detail.displayName : "Agent"} •{" "}
                  {new Date(msg.createdAt).toLocaleTimeString()}
                </div>
                <div className="text-sm text-gray-800 dark:text-gray-200 whitespace-pre-wrap">
                  {msg.content}
                </div>
              </div>
            ))
          )}
        </div>

        <div className="p-4 border-t dark:border-gray-700 text-xs text-gray-500">
         /workspace: {detail.workspacePath} • PID: - • Status: {detail.status}
        </div>
      </div>
    </div>
  );
}
```

- [ ] **Step 3: Update admin sessions page**

Update `apps/web/src/routes/admin/sessions.tsx` to include detail modal:

```tsx
import { createFileRoute } from "@tanstack/react-router";
import { useState, useEffect } from "react";
import { apiGet, apiDelete } from "../../lib/api-client";
import { SessionDetail } from "../../components/admin/session-detail";

export const Route = createFileRoute("/admin/sessions")({
  component: AdminSessionsPage,
});

interface AdminSession {
  id: string;
  status: string;
  model: string | null;
  createdAt: string;
  lastActive: string;
  username: string;
  displayName: string;
  workspacePath?: string;
}

function AdminSessionsPage() {
  const [sessions, setSessions] = useState<AdminSession[]>([]);
  const [selectedSessionId, setSelectedSessionId] = useState<string | null>(null);

  useEffect(() => {
    apiGet("/api/sessions").then((d) => setSessions(d.sessions));
  }, []);

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Aktif Oturumlar</h2>
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow">
        <table className="w-full text-sm">
          <thead className="border-b dark:border-gray-700">
            <tr className="text-left text-gray-500 dark:text-gray-400">
              <th className="px-4 py-3">Kullanıcı</th>
              <th className="px-4 py-3">Model</th>
              <th className="px-4 py-3">Durum</th>
              <th className="px-4 py-3">Son Aktif</th>
              <th className="px-4 py-3">İşlemler</th>
            </tr>
          </thead>
          <tbody>
            {sessions.map((s: Record<string, unknown>) => (
              <tr key={s.id} className="border-b dark:border-gray-700">
                <td className="px-4 py-3">{s.displayName}</td>
                <td className="px-4 py-3">{s.model || "-"}</td>
                <td className="px-4 py-3">
                  <span className={`px-2 py-0.5 rounded text-xs ${s.status === "active" ? "bg-green-100 text-green-700" : "bg-gray-100 text-gray-600"}`}>{s.status}</span>
                </td>
                <td className="px-4 py-3 text-gray-500">{new Date(s.lastActive).toLocaleString()}</td>
                <td className="px-4 py-3 space-x-2">
                  <button
                    onClick={() => setSelectedSessionId(s.id)}
                    className="text-blue-600 hover:underline text-xs"
                  >
                    Detay
                  </button>
                  <button
                    onClick={async () => {
                      if (!confirm("Bu oturumu kapatmak istediğinize emin misiniz?")) return;
                      await apiDelete(`/api/sessions/${s.id}`);
                      setSessions((p) => p.filter((x) => x.id !== s.id));
                    }}
                    className="text-red-600 hover:underline text-xs"
                  >
                    Kapat
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {selectedSessionId && (
        <SessionDetail
          sessionId={selectedSessionId}
          onClose={() => setSelectedSessionId(null)}
        />
      )}
    </div>
  );
}
```

- [ ] **Step 4: Commit**

```bash
git add apps/web/src/server/api/sessions/[id]/index.get.ts apps/web/src/components/admin/session-detail.tsx apps/web/src/routes/admin/sessions.tsx
git commit -m "feat: add session detail view with message history"
```

---

### Task 5.7: File Management (Download/Delete)

**Files:**
- Create: `apps/web/src/server/api/admin/files/[id].ts`
- Create: `apps/web/src/server/api/admin/files/[id]/download.get.ts`
- Modify: `apps/web/src/routes/admin/files.tsx`

- [ ] **Step 1: Write file delete endpoint**

Create `apps/web/src/server/api/admin/files/[id].ts`:

```typescript
import { eq } from "drizzle-orm";
import { unlink } from "fs/promises";
import { authMiddleware } from "../../../middleware/auth";
import { requireAdmin } from "../../../middleware/admin";
import { db, schema } from "../../../db";
import { logAudit } from "../../../services/audit-logger";

export default defineEventHandler(async (event) => {
  const ctx = await authMiddleware(getHeaders(event), parseCookies(event));
  requireAdmin(ctx);

  const fileId = getRouterParam(event, "id");
  if (!fileId) throw createError({ statusCode: 400, statusMessage: "Missing file ID" });

  if (event.method === "DELETE") {
    const [file] = await db
      .select()
      .from(schema.userFiles)
      .where(eq(schema.userFiles.id, fileId))
      .limit(1);

    if (!file) throw createError({ statusCode: 404, statusMessage: "File not found" });

    // Delete from filesystem
    try {
      await unlink(file.filePath);
    } catch {
      // File may already be deleted
    }

    await db.delete(schema.userFiles).where(eq(schema.userFiles.id, fileId));

    await logAudit({
      userId: ctx.user.userId,
      action: "file.deleted",
      entityType: "file",
      entityId: fileId,
      oldValue: { filename: file.filename, filePath: file.filePath },
    });

    return { success: true };
  }

  throw createError({ statusCode: 405, statusMessage: "Method not allowed" });
});
```

- [ ] **Step 2: Write file download endpoint**

Create `apps/web/src/server/api/admin/files/[id]/download.get.ts`:

```typescript
import { eq } from "drizzle-orm";
import { createReadStream, existsSync } from "fs";
import { join } from "path";
import { authMiddleware } from "../../../../middleware/auth";
import { requireAdmin } from "../../../../middleware/admin";
import { db, schema } from "../../../../db";

export default defineEventHandler(async (event) => {
  const ctx = await authMiddleware(getHeaders(event), parseCookies(event));
  requireAdmin(ctx);

  const fileId = getRouterParam(event, "id");
  if (!fileId) throw createError({ statusCode: 400, statusMessage: "Missing file ID" });

  const [file] = await db
    .select()
    .from(schema.userFiles)
    .where(eq(schema.userFiles.id, fileId))
    .limit(1);

  if (!file) throw createError({ statusCode: 404, statusMessage: "File not found" });

  if (!existsSync(file.filePath)) {
    throw createError({ statusCode: 404, statusMessage: "File not found on disk" });
  }

  setHeader(event, "Content-Type", file.mimeType || "application/octet-stream");
  setHeader(event, "Content-Disposition", `attachment; filename="${file.filename}"`);

  const stream = createReadStream(file.filePath);
  return stream;
});
```

- [ ] **Step 3: Update admin files page**

Update `apps/web/src/routes/admin/files.tsx` to include download/delete buttons:

```tsx
import { createFileRoute } from "@tanstack/react-router";
import { useState, useEffect } from "react";
import { apiGet, apiDelete } from "../../lib/api-client";

export const Route = createFileRoute("/admin/files")({
  component: AdminFilesPage,
});

function AdminFilesPage() {
  const [files, setFiles] = useState<Array<Record<string, unknown>>>([]);

  useEffect(() => {
    apiGet("/api/admin/files").then((d) => setFiles(d.files));
  }, []);

  const handleDelete = async (id: string, filename: string) => {
    if (!confirm(`"${filename}" dosyasını silmek istediğinize emin misiniz?`)) return;
    try {
      await apiDelete(`/api/admin/files/${id}`);
      setFiles((prev) => prev.filter((f) => f.id !== id));
    } catch (err: unknown) {
      alert(err instanceof Error ? err.message : "İşlem başarısız");
    }
  };

  const handleDownload = (id: string) => {
    window.open(`${import.meta.env.VITE_API_URL || "http://localhost:3000"}/api/admin/files/${id}/download`, "_blank");
  };

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Kullanıcı Dosyaları</h2>
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow">
        <table className="w-full text-sm">
          <thead className="border-b dark:border-gray-700">
            <tr className="text-left text-gray-500 dark:text-gray-400">
              <th className="px-4 py-3">Dosya</th>
              <th className="px-4 py-3">Boyut</th>
              <th className="px-4 py-3">Tip</th>
              <th className="px-4 py-3">Tarih</th>
              <th className="px-4 py-3">İşlemler</th>
            </tr>
          </thead>
          <tbody>
            {files.map((f: Record<string, unknown>) => (
              <tr key={f.id} className="border-b dark:border-gray-700">
                <td className="px-4 py-3 font-medium">{f.filename}</td>
                <td className="px-4 py-3 text-gray-500">{(f.fileSize / 1024).toFixed(1)} KB</td>
                <td className="px-4 py-3 text-gray-500">{f.mimeType || "-"}</td>
                <td className="px-4 py-3 text-gray-500">{new Date(f.createdAt).toLocaleString()}</td>
                <td className="px-4 py-3 space-x-2">
                  <button
                    onClick={() => handleDownload(f.id)}
                    className="text-blue-600 hover:underline text-xs"
                  >
                    İndir
                  </button>
                  <button
                    onClick={() => handleDelete(f.id, f.filename)}
                    className="text-red-600 hover:underline text-xs"
                  >
                    Sil
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
```

- [ ] **Step 4: Commit**

```bash
git add apps/web/src/server/api/admin/files/ apps/web/src/routes/admin/files.tsx
git commit -m "feat: add file download and delete for admin"
```

---

### Task 5.8: User Edit Form Integration

**Files:**
- Modify: `apps/web/src/components/admin/user-table.tsx`
- Modify: `apps/web/src/routes/admin/users.tsx`

- [ ] **Step 1: Update user table to support edit mode**

Update `apps/web/src/components/admin/user-table.tsx` to show edit button properly:

```tsx
// Add to the existing UserTable component's interface:
interface User {
  id: string;
  username: string;
  email: string | null;
  displayName: string;
  isActive: boolean;
  roleName: string;
  createdAt: string;
  resourceLimitsOverride: Record<string, unknown> | null;
  workspaceId: string | null;
}

// Update the table rows to include resource limits display and edit button:
// In the <td> for İşlemler, add:
<button
  onClick={() => onEdit(user)}
  className="text-blue-600 hover:underline text-xs"
>
  Düzenle
</button>

// Add a new column for resource limits:
<td className="px-4 py-3 text-xs text-gray-500">
  {user.resourceLimitsOverride ? "Özel" : "Varsayılan"}
</td>
```

- [ ] **Step 2: Create user edit modal component**

Create `apps/web/src/components/admin/user-edit-modal.tsx`:

```tsx
import { useState, FormEvent, useEffect } from "react";
import { apiGet, apiPut } from "../../lib/api-client";

interface User {
  id: string;
  username: string;
  email: string | null;
  displayName: string;
  isActive: boolean;
  roleName: string;
  resourceLimitsOverride: Record<string, unknown> | null;
  workspaceId: string | null;
  workspacePath: string | null;
  linuxUser: string | null;
}

export function UserEditModal({ userId, onClose, onSuccess }: { userId: string; onClose: () => void; onSuccess: () => void }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [form, setForm] = useState({
    displayName: "",
    email: "",
    isActive: true,
    resourceLimitsOverride: null as Record<string, unknown> | null,
  });
  const [error, setError] = useState("");

  useEffect(() => {
    apiGet(`/api/users/${userId}`).then((data: { user: User }) => {
      setUser(data.user);
      setForm({
        displayName: data.user.displayName,
        email: data.user.email || "",
        isActive: data.user.isActive,
        resourceLimitsOverride: data.user.resourceLimitsOverride,
      });
      setLoading(false);
    });
  }, [userId]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError("");

    try {
      await apiPut(`/api/users/${userId}`, form);
      onSuccess();
      onClose();
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "İşlem başarısız");
    }
  };

  if (loading) return <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50"><div className="bg-white p-4 rounded">Yükleniyor...</div></div>;

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-xl w-full max-w-lg">
        <div className="flex items-center justify-between p-4 border-b dark:border-gray-700">
          <h3 className="font-semibold text-gray-900 dark:text-white">Kullanıcı Düzenle</h3>
          <button onClick={onClose} className="text-gray-500 hover:text-gray-700">✕</button>
        </div>

        <form onSubmit={handleSubmit} className="p-4 space-y-4">
          <div>
            <label className="block text-sm text-gray-600 dark:text-gray-400">Kullanıcı Adı</label>
            <input
              type="text"
              value={user?.username || ""}
              className="mt-1 w-full px-3 py-2 border rounded-lg bg-gray-100 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
              disabled
            />
          </div>

          <div>
            <label className="block text-sm text-gray-600 dark:text-gray-400">Görünen İsim</label>
            <input
              type="text"
              value={form.displayName}
              onChange={(e) => setForm({ ...form, displayName: e.target.value })}
              className="mt-1 w-full px-3 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600 dark:text-white"
              required
            />
          </div>

          <div>
            <label className="block text-sm text-gray-600 dark:text-gray-400">Email</label>
            <input
              type="email"
              value={form.email}
              onChange={(e) => setForm({ ...form, email: e.target.value })}
              className="mt-1 w-full px-3 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600 dark:text-white"
            />
          </div>

          <div className="flex items-center gap-2">
            <input
              type="checkbox"
              id="isActive"
              checked={form.isActive}
              onChange={(e) => setForm({ ...form, isActive: e.target.checked })}
              className="rounded"
            />
            <label htmlFor="isActive" className="text-sm text-gray-600 dark:text-gray-400">Aktif</label>
          </div>

          <div className="text-xs text-gray-500">
            <p>Workspace: {user?.workspacePath || "Yok"}</p>
            <p>Linux User: {user?.linuxUser || "Yok"}</p>
          </div>

          {error && (
            <div className="p-3 text-sm text-red-600 bg-red-50 rounded-lg">{error}</div>
          )}

          <div className="flex gap-2 justify-end">
            <button type="button" onClick={onClose} className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg text-sm">
              İptal
            </button>
            <button type="submit" className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm">
              Kaydet
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
```

- [ ] **Step 3: Update admin users page to use edit modal**

Update `apps/web/src/routes/admin/users.tsx`:

```tsx
import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import { UserTable } from "../../components/admin/user-table";
import { UserForm } from "../../components/admin/user-form";
import { UserEditModal } from "../../components/admin/user-edit-modal";

export const Route = createFileRoute("/admin/users")({
  component: AdminUsersPage,
});

function AdminUsersPage() {
  const [refreshKey, setRefreshKey] = useState(0);
  const [editingUserId, setEditingUserId] = useState<string | null>(null);

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Kullanıcı Yönetimi</h2>
      <UserForm onSuccess={() => setRefreshKey((k) => k + 1)} />
      <UserTable
        key={refreshKey}
        onEdit={(user) => setEditingUserId(user.id)}
      />

      {editingUserId && (
        <UserEditModal
          userId={editingUserId}
          onClose={() => setEditingUserId(null)}
          onSuccess={() => setRefreshKey((k) => k + 1)}
        />
      )}
    </div>
  );
}
```

- [ ] **Step 4: Commit**

```bash
git add apps/web/src/components/admin/user-table.tsx apps/web/src/components/admin/user-edit-modal.tsx apps/web/src/routes/admin/users.tsx
git commit -m "feat: add user edit modal with resource limits and workspace info"
```

---

### Task 5.9: Per-User Workspace Customization (Admin File Editor)

> **Motivation:** Task 3.1'deki symlink stratejisi sayesinde template güncellemeleri tüm kullanıcılara anında yansır. Ancak admin bazı kullanıcılara özel prompt, skill veya MCP konfigürasyonu vermek isteyebilir (örn: Ahmet'e ekstra bir araştırma skill'i, Mehmet'e özel bir AGENTS.md yönergesi). Şu an symlink olduğu için bireysel değişiklik yapılamaz — dosyayı düzenlemek template'i değiştirir ve herkesi etkiler.

> **Çözüm:** Admin bir kullanıcının workspace dosyasını düzenlemeye kalktığında symlink otomatik kırılır, dosyanın kopyası oluşturulur ve değişiklik kopya üzerine yapılır. Bu kullanıcı artık template'ten bağımsız olur. "Şablona sıfırla" butonu ile symlink geri oluşturulabilir.

**Files:**
- Create: `apps/web/src/server/services/workspace-file-manager.ts`
- Create: `apps/web/src/server/api/admin/users/[id]/workspace-files.get.ts`
- Create: `apps/web/src/server/api/admin/users/[id]/workspace-files/index.put.ts`
- Create: `apps/web/src/routes/admin/workspace-files.tsx`
- Create: `apps/web/src/components/admin/workspace-file-editor.tsx`

- [ ] **Step 1: Write workspace file manager service**

Create `apps/web/src/server/services/workspace-file-manager.ts`:

```typescript
import { readFile, writeFile, symlink as symlinkFs, unlink, stat, readdir } from "fs/promises";
import { join, resolve } from "path";
import { db, schema } from "../db";
import { eq } from "drizzle-orm";

interface FileEntry {
  name: string;
  path: string;
  isSymlink: boolean;
  isDirectory: boolean;
  size: number;
  modifiedAt: Date;
}

const WORKSPACES_ROOT = process.env.WORKSPACES_ROOT || "/opt/personalautonomy/workspaces";

/**
 * Checks whether a path is a symlink. Returns the link target if it is, null otherwise.
 */
async function resolveSymlink(filePath: string): Promise<{ isSymlink: boolean; target: string | null }> {
  const { lstat, readlink } = await import("fs/promises");
  try {
    const stats = await lstat(filePath);
    if (stats.isSymbolicLink()) {
      const target = await readlink(filePath);
      return { isSymlink: true, target };
    }
    return { isSymlink: false, target: null };
  } catch {
    return { isSymlink: false, target: null };
  }
}

/**
 * Lists config files in a user's workspace root.
 * Returns: AGENTS.md, mcps.json, and directories (skills/, agents/).
 * Excludes data/ and logs/ — those are user data, not admin-managed config.
 */
export async function listWorkspaceFiles(linuxUser: string): Promise<FileEntry[]> {
  const workspaceDir = join(WORKSPACES_ROOT, linuxUser);
  const entries = await readdir(workspaceDir, { withFileTypes: true });
  const files: FileEntry[] = [];

  for (const entry of entries) {
    if (entry.name === "data" || entry.name === "logs") continue;

    const fullPath = join(workspaceDir, entry.name);
    const { isSymlink, target } = await resolveSymlink(fullPath);
    const s = await stat(fullPath).catch(() => null);

    files.push({
      name: entry.name,
      path: fullPath,
      isSymlink,
      isDirectory: entry.isDirectory() || entry.isSymbolicLink(),
      size: s?.size ?? 0,
      modifiedAt: s?.mtime ?? new Date(),
    });
  }

  return files;
}

/**
 * Reads file content. If the path is a directory or doesn't exist, returns null.
 */
export async function readWorkspaceFile(linuxUser: string, fileName: string): Promise<{ content: string; isSymlink: boolean } | null> {
  const workspaceDir = join(WORKSPACES_ROOT, linuxUser);
  const fullPath = join(workspaceDir, fileName);

  // Security: don't allow path traversal
  if (!fullPath.startsWith(resolve(workspaceDir))) {
    throw new Error("Access denied: path must be within workspace directory");
  }

  try {
    const content = await readFile(fullPath, "utf-8");
    const { isSymlink } = await resolveSymlink(fullPath);
    return { content, isSymlink };
  } catch {
    return null;
  }
}

/**
 * Writes file content.
 * If the file is currently a symlink, it BREAKS the symlink first (copies template),
 * then writes the new content to the copy. This user is now custom.
 */
export async function writeWorkspaceFile(
  linuxUser: string,
  fileName: string,
  content: string
): Promise<{ custom: boolean }> {
  const workspaceDir = join(WORKSPACES_ROOT, linuxUser);
  const fullPath = join(workspaceDir, fileName);

  if (!fullPath.startsWith(resolve(workspaceDir))) {
    throw new Error("Access denied");
  }

  const { isSymlink } = await resolveSymlink(fullPath);

  if (isSymlink) {
    // Break symlink: unlink the symlink, write a real file
    await unlink(fullPath);
  }

  await writeFile(fullPath, content, "utf-8");

  // Ensure workspace user owns the new custom file
  const { exec } = await import("child_process");
  const { promisify } = await import("util");
  const execAsync = promisify(exec);
  try {
    await execAsync(`chown ${linuxUser}:${linuxUser} "${fullPath}"`, { timeout: 3000 });
  } catch {
    // Ownership is best-effort; file is still writable by nitro-runner
  }

  return { custom: true };
}

/**
 * Reset a file to template: delete the custom copy and re-create the symlink.
 */
export async function resetToTemplate(linuxUser: string, fileName: string, roleName: string): Promise<void> {
  const workspaceDir = join(WORKSPACES_ROOT, linuxUser);
  const fullPath = join(workspaceDir, fileName);
  const templatesRoot = process.env.TEMPLATES_ROOT || "/opt/personalautonomy/templates/roles";
  const templatePath = join(templatesRoot, roleName, fileName);

  if (!fullPath.startsWith(resolve(workspaceDir))) {
    throw new Error("Access denied");
  }

  // Remove existing file or symlink
  try {
    await unlink(fullPath);
  } catch {
    // File may not exist
  }

  // Re-create symlink
  await symlinkFs(templatePath, fullPath);
}
```

- [ ] **Step 2: Write admin workspace files list endpoint**

Create `apps/web/src/server/api/admin/users/[id]/workspace-files.get.ts`:

```typescript
import { eq } from "drizzle-orm";
import { authMiddleware } from "../../../../middleware/auth";
import { requireAdmin } from "../../../../middleware/admin";
import { db, schema } from "../../../../db";
import { listWorkspaceFiles } from "../../../../services/workspace-file-manager";

export default defineEventHandler(async (event) => {
  const ctx = await authMiddleware(getHeaders(event), parseCookies(event));
  requireAdmin(ctx);

  const userId = getRouterParam(event, "id");
  if (!userId) throw createError({ statusCode: 400, statusMessage: "Missing user ID" });

  const [user] = await db
    .select({
      linuxUser: schema.workspaces.linuxUser,
      workspacePath: schema.workspaces.workspacePath,
      roleName: schema.roles.name,
    })
    .from(schema.users)
    .innerJoin(schema.workspaces, eq(schema.users.id, schema.workspaces.userId))
    .innerJoin(schema.roles, eq(schema.users.roleId, schema.roles.id))
    .where(eq(schema.users.id, userId))
    .limit(1);

  if (!user) throw createError({ statusCode: 404, statusMessage: "User or workspace not found" });

  const files = await listWorkspaceFiles(user.linuxUser);

  return { files, roleName: user.roleName, linuxUser: user.linuxUser };
});
```

- [ ] **Step 3: Write admin workspace file read/write endpoint**

Create `apps/web/src/server/api/admin/users/[id]/workspace-files/index.put.ts`:

```typescript
import { eq } from "drizzle-orm";
import { authMiddleware } from "../../../../../middleware/auth";
import { requireAdmin } from "../../../../../middleware/admin";
import { db, schema } from "../../../../../db";
import { readWorkspaceFile, writeWorkspaceFile, resetToTemplate } from "../../../../../services/workspace-file-manager";
import { logAudit } from "../../../../../services/audit-logger";

export default defineEventHandler(async (event) => {
  const ctx = await authMiddleware(getHeaders(event), parseCookies(event));
  requireAdmin(ctx);

  const userId = getRouterParam(event, "id");
  if (!userId) throw createError({ statusCode: 400, statusMessage: "Missing user ID" });

  const [user] = await db
    .select({
      linuxUser: schema.workspaces.linuxUser,
      roleName: schema.roles.name,
    })
    .from(schema.users)
    .innerJoin(schema.workspaces, eq(schema.users.id, schema.workspaces.userId))
    .innerJoin(schema.roles, eq(schema.users.roleId, schema.roles.id))
    .where(eq(schema.users.id, userId))
    .limit(1);

  if (!user) throw createError({ statusCode: 404, statusMessage: "User or workspace not found" });

  const method = getHeader(event, "x-http-method-override") || event.method;

  if (method === "GET") {
    const query = getQuery(event);
    const fileName = query.file as string;
    if (!fileName) throw createError({ statusCode: 400, statusMessage: "?file= param required" });

    const result = await readWorkspaceFile(user.linuxUser, fileName);
    if (!result) throw createError({ statusCode: 404, statusMessage: "File not found" });

    return { fileName, ...result };
  }

  if (method === "PUT") {
    const body = await readBody(event);
    const { fileName, content } = body;

    if (!fileName || content === undefined) {
      throw createError({ statusCode: 400, statusMessage: "fileName and content required" });
    }

    // Only allow editing config files, not data/ or logs/
    const allowedFiles = ["AGENTS.md", "mcps.json"];
    if (!allowedFiles.includes(fileName)) {
      throw createError({ statusCode: 400, statusMessage: `Cannot edit ${fileName}. Allowed: ${allowedFiles.join(", ")}` });
    }

    const result = await writeWorkspaceFile(user.linuxUser, fileName, content);

    await logAudit({
      userId: ctx.user.userId,
      action: "workspace.file.edited",
      entityType: "workspace",
      entityId: userId,
      newValue: { fileName, userId },
    });

    return { success: true, custom: result.custom };
  }

  if (method === "DELETE") {
    const body = await readBody(event);
    const { fileName } = body;

    if (!fileName) throw createError({ statusCode: 400, statusMessage: "fileName required" });

    await resetToTemplate(user.linuxUser, fileName, user.roleName);

    await logAudit({
      userId: ctx.user.userId,
      action: "workspace.file.reset",
      entityType: "workspace",
      entityId: userId,
      newValue: { fileName, resetTo: "template" },
    });

    return { success: true };
  }

  throw createError({ statusCode: 405, statusMessage: "Method not allowed" });
});
```

- [ ] **Step 4: Write admin workspace files page (frontend)**

Create `apps/web/src/routes/admin/workspace-files.tsx`:

```tsx
import { createFileRoute } from "@tanstack/react-router";
import { useState, useEffect } from "react";
import { apiGet, apiPut, apiDelete } from "../../lib/api-client";
import { WorkspaceFileEditor } from "../../components/admin/workspace-file-editor";

interface FileEntry {
  name: string;
  isSymlink: boolean;
  isDirectory: boolean;
  size: number;
}

export const Route = createFileRoute("/admin/workspace-files")({
  component: AdminWorkspaceFilesPage,
});

function AdminWorkspaceFilesPage() {
  const [users, setUsers] = useState<Array<Record<string, unknown>>>([]);
  const [selectedUserId, setSelectedUserId] = useState<string | null>(null);
  const [files, setFiles] = useState<FileEntry[]>([]);
  const [editingFile, setEditingFile] = useState<string | null>(null);
  const [fileContent, setFileContent] = useState("");
  const [isCustom, setIsCustom] = useState(false);
  const [roleName, setRoleName] = useState("");
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");

  useEffect(() => {
    apiGet("/api/users").then((d) => setUsers(d.users));
  }, []);

  const loadFiles = async (userId: string) => {
    setSelectedUserId(userId);
    const data = await apiGet(`/api/admin/users/${userId}/workspace-files`);
    setFiles(data.files);
    setRoleName(data.roleName);
    setEditingFile(null);
  };

  const openFile = async (fileName: string) => {
    const data = await apiGet(
      `/api/admin/users/${selectedUserId}/workspace-files?file=${encodeURIComponent(fileName)}`
    );
    setFileContent(data.content);
    setIsCustom(!data.isSymlink);
    setEditingFile(fileName);
  };

  const saveFile = async () => {
    if (!selectedUserId || !editingFile) return;
    setSaving(true);
    try {
      const data = await apiPut(`/api/admin/users/${selectedUserId}/workspace-files`, {
        fileName: editingFile,
        content: fileContent,
      });
      setIsCustom(data.custom);
      setMessage("Dosya kaydedildi. Kullanıcı artık şablondan bağımsız.");
      await loadFiles(selectedUserId);
    } catch (err: unknown) {
      setMessage(`Hata: ${err instanceof Error ? err.message : String(err)}`);
    } finally {
      setSaving(false);
    }
  };

  const resetToTemplate = async () => {
    if (!selectedUserId || !editingFile) return;
    if (!confirm(`${editingFile} dosyası şablona sıfırlansın mı? Tüm özel değişiklikler silinecek.`)) return;
    setSaving(true);
    try {
      await apiDelete(`/api/admin/users/${selectedUserId}/workspace-files`, {
        fileName: editingFile,
      });
      setMessage("Şablona sıfırlandı.");
      await loadFiles(selectedUserId);
      openFile(editingFile);
    } catch (err: unknown) {
      setMessage(`Hata: ${err instanceof Error ? err.message : String(err)}`);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
        Kullanıcı Workspace Dosyaları
      </h2>

      <div className="flex gap-4">
        <select
          value={selectedUserId || ""}
          onChange={(e) => loadFiles(e.target.value)}
          className="px-3 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600 dark:text-white text-sm"
        >
          <option value="">Kullanıcı seçin...</option>
          {users.map((u) => (
            <option key={u.id} value={u.id}>
              {u.displayName} ({u.username}) — {u.roleName}
            </option>
          ))}
        </select>
      </div>

      {selectedUserId && (
        <div className="flex gap-6">
          {/* File list */}
          <div className="w-64 bg-white dark:bg-gray-800 rounded-lg shadow p-3">
            <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Dosyalar ({roleName})
            </h3>
            {files.map((f) => (
              <button
                key={f.name}
                onClick={() => openFile(f.name)}
                className={`w-full text-left px-3 py-1.5 rounded text-sm flex items-center justify-between ${
                  editingFile === f.name
                    ? "bg-blue-50 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300"
                    : "hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300"
                }`}
              >
                <span>{f.name}</span>
                <span className="text-xs">
                  {f.isSymlink ? "🔗" : "✏️"}
                </span>
              </button>
            ))}
          </div>

          {/* Editor */}
          <div className="flex-1 bg-white dark:bg-gray-800 rounded-lg shadow p-4">
            {editingFile ? (
              <WorkspaceFileEditor
                fileName={editingFile}
                content={fileContent}
                isCustom={isCustom}
                roleName={roleName}
                saving={saving}
                message={message}
                onChange={setFileContent}
                onSave={saveFile}
                onReset={resetToTemplate}
              />
            ) : (
              <p className="text-gray-500 text-sm">
                Düzenlemek için sol panelden bir dosya seçin.
              </p>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
```

- [ ] **Step 5: Write file editor component**

Create `apps/web/src/components/admin/workspace-file-editor.tsx`:

```tsx
interface Props {
  fileName: string;
  content: string;
  isCustom: boolean;
  roleName: string;
  saving: boolean;
  message: string;
  onChange: (value: string) => void;
  onSave: () => void;
  onReset: () => void;
}

export function WorkspaceFileEditor({
  fileName,
  content,
  isCustom,
  roleName,
  saving,
  message,
  onChange,
  onSave,
  onReset,
}: Props) {
  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <h3 className="font-medium text-gray-900 dark:text-white">{fileName}</h3>
          {isCustom ? (
            <span className="px-2 py-0.5 text-xs bg-yellow-100 text-yellow-700 rounded-full">
              Özel — şablondan bağımsız
            </span>
          ) : (
            <span className="px-2 py-0.5 text-xs bg-green-100 text-green-700 rounded-full">
              Şablon ({roleName})
            </span>
          )}
        </div>

        <div className="flex gap-2">
          {isCustom && (
            <button
              onClick={onReset}
              disabled={saving}
              className="px-3 py-1 text-xs border border-gray-300 text-gray-600 rounded hover:bg-gray-50 disabled:opacity-50 dark:border-gray-600 dark:text-gray-400"
            >
              Şablona Sıfırla
            </button>
          )}
          <button
            onClick={onSave}
            disabled={saving}
            className="px-3 py-1 text-xs bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
          >
            {saving ? "Kaydediliyor..." : "Kaydet"}
          </button>
        </div>
      </div>

      {message && (
        <div className={`p-2 text-xs rounded ${
          message.startsWith("Hata")
            ? "bg-red-50 text-red-600"
            : "bg-green-50 text-green-600"
        }`}>
          {message}
        </div>
      )}

      <textarea
        value={content}
        onChange={(e) => onChange(e.target.value)}
        className="w-full h-96 px-3 py-2 font-mono text-sm border rounded-lg dark:bg-gray-700 dark:border-gray-600 dark:text-white resize-y"
        spellCheck={false}
      />

      <p className="text-xs text-gray-400">
        {fileName === "AGENTS.md"
          ? "Bu dosya AI agent'ın sistem prompt'unu ve yeteneklerini belirler. Markdown formatında."
          : "Bu dosya MCP (Model Context Protocol) sunucu bağlantılarını belirler. JSON formatında."}
        {" "}Değişiklik yaptığınızda kullanıcı şablondan bağımsız hale gelir — artık template güncellemelerinden etkilenmez.
      </p>
    </div>
  );
}
```

- [ ] **Step 6: Add route to admin navigation**

Update `apps/web/src/components/admin/admin-layout.tsx` — navItems dizisine şu satırı ekle:

```tsx
{ label: "Workspace Dosyaları", to: "/admin/workspace-files" },
```

- [ ] **Step 7: Commit**

```bash
git add apps/web/src/server/services/workspace-file-manager.ts apps/web/src/server/api/admin/users/[id]/workspace-files* apps/web/src/routes/admin/workspace-files.tsx apps/web/src/components/admin/workspace-file-editor.tsx apps/web/src/components/admin/admin-layout.tsx
git commit -m "feat: add per-user workspace file editor with symlink break on edit"
```

---

## Phase 6: Deployment

### Task 6.0: VPS Setup (Sıfırdan Sunucu Kurulumu)

> **Bu task'ın tamamını sen yapacaksın.** Sıfır bir VPS'i PersonalAutonomy'yi çalıştıracak hale getirecek tüm adımları içerir. Hetzner CX22 (2 vCPU, 4 GB RAM, 40 GB SSD, ~4€/ay) önerilir. Ubuntu 24.04 LTS seç.

---

#### Adım 0: VPS Satın Al

1. [hetzner.com/cloud](https://hetzner.com/cloud) → hesap aç
2. **"Add Server"** → şu ayarları seç:
   - Location: **Nuremberg** veya **Falkenstein** (Almanya, ping düşük)
   - Image: **Ubuntu 24.04 LTS**
   - Type: **CX22** (2 vCPU, 4 GB RAM, 40 GB SSD, 20 TB trafik)
   - IPv4: **Açık** (gelmesi ~30 sn)
   - **SSH Key ekleme:** Aşağıdaki Adım 1'de SSH key oluşturup buraya yapıştıracaksın. Şimdilik boş geç, sonradan eklenebilir.
3. **"Create & Buy"** → ödeme
4. Sunucu 30-60 saniyede hazır. Dashboard'da **IP adresini** ve **root şifresini** gör

---

#### Adım 1: Kendi bilgisayarından SSH bağlantısı kur

Bilgisayarında PowerShell (Admin) aç:

**1a. SSH anahtarı oluştur (daha önce Task 6.2 için oluşturduysan tekrar yapma, aynısını kullan):**

```powershell
ssh-keygen -t ed25519 -f "$env:USERPROFILE\.ssh\vps_root" -N '""'
```

Bu komut 2 dosya oluşturur:
- `C:\Users\KULLANICI\.ssh\vps_root` — özel anahtar (sakla)
- `C:\Users\KULLANICI\.ssh\vps_root.pub` — açık anahtar (VPS'e kopyalanacak)

**1b. Açık anahtarı göster (kopyalamak için):**

```powershell
Get-Content "$env:USERPROFILE\.ssh\vps_root.pub"
```

Çıkan uzun metni (ssh-ed25519 AAAA... ile başlar) **tamamını kopyala**.

**1c. Hetzner panelinde SSH Key ekle:**
- Hetzner Cloud Console → sol menü → **"SSH Keys"** → **"Add SSH Key"**
- Name: `kendi-pc`
- Key: **kopyaladığın açık anahtarı yapıştır**
- "Add" butonuna tıkla

**1d. VPS sunucuna SSH Key ata:**
- **"Servers"** → sunucunun üstüne tıkla → **"Rebuild"** (yeniden kur)
- Image: Ubuntu 24.04, SSH Key: `kendi-pc` seçili olsun
- "Rebuild" — 30 saniye sürer

**1e. Bağlantıyı test et:**

```powershell
ssh -i "$env:USERPROFILE\.ssh\vps_root" root@VPS-IP-ADRESIN
```

`VPS-IP-ADRESIN` yerine Hetzner panelinde gördüğün IP'yi yaz. Örn: `root@5.161.142.10`

Bağlanabilmen lazım. İlk bağlantıda "Are you sure you want to continue connecting?" sorusuna `yes` yaz.

---

#### Adım 2: VPS temel güvenlik ayarları

VPS'e bağlandıktan sonra (root olarak) şunları yap:

**2a. Sistemi güncelle:**

```bash
apt update && apt upgrade -y
```

**2b. Zaman dilimini ayarla:**

```bash
timedatectl set-timezone Europe/Istanbul
```

**2c. Hostname ayarla:**

```bash
hostnamectl set-hostname pa-vps
```

**2d. Swap oluştur (4 GB RAM'e ek, OpenCode process'leri için güvenlik):**

```bash
fallocate -l 2G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo '/swapfile none swap sw 0 0' >> /etc/fstab
```

**2e. SSH'ı güvenli hale getir:**

```bash
# SSH config'i düzenle
nano /etc/ssh/sshd_config
```

Şu satırları bul ve değerlerini değiştir (başında # varsa kaldır):
```
PermitRootLogin prohibit-password   # root şifre ile girişi kapat, sadece SSH key
PasswordAuthentication no           # şifre ile girişi tamamen kapat
PubkeyAuthentication yes            # SSH key ile giriş açık
```

Kaydet (Ctrl+X, Y, Enter) ve SSH'ı yeniden başlat:
```bash
systemctl restart sshd
```

> **ÖNEMLİ:** Bu pencereyi kapatma! Yeni bir PowerShell penceresi aç ve tekrar bağlanmayı dene. Bağlanamazsan hata var demektir, eski pencereden düzelt. Bağlanabiliyorsan devam et.

---

#### Adım 3: nitro-runner kullanıcısını oluştur

VPS'te (root olarak):

```bash
# Sistem kullanıcısı oluştur (login yok, ev dizini yok)
useradd -r -s /sbin/nologin -M nitro-runner

# nitro-runner'ın OpenCode process'lerini yönetebilmesi için sudo yetkisi ver
# (Bu geçici — Task 3.1'deki sudoers dosyasıyla değiştirilecek)
echo 'nitro-runner ALL=(ALL) NOPASSWD: ALL' > /etc/sudoers.d/nitro-runner
chmod 440 /etc/sudoers.d/nitro-runner
visudo -cf /etc/sudoers.d/nitro-runner
```

> **Not:** Sonraki adımda Task 3.1'deki kısıtlı sudoers ile değiştirilecek. Şimdilik full access.

---

#### Adım 4: Gerekli yazılımları kur

**4a. Temel araçlar:**

```bash
apt install -y curl git unzip gzip nginx certbot python3-certbot-nginx cron
```

**4b. Docker + Docker Compose:**

```bash
# Docker
curl -fsSL https://get.docker.com | bash

# Docker Compose (standalone binary)
curl -SL https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Docker'ı başlat ve otomatik başlatmayı aç
systemctl enable docker
systemctl start docker
```

**4c. Bun:**

```bash
curl -fsSL https://bun.sh/install | bash
# Kurulum betiği PATH'i otomatik ekler.
# root için hemen kullanılabilir olması için:
source /root/.bashrc
bun --version
```

**4d. OpenCode:**

```bash
curl -fsSL https://opencode.ai/install | bash
# PATH'e eklendiğini doğrula:
opencode --version
```

**4e. PM2:**

```bash
bun install -g pm2
pm2 --version
```

---

#### Adım 5: Dizin yapısını oluştur

```bash
# Ana uygulama dizini
mkdir -p /opt/personalautonomy

# Workspace'ler (kullanıcı başına bir dizin)
mkdir -p /opt/personalautonomy/workspaces

# Template'ler
mkdir -p /opt/personalautonomy/templates/roles

# Script'ler
mkdir -p /opt/personalautonomy/scripts

# Log'lar (PM2 + Nitro + Nginx)
mkdir -p /opt/personalautonomy/logs

# Backup'lar (günlük pg_dump buraya)
mkdir -p /opt/backups/db

# Sahiplik
chown -R root:root /opt/personalautonomy
chown -R root:root /opt/backups
```

---

#### Adım 6: Domain ve SSL (ilk deploy'dan SONRA yap)

Bu adımı **Task 6.1 ve ilk deploy tamamlandıktan sonra** yapacaksın:

```bash
# Cloudflare veya domain sağlayıcında DNS A kaydı ekle:
# api.PERSONALAUTONOMY.COM → VPS-IP-ADRESIN

# Nginx config'i oluştur (Task 6.1'deki api.conf)
nano /etc/nginx/sites-available/api.conf
# ... yapıştır ...

ln -s /etc/nginx/sites-available/api.conf /etc/nginx/sites-enabled/
nginx -t
systemctl reload nginx

# SSL sertifikası al
certbot --nginx -d api.PERSONALAUTONOMY.COM
# E-posta sorarsa kendi e-postanı gir
# "Redirect HTTP to HTTPS" → 2 (redirect)
```

---

#### Adım 7: UFW Firewall (Task 6.1 Step 5 ile aynı)

```bash
# Önce SSH portunu aç (kendini kilitleme!)
ufw allow 22/tcp

# Web portlarını aç
ufw allow 80/tcp
ufw allow 443/tcp

# PostgreSQL'i sadece localhost'a aç (dışarıya kapalı)
# docker-compose zaten 127.0.0.1:5432'ye map'liyor, ek ayar gerekmez

# Firewall'u aktif et
ufw --force enable
ufw status verbose
```

Beklenen çıktı:
```
22/tcp    ALLOW IN    Anywhere
80/tcp    ALLOW IN    Anywhere
443/tcp   ALLOW IN    Anywhere
```

---

#### Adım 8: SSH config'ini kolaylaştır (kendi bilgisayarında)

Bilgisayarında PowerShell'de:

```powershell
# SSH config dosyasını oluştur (yoksa)
$sshConfig = "$env:USERPROFILE\.ssh\config"
if (-not (Test-Path $sshConfig)) { New-Item $sshConfig -ItemType File }

# Config'e ekle:
@"

Host pa-vps
    HostName VPS-IP-ADRESIN
    User root
    IdentityFile ~/.ssh/vps_root
"@ | Out-File -Append $sshConfig
```

Artık `ssh pa-vps` yazarak direkt bağlanabilirsin. `VPS-IP-ADRESIN` yerine kendi IP'ni yaz.

---

#### Adım 9: İlk deploy'u yap

```bash
# VPS'te:
cd /opt/personalautonomy
git clone https://github.com/kocakburhan/portal.git .

# Bağımlılıkları kur
cd apps/web
bun install

# .env dosyasını oluştur (proje root'unda)
cp /opt/personalautonomy/.env.example /opt/personalautonomy/.env
nano /opt/personalautonomy/.env
# → DB_PASSWORD, JWT_SECRET, VITE_API_URL değerlerini doldur

# Docker PostgreSQL'i başlat
cd /opt/personalautonomy
docker-compose up -d

# Migration'ları çalıştır
cd /opt/personalautonomy
bun drizzle-kit push

# Build al
cd apps/web
bun run build

# PM2 ile başlat
pm2 start /opt/personalautonomy/ecosystem.config.cjs
pm2 save
pm2 startup
# PM2'nin verdiği komutu kopyala-yapıştır (root olarak çalıştırmanı ister)
```

---

#### Adım 10: Her şey çalışıyor mu kontrol et

```bash
# PostgreSQL ayakta mı?
docker ps | grep pa-postgres

# PM2 process ayakta mı?
pm2 status

# Health endpoint cevap veriyor mu?
curl http://localhost:3000/api/health

# Nginx çalışıyor mu?
systemctl status nginx

# Log'ları kontrol et
pm2 logs nitro-api --lines 20
```

---

### Task 6.1: Docker, Nginx, PM2, and CI/CD

**Files:**
- Create: `docker-compose.yml`
- Create: `nginx/api.conf`
- Create: `ecosystem.config.cjs`
- Create: `.github/workflows/deploy.yml`

- [ ] **Step 1: Write docker-compose.yml**

Create `docker-compose.yml`:

```yaml
services:
  postgres:
    image: postgres:16-alpine
    container_name: pa-postgres
    restart: unless-stopped
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: personalautonomy
    ports:
      - "127.0.0.1:5432:5432"
    volumes:
      - ./data/postgres:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
```

- [ ] **Step 2: Write Nginx config**

Create `nginx/api.conf`:

```nginx
server {
    listen 80;
    server_name api.personalautonomy.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name api.personalautonomy.com;

    ssl_certificate /etc/letsencrypt/live/api.personalautonomy.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.personalautonomy.com/privkey.pem;

    location /api/ {
        if ($request_method = 'OPTIONS') {
            add_header 'Access-Control-Allow-Origin' 'https://personalautonomy.vercel.app' always;
            add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS' always;
            add_header 'Access-Control-Allow-Headers' 'Authorization, Content-Type' always;
            add_header 'Access-Control-Allow-Credentials' 'true' always;
            add_header 'Access-Control-Max-Age' 1728000;
            add_header 'Content-Length' 0;
            return 204;
        }

        add_header 'Access-Control-Allow-Origin' 'https://personalautonomy.vercel.app' always;
        add_header 'Access-Control-Allow-Credentials' 'true' always;

        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        proxy_read_timeout 86400s;
        proxy_buffering off;
    }
}
```

- [ ] **Step 3: Write PM2 ecosystem config**

Create `ecosystem.config.cjs`:

```javascript
module.exports = {
  apps: [
    {
      name: "nitro-api",
      script: "./apps/web/.output/server/index.mjs",
      interpreter: "bun",
      user: "nitro-runner",
      cwd: "/opt/personalautonomy",
      env: {
        NODE_ENV: "production",
        PORT: 3000,
      },
      autorestart: true,
      max_memory_restart: "1G",
      error_file: "/opt/personalautonomy/logs/nitro-error.log",
      out_file: "/opt/personalautonomy/logs/nitro-out.log",
    },
  ],
};
```

- [ ] **Step 4: Write CI/CD workflow**

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to VPS
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.VPS_HOST }}
          username: ${{ secrets.VPS_USER }}
          key: ${{ secrets.VPS_SSH_KEY }}
          script: |
            cd /opt/personalautonomy
            git pull origin main
            cd apps/web
            bun install
            cd /opt/personalautonomy && bun drizzle-kit push
            bun run build
            pm2 restart nitro-api
            pm2 save

  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to Vercel
        run: npx vercel --prod --token=${{ secrets.VERCEL_TOKEN }} --yes
```

- [ ] **Step 5: Configure UFW firewall (VPS'te çalıştır)**

SSH ile VPS'e bağlan ve sırayla aşağıdaki komutları çalıştır:

```bash
# Mevcut kuralları kontrol et
sudo ufw status

# Varsayılan: gelen trafiği engelle, giden trafiğe izin ver
sudo ufw default deny incoming
sudo ufw default allow outgoing

# SSH erişimi (bu olmadan VPS'e erişemezsin!)
sudo ufw allow 22/tcp

# HTTP ve HTTPS (Nginx)
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# PostgreSQL'i SADECE localhost'a kısıtla (dışarıdan erişim yok)
# docker-compose zaten 127.0.0.1:5432 bind ediyor ama UFW ek güvenlik katmanı
sudo ufw deny 5432

# Firewall'ı etkinleştir
sudo ufw enable

# Doğrula
sudo ufw status verbose
```

Beklenen çıktı:
```
Status: active
To                         Action      From
--                         ------      ----
22/tcp                     ALLOW       Anywhere
80/tcp                     ALLOW       Anywhere
443/tcp                    ALLOW       Anywhere
5432                       DENY        Anywhere
```

> **Dikkat:** `ufw enable` komutundan önce 22/tcp kuralını eklediğinden emin ol, yoksa SSH bağlantın kesilir!

- [ ] **Step 6: Commit**

```bash
git add docker-compose.yml nginx/api.conf ecosystem.config.cjs .github/workflows/deploy.yml
git commit -m "feat: add deployment configs and CI/CD pipeline"
```

---

### Task 6.2: Backup Strategy

> **Motivation:** docker-compose.yml'da PostgreSQL volume'ü `./data/postgres` altında ancak herhangi bir yedekleme mekanizması tanımlı değil. Volume kaybı durumunda tüm kullanıcı, workspace, oturum, audit log ve chat mesajı verileri geri döndürülemez şekilde silinir. Ayrıca kullanıcı workspace'leri de (`/opt/personalautonomy/workspaces/`) VPS diskinde tutulduğu için aynı riski taşır.

**Strateji:** VPS'te günlük `pg_dump` (cron, 00:00) + kendi bilgisayarına günlük `rclone` pull (Task Scheduler, 00:00). Son 30 günlük yedekler saklanır.

**PC'de ne lazım (Docker gerekmez):**
- Windows 10/11 built-in OpenSSH Client (zaten var, bir ayar açılacak)
- rclone (tek bir `.exe`, 20 MB, `winget install rclone` ile 10 saniyede kurulur)
- D:\ sürücüsünde boş yer (>= 50 GB önerilir, 5-10 kullanıcı için fazlasıyla yeterli)

**Mimari:**
```
VPS (Hetzner)                              Kendi Bilgisayarın (Windows)
┌──────────────────────┐                   ┌───────────────────────────┐
│  /opt/personalautonomy│                   │  D:\backups\               │
│  ├── data/postgres/   │     rclone       │  ├── personalautonomy/     │
│  └── workspaces/      │ ←─────────────── │  │   ├── db/              │
│                        │  (SFTP, pull)    │  │   │  ├── 2026-05-30.sql.gz
│  /opt/backups/db/     │                   │  │   │  └── ...           │
│  ├── 2026-05-30.sql.gz│                   │  │   └── workspaces/      │
│  └── ...              │                   │  │       └── ...          │
└──────────────────────┘                   │  └── pull-backup.log      │
                                           └───────────────────────────┘
```

**Files:**
- Create: `scripts/backup.sh` (VPS yedeği)
- Create: `scripts/pull-backup.ps1` (Windows tarafı, rclone ile)
- Modify: `docs/README.md` (yedek geri yükleme talimatı)

---

#### PC Ön Hazırlık Adımları (kendi Windows bilgisayarında yapılacak)

> **Önemli:** Bu 3 adım sadece **bir kere** yapılır. Docker veya WSL kurmana gerek yok. Tek ihtiyacın Windows 10 veya 11.

---

- [ ] **Step 1: PowerShell'i Admin olarak aç**

Klavyende **Windows tuşuna** bas, `powershell` yaz. Çıkan sonuçta **"Yönetici olarak çalıştır"** yazısına tıkla (veya sağ tıkla → Yönetici olarak çalıştır).

Açılan mavi pencere PowerShell. Bundan sonraki tüm komutları bu pencereye yazıp Enter'a basarak çalıştıracaksın.

---

- [ ] **Step 2: OpenSSH Client'ı aç ve SSH anahtarı oluştur**

Windows 10/11'de OpenSSH zaten yüklü gelir ama kapalı olabilir. Sırayla yap:

**2a. SSH'ın açık olup olmadığını kontrol et.** Aşağıdaki komutu PowerShell'e yaz, Enter'a bas:

```powershell
Get-WindowsCapability -Online | Where-Object Name -like "OpenSSH.Client*"
```

Çıkan yazıda `State : Installed` görüyorsan sorun yok, 2b adımına geç.

`State : NotPresent` görüyorsan SSH kapalı demektir. Açmak için şunu yaz:

```powershell
Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0
```

"Restart Needed : False" yazısını gördüğünde tamamdır, bilgisayarı yeniden başlatmana gerek yok.

**2b. VPS'e şifresiz bağlanmak için SSH anahtarı oluştur.** Bu sayede her yedek çekmede şifre girmek zorunda kalmazsın:

```powershell
ssh-keygen -t ed25519 -f "$env:USERPROFILE\.ssh\vps_yedek" -N '""'
```

Çıktı şuna benzer olacak:
```
Your identification has been saved in C:\Users\kocak\.ssh\vps_yedek
Your public key has been saved in C:\Users\kocak\.ssh\vps_yedek.pub
```

Bu 2 dosya oluştu:
- `C:\Users\KULLANICIADIN\.ssh\vps_yedek` ← **özel anahtar** (bunu kimseyle paylaşma)
- `C:\Users\KULLANICIADIN\.ssh\vps_yedek.pub` ← **açık anahtar** (bunu VPS'e kopyalayacaksın)

**2c. Açık anahtarı VPS'e kopyala** (VPS şifreni son bir kez gireceksin):

```powershell
type "$env:USERPROFILE\.ssh\vps_yedek.pub" | ssh root@VPS-IP-ADRESIN "cat >> ~/.ssh/authorized_keys"
```

> `VPS-IP-ADRESIN` yerine kendi VPS'inin IP adresini yaz. Örn: `ssh root@5.161.142.10`

Şifreni soracak, VPS şifreni gir. Başarılı olursa hiçbir çıktı vermez, direkt yeni satıra geçer.

**2d. Şifresiz bağlantıyı test et:**

```powershell
ssh -i "$env:USERPROFILE\.ssh\vps_yedek" root@VPS-IP-ADRESIN "echo baglanti-basarili"
```

`baglanti-basarili` yazısını görüyorsan tamamdır. `exit` yazıp çık.

> **Sorun çıkarsa:** VPS'te `~/.ssh/authorized_keys` dosyasının izinlerini kontrol et:
> ```bash
> chmod 700 ~/.ssh
> chmod 600 ~/.ssh/authorized_keys
> ```

---

- [ ] **Step 3: rclone kur**

rclone nedir? VPS'indeki dosyaları kendi bilgisayarına kopyalamaya yarayan bir program. Tek bir `.exe` dosyası, başka hiçbir şeye ihtiyacı yok.

**3a. rclone'ı yükle:**

PowerShell'de şunu yaz (hala Admin modunda olmalısın):

```powershell
winget install rclone
```

Çıktıda `Successfully installed` yazısını görene kadar bekle (~30 saniye).

**3b. Yüklendiğini doğrula:**

```powershell
rclone version
```

Şuna benzer bir çıktı almalısın:
```
rclone v1.70.0
- os/version: Microsoft Windows 11 Pro 23H2 (64 bit)
```

---

- [ ] **Step 4: rclone'ı VPS'e bağlanacak şekilde ayarla**

Bu adımı **1 kere** yapacaksın. rclone VPS bilgilerini kaydedecek, sonraki tüm yedeklemelerde otomatik kullanacak.

**4a. Sihirbazı başlat:**

```powershell
rclone config
```

**4b. Sırayla aşağıdakileri yaz.** Ok işaretinden (→) sonrası senin yazacağın şey. Hiçbir şey yazmayan satırlarda direkt Enter'a bas.

```
No remotes found, make a new one?
n) New remote
s) Set configuration password
q) Quit config
n/s/q> n                          → n yaz, Enter

name> vps                          → vps yaz, Enter (bu ismi aklında tut, script'te kullanılacak)

Storage> sftp                      → sftp yaz, Enter

host> VPS-IP-ADRESIN               → KENDİ VPS IP ADRESİNİ YAZ, Enter

user> root                         → root yaz, Enter

port> 22                           → direkt Enter (22 varsayılan)

key_file> C:\Users\KOCAK\.ssh\vps_yedek   → ÖNEMLİ: SSH özel anahtarının tam yolu
                                           → KOCAK yerine kendi kullanıcı adını yaz
                                           → Adım 2b'deki çıktıya bak, orada yol yazıyor

(Yine Enter'a basarak devam et — aşağıdakilerin hepsini boş geç)
key_pass>
key_use_agent>
pass>
shell_type>
md5sum_command>
sha1sum_command>

Bu noktada rclone sana bir özet gösterecek:
[vps]
type = sftp
host = 5.161.142.10
user = root
key_file = C:\Users\KOCAK\.ssh\vps_yedek

y) Yes this is OK                        → y yaz, Enter
e) Edit this remote
d) Delete this remote

Current remotes:
Name                 Type
====                 ====
vps                  sftp

e/n/d/r/c/s/q> q                        → q yaz, Enter (çıkış)
```

**4c. Bağlantıyı test et:**

```powershell
rclone lsd vps:/opt
```

Eğer VPS'indeki `/opt` dizininin alt klasörlerini listeliyorsa bağlantı tamamdır. Hata alırsan `key_file` yolunu kontrol et, en sık yapılan hata orası.

> **En sık hata:** `key_file` yolundaki kullanıcı adını yanlış yazmak.
> Doğru yolu bulmak için PowerShell'de şunu çalıştır:
> ```powershell
> echo "$env:USERPROFILE\.ssh\vps_yedek"
> ```
> Çıkan yolu birebir kopyalayıp rclone config'te `key_file` satırına yapıştır.

---

#### VPS Yedekleme (VPS üzerinde yapılacak)

- [ ] **Step 5: VPS yedekleme scripti**

Create `scripts/backup.sh`:

```bash
#!/bin/bash
# VPS tarafında günlük veritabanı yedeği alır.
# Cron: 0 0 * * * /opt/personalautonomy/scripts/backup.sh

set -e

BACKUP_DIR="/opt/backups/db"
DB_NAME="personalautonomy"
DB_USER="postgres"
RETENTION_DAYS=30
TIMESTAMP=$(date +%Y%m%d)
BACKUP_FILE="$BACKUP_DIR/$TIMESTAMP.sql.gz"

mkdir -p "$BACKUP_DIR"

# pg_dump al ve sıkıştır (PostgreSQL docker container'ında çalıştığı için docker exec ile)
docker exec pa-postgres pg_dump -U "$DB_USER" "$DB_NAME" | gzip > "$BACKUP_FILE"

# 30 günden eski yedekleri sil
find "$BACKUP_DIR" -name "*.sql.gz" -mtime +$RETENTION_DAYS -delete

echo "[$(date)] Backup created: $BACKUP_FILE ($(du -h "$BACKUP_FILE" | cut -f1))"
echo "[$(date)] Retention: $(ls -1 "$BACKUP_DIR"/*.sql.gz 2>/dev/null | wc -l) files"
```

```bash
chmod +x scripts/backup.sh
```

- [ ] **Step 6: VPS cron job**

VPS'te aşağıdaki cron satırını ekle (gece 00:00):

```bash
(crontab -l 2>/dev/null; echo "0 0 * * * /opt/personalautonomy/scripts/backup.sh >> /opt/backups/db/backup.log 2>&1") | crontab -
```

Doğrula:
```bash
crontab -l
# Çıktı: 0 0 * * * /opt/personalautonomy/scripts/backup.sh >> /opt/backups/db/backup.log 2>&1
```

- [ ] **Step 7: Windows tarafı yedek çekme scripti (rclone ile)**

Create `scripts/pull-backup.ps1`:

```powershell
<#
.SYNOPSIS
    VPS'ten D:\backups\personalautonomy\ altına veritabanı ve workspace yedeklerini çeker.
    Windows Task Scheduler ile her gün 00:00'da çalıştırılır.
    Gereksinim: rclone (winget install rclone), OpenSSH Client (Windows built-in)
    Docker gerekmez.
#>

$ErrorActionPreference = "Stop"

# === YAPILANDIRMA (kendi değerlerin ile değiştir) ===
$RCLONE_REMOTE = "vps"                          # rclone config'de tanımladığın remote adı
$VPS_DB_BACKUP_DIR = "/opt/backups/db"           # VPS'te yedeklerin bulunduğu dizin
$VPS_WORKSPACES_DIR = "/opt/personalautonomy/workspaces"  # VPS'te workspace root
$LOCAL_BACKUP_ROOT = "D:\backups\personalautonomy"
# ==================================================

$LOCAL_DB_DIR = Join-Path $LOCAL_BACKUP_ROOT "db"
$LOCAL_WORKSPACES_DIR = Join-Path $LOCAL_BACKUP_ROOT "workspaces"
$LOG_FILE = Join-Path $LOCAL_BACKUP_ROOT "pull-backup.log"
$DATE = Get-Date -Format "yyyyMMdd"

# Dizinleri oluştur
foreach ($dir in @($LOCAL_DB_DIR, $LOCAL_WORKSPACES_DIR)) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
}

function Write-Log {
    param([string]$Message)
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$ts $Message" | Out-File -Append -FilePath $LOG_FILE -Encoding utf8
    Write-Host "$ts $Message"
}

Write-Log "=== Yedek çekme başladı (rclone SFTP) ==="

# 1. Veritabanı yedeklerini çek
Write-Log "DB yedekleri çekiliyor: $RCLONE_REMOTE`:$VPS_DB_BACKUP_DIR → $LOCAL_DB_DIR"
try {
    rclone sync "$RCLONE_REMOTE`:$VPS_DB_BACKUP_DIR" "$LOCAL_DB_DIR" --progress --log-level INFO 2>&1 | ForEach-Object { Write-Log $_ }
    Write-Log "DB yedekleri başarıyla çekildi"
}
catch {
    Write-Log "HATA: DB yedekleri çekilemedi: $_"
}

# 2. Workspace'leri çek (kullanıcı dosya upload'ları, agent log'ları vs.)
Write-Log "Workspace'ler çekiliyor: $RCLONE_REMOTE`:$VPS_WORKSPACES_DIR → $LOCAL_WORKSPACES_DIR"
try {
    rclone sync "$RCLONE_REMOTE`:$VPS_WORKSPACES_DIR" "$LOCAL_WORKSPACES_DIR" --progress --log-level INFO 2>&1 | ForEach-Object { Write-Log $_ }
    Write-Log "Workspace'ler başarıyla çekildi"
}
catch {
    Write-Log "HATA: Workspace'ler çekilemedi: $_"
}

# 3. Yerel retention: 30 günden eski .sql.gz dosyalarını sil
$cutoff = (Get-Date).AddDays(-30)
Get-ChildItem -Path $LOCAL_DB_DIR -Filter "*.sql.gz" -ErrorAction SilentlyContinue |
    Where-Object { $_.LastWriteTime -lt $cutoff } |
    ForEach-Object {
        Write-Log "Eski yedek siliniyor: $($_.Name) ($(($_.Length / 1MB).ToString('0.0')) MB)"
        Remove-Item $_.FullName -Force
    }

# Özet
$dbCount = (Get-ChildItem -Path $LOCAL_DB_DIR -Filter "*.sql.gz" -ErrorAction SilentlyContinue).Count
$dbSize = (Get-ChildItem -Path $LOCAL_DB_DIR -Filter "*.sql.gz" -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum / 1MB
Write-Log "=== Yedek çekme tamamlandı | DB: $dbCount dosya, ${dbSize:N0} MB | Yerel dizin: $LOCAL_BACKUP_ROOT ==="
```

> **Not:** `rclone sync` komutu `rsync` gibi çalışır — sadece değişen dosyaları aktarır. Her seferinde tüm dosyaları yeniden kopyalamaz.

- [ ] **Step 8: Windows Task Scheduler görevi**

PowerShell'i **Administrator** olarak aç ve aşağıdaki komutu çalıştır:

```powershell
$ScriptPath = "D:\Projects\PersonalAutonomy\scripts\pull-backup.ps1"

$Action = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$ScriptPath`""

$Trigger = New-ScheduledTaskTrigger -Daily -At "00:00"

$Principal = New-ScheduledTaskPrincipal `
    -UserId "SYSTEM" `
    -LogonType ServiceAccount `
    -RunLevel Highest

$Settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBattery `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RestartCount 3 `
    -RestartInterval (New-TimeSpan -Minutes 10) `
    -ExecutionTimeLimit (New-TimeSpan -Hours 2)

Register-ScheduledTask `
    -TaskName "PersonalAutonomy-Yedek" `
    -Action $Action `
    -Trigger $Trigger `
    -Principal $Principal `
    -Settings $Settings `
    -Description "Her gece 00:00'da VPS'ten rclone ile yedek çeker. PC kapalıysa ilk açılışta çalışır."

# Manuel test:
# Start-ScheduledTask -TaskName "PersonalAutonomy-Yedek"
# Get-ScheduledTask -TaskName "PersonalAutonomy-Yedek" | Get-ScheduledTaskInfo
```

> **Edge case'ler:**
> - Bilgisayar 00:00'da kapalıysa → `StartWhenAvailable` ile ilk açılışta çalışır
> - rclone bağlantı koparsa → 3 kez yeniden dener (`RestartCount 3`)
> - Yedek 2 saatten uzun sürerse → timeout, ertesi gün tekrar (`ExecutionTimeLimit`)
> - SYSTEM kullanıcısının rclone config'i → `rclone config file` çıktısını not al, SYSTEM'in kullanıcı profilinde olmadığı için config dosyasının tam yolunu script'e eklemen gerekebilir. Çözüm: rclone'ı mevcut kullanıcınla kur, `$env:APPDATA\rclone\rclone.conf` yolunu `--config "C:\Users\KULLANICIADIN\AppData\Roaming\rclone\rclone.conf"` olarak rclone komutlarına ekle.

- [ ] **Step 9: Yedekleri doğrulama (ilk çalıştırmadan sonra)**

```powershell
# Yedekler indi mi kontrol et:
Get-ChildItem D:\backups\personalautonomy\db -Name

# Log dosyasını incele:
Get-Content D:\backups\personalautonomy\pull-backup.log -Tail 20
```

VPS'te manuel test:
```bash
# Cron'u beklemeden script'i hemen çalıştır:
/opt/personalautonomy/scripts/backup.sh
ls -lah /opt/backups/db/
```

- [ ] **Step 10: Felaket kurtarma prosedürü (docs/README.md'ye ek)**

> **Not:** Geri yükleme işlemleri VPS üzerinde çalıştırılır, PC sadece yedek deposu olarak kullanılır. **PC'de Docker gerekmez.**

```markdown
## Felaket Kurtarma (Disaster Recovery)

### Veritabanı geri yükleme

1. Son yedeği bilgisayardan VPS'e kopyala (Windows PowerShell'den — scp built-in):
   ```powershell
   scp D:\backups\personalautonomy\db\YYYYMMDD.sql.gz root@VPS-IP:/tmp/
   ```

2. VPS'te SSH ile mevcut veritabanını sıfırla ve geri yükle:
   ```bash
   docker exec -i pa-postgres psql -U postgres -c "DROP DATABASE IF EXISTS personalautonomy;"
   docker exec -i pa-postgres psql -U postgres -c "CREATE DATABASE personalautonomy;"
   gunzip -c /tmp/YYYYMMDD.sql.gz | docker exec -i pa-postgres psql -U postgres personalautonomy
   ```

3. Drizzle migration'larını yeniden çalıştır (yapısal fark varsa):
   ```bash
   cd /opt/personalautonomy && bun drizzle-kit migrate
   ```

4. PM2'yi yeniden başlat:
   ```bash
   pm2 restart nitro-api
   ```

### Workspace'leri geri yükleme

1. Yedek workspace'leri bilgisayardan VPS'e kopyala (Windows PowerShell'den):
   ```powershell
   scp -r D:\backups\personalautonomy\workspaces\* root@VPS-IP:/opt/personalautonomy/workspaces/
   ```

2. VPS'te ownership'leri düzelt:
   ```bash
   for dir in /opt/personalautonomy/workspaces/ws-*; do
       user=$(basename "$dir")
       sudo chown -R "$user:$user" "$dir/data"
       sudo chown -R "$user:$user" "$dir/logs"
   done
   ```

### Geri yükleme sonrası test

1. Login sayfasına git ve admin ile giriş yapmayı dene
2. Admin panelden kullanıcı listesini kontrol et
3. Bir kullanıcı ile chat başlatıp mesaj geçmişini kontrol et
```

- [ ] **Step 11: Commit**

```bash
git add scripts/backup.sh scripts/pull-backup.ps1
git commit -m "feat: add daily backup strategy with local PC pull via rclone"
```

---

### Task 6.2.5: Health Check Endpoint

> **Motivation:** UptimeRobot Task 6.3'te `GET /api/health` URL'sini izleyecek. Bu endpoint olmadan monitoring çalışmaz. File Structure'da `health.get.ts` tanımlı ama hiçbir task oluşturmuyor.

**Files:**
- Create: `apps/web/src/server/api/health.get.ts`

- [ ] **Step 1: Write health check endpoint**

Create `apps/web/src/server/api/health.get.ts`:

```typescript
import { db } from "../db";
import { sql } from "drizzle-orm";

export default defineEventHandler(async () => {
  try {
    // Test DB connectivity
    await db.execute(sql`SELECT 1`);

    return {
      status: "ok",
      timestamp: new Date().toISOString(),
      uptime: process.uptime(),
    };
  } catch {
    throw createError({
      statusCode: 503,
      statusMessage: "Service unavailable",
    });
  }
});
```

- [ ] **Step 2: Commit**

```bash
git add apps/web/src/server/api/health.get.ts
git commit -m "feat: add health check endpoint for monitoring"
```

---

### Task 6.3: Monitoring & Alerting

> **Motivation:** Plana göre sitenin çöküp çökmediğini ancak bir kullanıcı şikayet edince öğrenebilirsin. Disk dolsa, backup alınamasa, PM2 çökse hiçbir yerden haberin olmaz. 3-10 kişilik sistem için Prometheus+Grafana overkill. Onun yerine: UptimeRobot (HTTP uptime) + healthchecks.io (cron monitoring) + 1 bash script (disk kontrolü). Toplam maliyet: 0 TL.

**Mimari:**
```
┌─────────────┐    her 5 dk'da GET    ┌──────────────┐
│ UptimeRobot │ ────────────────────→ │ VPS (Nginx)  │
│  (ücretsiz) │    timeout/500 alırsa │ :443/api/... │
│             │ ←─── Telegram'a alarm │              │
└─────────────┘                       └──────┬───────┘
                                             │
┌───────────────┐    cron bitince ping      │
│ healthchecks  │ ←─────────────────────────┘
│  .io (ücretsiz)│   backup.sh → curl diyecek
│               │   disk-check.sh → curl diyecek
└──────┬────────┘
       │ ping gelmezse
       ▼ Telegram'a alarm
```

**Files:**
- Create: `scripts/healthcheck.sh` (disk + DB + memory kontrolü)
- Modify: `scripts/backup.sh` (healthchecks.io ping eklenecek)

- [ ] **Step 1: Telegram bildirim kanalını hazırla**

Uyarıları nasıl almak istiyorsun? **Telegram (önerilir)** veya **e-posta**. İkisi de ücretsiz. Telegram anında ulaşır, e-posta gecikebilir.

**Telegram ile:**

**1a. BotFather'dan kendi bot'unu oluştur (1 kerelik):**

Telefonunda veya masaüstünde Telegram'ı aç. Arama çubuğuna `@BotFather` yaz, mavi tikli olanı seç. Şu adımları yap:

```
Sen: /start
BotFather: I can help you create and manage Telegram bots...

Sen: /newbot
BotFather: Alright, a new bot. How are we going to call it?
Sen: PersonalAutonomy Uyari
BotFather: Good. Now choose a username for your bot.
Sen: pa_uyari_bot
BotFather: Done! Use this token to access HTTP API:
          7495116295:AAHmqwerty1234567890abcdefghijklmno
          Keep your token secure!
```

**Bu token'ı bir yere kaydet.** Ama henüz hiçbir servise vermeyeceksin — sadece sohbet ID'ni almak için lazım.

**1b. Bot'la sohbet başlat:**

Telegram'da `@pa_uyari_bot` (veya verdiğin isim) diye arat, bul, tıkla, **"Başlat"** (Start) yaz. Bu zorunlu — bot sana mesaj atabilmesi için önce senin ona yazman gerek.

**1c. Sohbet ID'ni öğren:**

Telefonundaki Telegram'dan veya bilgisayardaki tarayıcıdan şu linke git (TOKEN yerine BotFather'ın verdiği token'ı yaz):

```
https://api.telegram.org/botTOKEN/getUpdates
```

Örnek:
```
https://api.telegram.org/bot7495116295:AAHmqwerty1234567890abcdefghijklmno/getUpdates
```

Tarayıcıda şuna benzer bir JSON göreceksin:

```json
{
  "ok": true,
  "result": [
    {
      "update_id": 123456789,
      "message": {
        "chat": {
          "id": 987654321,    ← BU SAYI SENİN TELEGRAM CHAT ID'N
          "first_name": "Burhan"
        }
      }
    }
  ]
}
```

`"id": 987654321` → bu senin sohbet ID'n. **Bu numarayı kaydet.** Aşağıdaki adımlarda hem UptimeRobot'ta hem healthchecks.io'da bu ID'yi kullanacaksın.

> **Sonuç çıkmazsa:** Telegram'da bot'una tekrar "merhaba" yaz, sayfayı yenile.

**E-posta ile (alternatif):**

Telegram istemiyorsan direkt e-posta ile de alarm alabilirsin. Her iki servis de e-posta destekler. Telegram'a göre tek farkı: e-postayı hemen görmeyebilirsin, gece acil durumda gecikir.

---

- [ ] **Step 2: UptimeRobot hesabı aç ve monitör tanımla**

1. Tarayıcıdan [uptimerobot.com](https://uptimerobot.com) adresine git
2. Sağ üstte **"Register"** veya **"Start Free"** butonuna tıkla
3. "Sign up with Google" ile Google hesabınla giriş yap (en kolayı)
4. Karşına dashboard gelecek. Sol menüden **"Monitors"** → sağ üstte mavi **"+ Add New Monitor"** butonuna tıkla
5. Açılan formu şöyle doldur:

```
Monitor Type:       HTTP(s)                    ← açılır menüden seç
Friendly Name:      PersonalAutonomy           ← istediğin isim
URL (or IP):        https://api.PERSONALAUTONOMY.COM/api/health  ← KENDİ domain adresin
Monitoring Interval: 5 minutes                 ← 5 dakika yeter
Monitor Timeout:    30 seconds                 ← 30 saniyede cevap vermezse down say
```

6. **Alert Contacts** bölümüne gel. Bu kısım kritik:

   **Telegram ile bildirim eklemek için:**
   - "Alert Contacts" altında **"Add Alert Contact"** yazısına tıkla
   - Açılan listeden **Telegram** seç
   - `Telegram Chat ID` kutusuna **Step 1c'de aldığın chat ID numarasını** yaz (örn: `987654321`)
   - `Telegram Bot Token` kutusuna **Step 1a'da BotFather'ın verdiği token'ı** yapıştır (örn: `7495116295:AAHmqwerty...`)
   - "Add Alert Contact" butonuna tıkla
   - "Test" butonuyla test et — Telegram'a "Test message from UptimeRobot" mesajı gelmeli

   **E-posta ile bildirim eklemek için:**
   - "Add Alert Contact" → **E-mail** seç
   - E-posta adresini yaz, kaydet

7. **"Advanced Settings"** bölümünü aç (en altta küçük yazıyla):

```
Enable keyword monitoring:  ☑ (tik at)
Keyword:                     "ok"            ← tırnak içinde ok yaz, küçük harfle
Case Sensitive:              No
```

Bu ne işe yarar: `/api/health` endpoint'i `{ "status": "ok" }` döner. Eğer site çökmüşse ve Nginx "502 Bad Gateway" dönerse sayfada `ok` kelimesi olmaz → UptimeRobot alarm verir.

8. En altta **"Create Monitor"** butonuna tıkla

9. Test etmek için monitörün yanındaki ▶ (play) butonuna tıkla, "Check Now" ile manuel test yap

---

- [ ] **Step 3: healthchecks.io hesabı aç ve cron job monitörleri tanımla**

1. Tarayıcıdan [healthchecks.io](https://healthchecks.io) adresine git
2. **"Sign Up"** butonuna tıkla, e-posta adresinle kaydol (Google hesabı seçeneği yok, klasik kayıt)
3. Gelen doğrulama e-postasındaki linke tıkla
4. Giriş yaptıktan sonra **"My Checks"** sayfasındasın. **"+ Add Check"** butonuna tıkla ve aşağıdaki 2 check'i oluştur:

---

**Check 1: DB Backup monitorü**

```
Name:            DB Backup
Tags:            backup
Schedule:        1 day                  ← günde 1 kez ping bekler
Grace Time:      2 hours                ← ping 2 saat gecikse bile alarm vermez (backup script'in biraz geç çalışabilir)
```

Oluşturduktan sonra sana özel bir URL verilecek. Şuna benzer:

```
https://hc-ping.com/a1b2c3d4-1111-2222-3333-4444e5f6a7b8
```

→ **Bu URL'yi not al.** `a1b2c3d4...` kısmı senin DB Backup UUID'n.

---

**Check 2: Disk Health monitorü**

```
Name:            Disk Health
Tags:            disk
Schedule:        1 hour                 ← her saat ping bekler
Grace Time:      15 minutes             ← 15 dk gecikme toleransı
```

Bunun da kendine özel bir URL'si olacak:

```
https://hc-ping.com/b2c3d4e5-2222-3333-4444-5555a6b7c8d9
```

→ **Bu URL'yi de not al.** `b2c3d4e5...` kısmı senin Disk Health UUID'n.

---

**Bildirim entegrasyonu:**

5. Sol menüden **"Integrations"** → **"Add Integration"**

   **Telegram ile:**
   - Listeden **Telegram** seç
   - `Bot Token`: Step 1a'daki BotFather token'ını yapıştır
   - `Chat ID`: Step 1c'deki sohbet ID'sini yapıştır
   - "Save Integration" butonuna tıkla
   - Test mesajı gelecek

   **E-posta ile:**
   - Listenin en üstünde **Email** zaten default olarak ekli (kaydolduğun e-posta adresin)
   - Ekstra bir şey yapmana gerek yok

---

**Özet — elinde olması gerekenler:**

| Servis | URL / ID |
|--------|----------|
| UptimeRobot | Monitor kurulu, Telegram bağlı |
| healthchecks.io DB Backup UUID | `https://hc-ping.com/a1b2c3d4-1111-2222-3333-4444e5f6a7b8` |
| healthchecks.io Disk Health UUID | `https://hc-ping.com/b2c3d4e5-2222-3333-4444-5555a6b7c8d9` |

- [ ] **Step 4: VPS sağlık kontrol scripti**

Create `scripts/healthcheck.sh`:

```bash
#!/bin/bash
# VPS sağlık kontrolü: disk doluluğu, PostgreSQL bağlantısı, RAM kullanımı.
# Cron: her saat başı çalışır. Sorun varsa stderr'e yazar, hata kodu döner.
# healthchecks.io URL'sini kendi UUID'n ile değiştir.

set -e

HC_DISK_URL="https://hc-ping.com/BURAYA-DISK-UUID-YAZ"
HOSTNAME=$(hostname)

# ---------- Disk doluluk kontrolü ----------
DISK_USE=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ "$DISK_USE" -gt 80 ]; then
    echo "UYARI: Disk doluluğu %${DISK_USE} (eşik: %80) — $HOSTNAME" >&2
    curl -fsS --retry 3 "$HC_DISK_URL/fail" -d "Disk %${DISK_USE} dolu"
    exit 1
fi

# ---------- PostgreSQL bağlantı kontrolü ----------
if ! docker exec pa-postgres pg_isready -U postgres -t 5 > /dev/null 2>&1; then
    echo "UYARI: PostgreSQL bağlantısı başarısız — $HOSTNAME" >&2
    curl -fsS --retry 3 "$HC_DISK_URL/fail" -d "PostgreSQL kapalı"
    exit 1
fi

# ---------- RAM kontrolü ----------
RAM_USE=$(free | awk '/Mem:/ {printf "%.0f", $3/$2 * 100}')
if [ "$RAM_USE" -gt 90 ]; then
    echo "UYARI: RAM kullanımı %${RAM_USE} (eşik: %90) — $HOSTNAME" >&2
    curl -fsS --retry 3 "$HC_DISK_URL/fail" -d "RAM %${RAM_USE} dolu"
    exit 1
fi

# Her şey normalse başarı sinyali gönder
curl -fsS --retry 3 "$HC_DISK_URL" > /dev/null 2>&1
echo "[$(date)] Sağlık kontrolü OK | Disk: %${DISK_USE} | RAM: %${RAM_USE} | DB: UP | $HOSTNAME"
```

```bash
chmod +x scripts/healthcheck.sh
```

> **Not:** `BURAYA-DISK-UUID-YAZ` yazan yere Step 2'de healthchecks.io'dan aldığın Disk Check UUID'sini yapıştır. `/fail` eki hata durumunda alarmı tetikler.

- [ ] **Step 5: Backup script'ine healthchecks ping ekle**

`scripts/backup.sh` dosyasının sonuna aşağıdaki satırı ekle (Step 11'deki commit'ten önce):

```bash
# Script'in EN BAŞINA (set -e'den sonra) ekle:
HC_BACKUP_URL="https://hc-ping.com/BURAYA-BACKUP-UUID-YAZ"

# Script'in EN SONUNA (exit 0'dan önce) ekle:
curl -fsS --retry 3 "$HC_BACKUP_URL" > /dev/null 2>&1
```

> `BURAYA-BACKUP-UUID-YAZ` yerine Step 2'deki DB Backup UUID'sini yapıştır.

Bu sayede backup başarısız olursa (script hata verirse) healthchecks.io ping almaz ve sana alarm gönderir.

- [ ] **Step 6: VPS cron job'ları**

```bash
# Her saat başı sağlık kontrolü
(crontab -l 2>/dev/null; echo "0 * * * * /opt/personalautonomy/scripts/healthcheck.sh >> /var/log/healthcheck.log 2>&1") | crontab -

# Mevcut cron'ları listele:
crontab -l
```

Beklenen çıktı:
```
0 0 * * * /opt/personalautonomy/scripts/backup.sh >> /opt/backups/db/backup.log 2>&1
0 * * * * /opt/personalautonomy/scripts/healthcheck.sh >> /var/log/healthcheck.log 2>&1
```

- [ ] **Step 7: Alarm senaryoları ve beklenen davranış**

| Olay | Seni nasıl uyarır | Ne yapmalısın |
|------|-------------------|---------------|
| Site down (Nginx/Nitro çöktü) | UptimeRobot → Telegram | VPS'e SSH, `pm2 restart nitro-api` |
| PostgreSQL çöktü | UptimeRobot → Telegram (health endpoint DB sorgusu yaparsa) | `docker restart pa-postgres` |
| Disk %80 üstü | healthchecks.io "fail" ping → Telegram | Eski backup'ları temizle, workspace log'larını kontrol et |
| Gece backup'ı alınamadı | healthchecks.io "missing ping" → Telegram (ertesi sabah) | VPS'e SSH, `backup.sh`'i manuel çalıştır, hatayı gör |
| RAM %90 üstü | healthchecks.io "fail" ping → Telegram | `pm2 restart nitro-api`, fazla OpenCode session varsa kapat |

- [ ] **Step 8: Commit**

```bash
git add scripts/healthcheck.sh scripts/backup.sh
git commit -m "feat: add monitoring with UptimeRobot, healthchecks.io, and server health script"
```

---

### Task 6.4: PWA (Installable Web App)

> **Motivation:** Kullanıcılar her gün tarayıcı açıp URL yazarak girmek zorunda kalmasın. Telefon ana ekranına veya masaüstüne tek tıkla uygulama gibi eklensin, kendi ikonu ve ismiyle dursun. Ayrıca UI shell (React bundle, CSS, font) cache'lenerek tekrar girişler anında açılsın. İnternet koparsa beyaz sayfa yerine "çevrimdışı" mesajı gösterilsin.

> **Kapsam dışı:** Push notification (şu an bildirim feature'ı yok), background sync, offline mesajlaşma (canlı AI sohbeti için zaten internet şart).

**Tech:** [`vite-plugin-pwa`](https://vite-pwa-org.netlify.app) — Vite + React ile PWA'yı sıfır konfigürasyona yakın halleder. Manifest, service worker, icon generation hepsini tek plugin'den yönetir.

**Files:**
- Modify: `apps/web/vite.config.ts` (veya projedeki vite config dosyası)
- Modify: `apps/web/index.html` (meta etiketleri)
- Create: `apps/web/public/icon-512.png` (uygulama simgesi)
- Create: `apps/web/public/offline.html` (internet kesilince gösterilecek sayfa)
- Modify: `apps/web/package.json` (vite-plugin-pwa bağımlılığı)

- [ ] **Step 1: vite-plugin-pwa'yı yükle**

```bash
cd apps/web && bun add -D vite-plugin-pwa
```

- [ ] **Step 2: vite.config.ts'ye PWA plugin'ini ekle**

> Projedeki vite config dosyasının adı ve yolu ne olursa olsun (genelde `apps/web/vite.config.ts`), aşağıdaki `VitePWA` bloğunu mevcut `plugins` dizisine ekle.

```typescript
import { VitePWA } from "vite-plugin-pwa";

// Mevcut plugins: [...] içine şunu ekle:
plugins: [
  // ... diğer plugin'ler ...
  VitePWA({
    registerType: "autoUpdate",
    includeAssets: ["favicon.ico", "icon-192.png", "icon-512.png"],
    manifest: {
      name: "PersonalAutonomy",
      short_name: "PAutonomy",
      description: "Kişisel AI asistan çalışma alanınız",
      theme_color: "#1e40af",       // koyu mavi (Tailwind blue-800)
      background_color: "#f9fafb",  // açık gri (Tailwind gray-50)
      display: "standalone",
      scope: "/",
      start_url: "/chat",
      orientation: "any",
      icons: [
        {
          src: "/icon-192.png",
          sizes: "192x192",
          type: "image/png",
        },
        {
          src: "/icon-512.png",
          sizes: "512x512",
          type: "image/png",
          purpose: "any maskable",
        },
      ],
    },
    workbox: {
      // UI shell'i cache'le (React bundle, CSS, font, ikonlar)
      globPatterns: ["**/*.{js,css,html,ico,png,svg,woff2}"],
      // API isteklerini cache'leme — canlı AI sohbeti için her zaman network
      runtimeCaching: [
        {
          urlPattern: /^https?:\/\/.*\/api\/.*/i,
          handler: "NetworkOnly",
          options: {
            backgroundSync: { name: "apiQueue" },
          },
        },
      ],
    },
  }),
]
```

> **`display: "standalone"` ne yapar?** Uygulama ana ekrana eklendiğinde tarayıcının adres çubuğu + gezinme butonları gizlenir. Tam ekran native uygulama gibi görünür.

- [ ] **Step 3: index.html'e PWA meta etiketlerini ekle**

Mevcut `apps/web/index.html` dosyasındaki `<head>` bölümüne şu satırları ekle:

```html
<!-- PWA -->
<meta name="theme-color" content="#1e40af" />
<meta name="apple-mobile-web-app-capable" content="yes" />
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
<meta name="apple-mobile-web-app-title" content="PAutonomy" />
<link rel="apple-touch-icon" href="/icon-192.png" />
```

> **`apple-mobile-web-app-capable` ne yapar?** iOS Safari'de "Ana Ekrana Ekle" yapıldığında standalone modda açılmasını sağlar. Bu satır olmazsa iOS'ta PWA tam ekran açılmaz.

- [ ] **Step 4: Uygulama ikonlarını oluştur**

512x512 px boyutunda bir PNG ikon oluştur ve `apps/web/public/` altına kaydet:

```bash
# Eğer bir ikon dosyan yoksa, basit bir SVG'den PNG üretebilirsin.
# Veya https://realfavicongenerator.net → tek PNG yükle, tüm boyutları indir.
```

Minimum 2 dosya:
```
apps/web/public/icon-192.png   (192x192 px)
apps/web/public/icon-512.png   (512x512 px)
```

> **İkon yoksa geçici çözüm:** Tek renkli bir kare + "PA" yazısı olan basit bir PNG. Sonra değiştirirsin. PWA testi için şimdilik herhangi bir 512x512 PNG iş görür.

- [ ] **Step 5: Offline fallback sayfası**

Create `apps/web/public/offline.html`:

```html
<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>PersonalAutonomy - Çevrimdışı</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      display: flex; align-items: center; justify-content: center;
      min-height: 100vh; background: #f9fafb; color: #374151;
    }
    .container { text-align: center; padding: 2rem; }
    .icon { font-size: 4rem; margin-bottom: 1rem; }
    h1 { font-size: 1.5rem; margin-bottom: 0.5rem; color: #111827; }
    p { color: #6b7280; margin-bottom: 1.5rem; }
    button {
      padding: 0.75rem 1.5rem; background: #1e40af; color: white;
      border: none; border-radius: 0.5rem; font-size: 1rem; cursor: pointer;
    }
    button:hover { background: #1e3a8a; }
  </style>
</head>
<body>
  <div class="container">
    <div class="icon">📡</div>
    <h1>İnternet bağlantısı yok</h1>
    <p>PersonalAutonomy'yi kullanmak için internet bağlantısı gerekiyor.</p>
    <p>Lütfen bağlantınızı kontrol edip tekrar deneyin.</p>
    <button onclick="location.reload()">Tekrar Dene</button>
  </div>
</body>
</html>
```

- [ ] **Step 6: Build testi**

```bash
cd apps/web && bun run build
```

Build çıktısında şu dosyaların oluştuğunu kontrol et:

```
apps/web/dist/
├── manifest.webmanifest      ← vite-plugin-pwa otomatik oluşturur
├── sw.js                     ← service worker (workbox)
├── icon-192.png
├── icon-512.png
└── offline.html
```

Hepsi varsa PWA entegrasyonu başarılı.

- [ ] **Step 7: Lighthouse ile PWA puanını kontrol et**

1. Uygulamayı production build + Nginx üzerinden HTTPS ile aç (PWA testi için HTTPS zorunlu)
2. Chrome DevTools → **Lighthouse** sekmesi → "Progressive Web App" kategorisini seç → "Analyze page load"
3. Hedef: **yeşil puan** (en az 3/4 PWA kriteri karşılanmalı)

Beklenen sonuçlar:
- Installable: ✅ (manifest.json + icon + HTTPS)
- PWA Optimized: ✅ (service worker + offline page)
- Hızlı yükleme: ✅ (UI shell cache'li)

- [ ] **Step 8: Kullanıcı deneyimi kontrol listesi**

| Platform | Beklenen davranış |
|----------|-------------------|
| Android Chrome | Adres çubuğunda "Uygulamayı yükle" bildirimi çıkar. Ana ekrana eklenince tam ekran açılır |
| iOS Safari | Paylaş butonu → "Ana Ekrana Ekle". Ana ekranda standalone modda açılır (adres çubuğu gizli) |
| Masaüstü Chrome | Adres çubuğu sağında "Yükle" (➕ bilgisayar) ikonu. Ayrı pencere olarak açılır |
| İnternet kesilince | `offline.html` sayfası gösterilir. "Tekrar Dene" butonu ile sayfa yenilenir |
| Tekrar ziyaret | UI shell cache'ten geldiği için < 1 saniyede açılır |

- [ ] **Step 9: Commit**

```bash
git add apps/web/vite.config.ts apps/web/index.html apps/web/public/icon-*.png apps/web/public/offline.html apps/web/package.json
git commit -m "feat: add PWA support with install prompt, offline page, and UI shell caching"
```

---

## Phase 7: Seed Data and Testing

### Task 7.1: Database Seed

**Files:**
- Create: `apps/web/src/server/db/seed.ts`

- [ ] **Step 1: Write seed script**

Create `apps/web/src/server/db/seed.ts`:

```typescript
import { db, schema } from "./index";
import { hashPassword } from "../utils/password";
import { createWorkspace } from "../services/workspace-manager";

async function seed() {
  // Insert roles
  const [adminRole] = await db
    .insert(schema.roles)
    .values({
      name: "admin",
      description: "Full system administrator",
      templatePath: "templates/roles/admin",
      isDefault: false,
    })
    .returning();

  const [marketingAgentRole] = await db
    .insert(schema.roles)
    .values({
      name: "marketing-agent",
      description: "Dijital pazarlama stratejisti",
      templatePath: "templates/roles/marketing-agent",
      isDefault: true,
    })
    .returning();

  // Insert permissions
  const adminPermissions = [
    "workspace:create",
    "workspace:delete",
    "user:manage",
    "admin:access",
    "session:manage",
    "logs:view",
  ];

  for (const perm of adminPermissions) {
    await db.insert(schema.rolePermissions).values({
      roleId: adminRole.id,
      permission: perm,
    });
  }

  // Create admin user
  const passwordHash = await hashPassword("admin123");
  const [adminUser] = await db
    .insert(schema.users)
    .values({
      username: "admin",
      displayName: "System Admin",
      passwordHash,
      roleId: adminRole.id,
    })
    .returning();

  // Create admin workspace (triggers manage-workspace.sh for Linux user + dirs)
  await createWorkspace({
    userId: adminUser.id,
    name: "Admin Workspace",
    slug: "admin",
    roleName: "admin",
  });

  console.log("Seed complete. Admin user created:");
  console.log("  Username: admin");
  console.log("  Password: admin123");
  console.log("  User ID:", adminUser.id);
}

seed()
  .then(() => process.exit(0))
  .catch((err) => {
    console.error(err);
    process.exit(1);
  });
```

- [ ] **Step 2: Add seed script to package.json**

```bash
# Add to root package.json scripts:
# "db:seed": "bun run apps/web/src/server/db/seed.ts"
```

- [ ] **Step 3: Commit**

```bash
git add apps/web/src/server/db/seed.ts
git commit -m "feat: add database seed script"
```

---

### Task 7.2: Role Templates

> **Template güncelleme stratejisi:** Template'ler workspace'lere `cp` ile değil `ln -s` (symlink) ile bağlanır (bkz. Task 3.1 `manage-workspace.sh`). Admin `templates/roles/` altındaki herhangi bir dosyayı güncellediğinde, değişiklikler **tüm mevcut workspace'lerde anında görünür** — yeni workspace açmaya gerek yoktur. Workspace delete edildiğinde symlink silinir, template'e dokunulmaz.

**Files:**
- Create: `templates/roles/marketing-agent/AGENTS.md`
- Create: `templates/roles/marketing-agent/mcps.json`

- [ ] **Step 1: Create marketing-agent template**

Create `templates/roles/marketing-agent/AGENTS.md`:

```markdown
# Dijital Pazarlama Stratejisti

Sen bir dijital pazarlama stratejistisin. Görevin kullanıcının pazarlama ihtiyaçlarını analiz etmek, strateji geliştirmek, içerik üretmek ve veriye dayalı pazarlama kararları almaktır.

## Uzmanlık Alanların

### Araştırma & Analiz
- Derinlemesine pazar araştırması ve trend analizi (deep-research)
- Rakip analizi, SWOT ve konumlandırma (competitive-teardown)
- Ürün metrikleri, KPI takibi ve cohort analizi (product-analytics)

### Strateji & Planlama
- Ürün stratejisi, OKR kaskadı ve vizyon oluşturma (product-strategist)
- Fırsat validasyonu, varsayım haritalama ve discovery sprintleri (product-discovery)
- RICE önceliklendirme, müşteri görüşme analizi ve GTM stratejileri (product-manager-toolkit)
- A/B test tasarımı, hipotez oluşturma ve deney önceliklendirme (experiment-designer)
- Yol haritası, release notes ve stakeholder iletişimi (roadmap-communicator)

### İçerik & Kreatif
- Landing page, hero bölümü, CTA ve pricing sayfası üretimi (landing-page-generator)
- Kullanıcı persona'ları, journey map ve kullanılabilirlik testi (ux-researcher-designer)
- Tasarım sistemi, token ve komponent dokümantasyonu (ui-design-system)
- Brief'leri yapılandırılmış prompt'lara dönüştürme (enhance-prompt)

### Teknik
- SaaS projesi boilerplate ve hızlı prototipleme (saas-scaffolder)

## Çalışma Prensibin
Kullanıcı sana bir pazarlama görevi verdiğinde:
1. Önce durumu ve hedef kitleyi analiz et
2. İlgili skill'leri kullanarak veriye dayalı öneriler sun
3. Uygulanabilir, ölçülebilir çıktılar üret (doküman, metin, plan, analiz, tasarım)
4. Tüm kararları, varsayımları ve süreçleri md formatında kaydet
5. Çıktının başarısını ölçmek için KPI önerileri sun

## Kurallar
- Her zaman Türkçe yanıt ver
- Her karar için veri/gerekçe göster
- Rakip analizlerinde objektif kal
- Önerilerini her zaman iş hedefleriyle ilişkilendir
- Kullanıcının mevcut kaynaklarını ve kısıtlarını dikkate al
```

- [ ] **Step 2: Create mcps.json file**

Create `templates/roles/marketing-agent/mcps.json`:

```json
{
  "version": "1.0",
  "mcps": []
}
```

- [ ] **Step 3: Create admin template**

Create `templates/roles/admin/AGENTS.md`:

```markdown
# Sistem Yöneticisi

Sen bir sistem yönetim asistanısın. Görevin platform yönetimi, kullanıcı desteği ve teknik sorunların çözümünde yardımcı olmaktır.

## Yeteneklerin
- Kullanıcı sorunlarını analiz et ve çözüm öner
- Sistem durumu ve performans analizi
- Yapılandırma dosyalarını inceleme ve öneriler
- Dokümantasyon oluşturma ve güncelleme

Önemli: Her zaman Türkçe yanıt ver.
```

Create `templates/roles/admin/mcps.json`:

```json
{
  "version": "1.0",
  "mcps": []
}
```

- [ ] **Step 4: Commit**

```bash
git add templates/
git commit -m "feat: add role templates for admin and marketing-agent"
```

---

## Self-Review

**1. Spec coverage check:**

| Spec Section | Covered By |
|---|---|
| Genel Mimari + İzolasyon | Phase 1-4: schema, workspace-manager, opencode-manager, session-manager |
| Resource Limits (ulimit via bash) | Task 4.1: bash -c ulimit -v -n -u |
| Port tracking + release | Task 4.1-4.2: usedPorts Set, releasePort on kill/stop |
| DB Migrations in CI/CD | Task 6.1: bun drizzle-kit migrate in deploy script |
| waitForReady (TCP socket) | Task 4.2: TCP connection check instead of /health HTTP |
| FK cascades | Task 1.2: onDelete cascade on key references |
| Process kill (-PGID) | Task 4.1: killOpenCode with process.kill(-pid) |
| Atomic port assignment | Task 4.1: findAndLockPort + global Set<number> with port tracking |
| Resource Limits (ulimit) | Task 4.1: bash -c with ulimit built-in (avoids sudo PID mismatch) |
| TOCTOU port race fix | Task 4.1: usedPorts Set + releasePort on session close |
| Handshake timeout | Task 4.2: waitForReady with 10s timeout |
| Template symlink strategy | Task 3.1: ln -sfn instead of cp; Task 7.2: note on live updates |
| Logging (stdout/stderr) | Task 4.1: pipe to agent.log |
| Veritabanı Modeli (all 10 tables) | Task 1.2: schema.ts |
| Soft delete (deleted_at) | Task 1.2: users.workspaces deletedAt columns |
| Auth (login/me, JWT, rate limit) | Task 2.1-2.3 |
| User Management CRUD | Task 3.3 |
| Workspace creation/deletion | Task 3.1-3.2 |
| Session Management | Task 4.2 |
| OpenCode integration (SDK-based) | Task 4.1-4.2: uses @opencode-ai/sdk, not raw HTTP |
| Frontend (login, chat, admin) | Phase 5: Tasks 5.1-5.4 |
| SSE with reconnect | Task 5.1: sse-client.ts |
| Markdown rendering | Portal existing (react-markdown) |
| Admin Panel (users, sessions, logs, files) | Task 5.4 |
| Role Management CRUD | Task 5.5 |
| Session Detail View | Task 5.6 |
| File Download/Delete | Task 5.7 |
| User Edit Form | Task 5.8 |
| Per-User Workspace File Editor | Task 5.9 |
| Deployment (Docker, Nginx, PM2, CI/CD) | Phase 6 |
| UFW Firewall | Task 6.1 Step 5: UFW firewall configuration |
| sudoers wrapper script | Task 3.1: manage-workspace.sh |
| CORS + OPTIONS preflight | Task 6.1: nginx/api.conf |
| Role Templates | Task 7.2 |
| PWA (manifest + service worker + offline) | Task 6.4 |
| Seed Data | Task 7.1 |
| Backup Strategy | Task 6.2: VPS cron pg_dump + PC rclone pull |
| Monitoring & Alerting | Task 6.3: UptimeRobot + healthchecks.io + healthcheck.sh |
| Health Check Endpoint | Task 6.2.5: /api/health for UptimeRobot |

**2. Placeholder scan:** The following values must be replaced by the user during setup:
- `BURAYA-DISK-UUID-YAZ` — healthcheck.sh (Task 6.3): healthchecks.io Disk Health UUID
- `BURAYA-BACKUP-UUID-YAZ` — backup.sh (Task 6.3): healthchecks.io DB Backup UUID
- `VPS-IP-ADRESIN` — backup setup (Task 6.2): user's VPS IP address
- `KOCAK` → user's Windows username — rclone config (Task 6.2)

**3. Type consistency:** All types reference the schema defined in Task 1.2. API routes use consistent field names matching schema columns. Service methods use consistent parameter names.

**4. Coverage:** All admin pages (users, roles, sessions, logs, files) have frontend routes and backend API endpoints with full CRUD operations. Role management includes create/edit/delete with audit logging. Session detail shows message history. File management supports download/delete. User edit modal provides workspace info and resource limits override. Chat SSE hook is scaffolded.

---

**Plan complete and saved to `docs/superpowers/plans/<filename>.md`. Two execution options:**

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?**

---

## Phase 7: Marketing Agent � Role Template

> **Durum:** Agent tan�m dosyalar� haz�r (marketing-agent/), VPS'te test ve deploy bekliyor.
> **Hedef:** `marketing-agent` rolü için kusursuz, otonom çalışan marketing agent oluşturmak.

### Task 7.1: Marketing Agent Skill Setini Tamamla

- [ ] **Marketing skill'lerini test et** � Her /market komutu i�in en az bir test senaryosu �al��t�r
  - /market funnel https://orneksite.com � Funnel analizi do�ru ��k�yor mu?
  - /market seo https://orneksite.com � SEO tespitleri isabetli mi?
  - /market emails "SaaS CRM �r�n�" � Email sequence mant�kl� m�?
  - /market social "yapay zeka" � 30 g�nl�k takvim d�zg�n m�?
  - /market ads https://orneksite.com � Reklam kreatifleri platform limitlerine uygun mu?
  - /market competitors https://orneksite.com � Rakip analizi yeterli derinlikte mi?
  - /market launch "AI Chatbot" � 8 haftal�k plan kapsaml� m�?
  - /market proposal "Tech Corp" � Teklif profesyonel duruyor mu?
  - /market report https://orneksite.com � 6 boyutlu skorlama tutarl� m�?
  - /market brand https://orneksite.com � Marka sesi analizi do�ru mu?

- [ ] **Python script'leri test et**
  - python scripts/analyze_page.py https://orneksite.com � JSON ��kt�s� do�ru mu?
  - python scripts/competitor_scanner.py https://rakip1.com https://rakip2.com � Do�ru parse ediyor mu?
  - python scripts/social_calendar.py --topic "AI" --platforms instagram,linkedin � Takvim �retiliyor mu?
  - python scripts/generate_pdf_report.py --input MARKETING-REPORT.md --output test.pdf � PDF olu�uyor mu?

- [ ] **Skill zincirlerini test et** (SKILLS.md Section D)
  - Yeni �r�n lansman� zinciri: market-launch � market-brand � market-emails � market-social � landing-page-generator
  - Rakip sald�r�s� zinciri: market-competitors � competitive-teardown � product-strategist

- [ ] **Eksik skill'leri tamamla** � Testlerde eksik/hatal� ��kan skill'leri d�zelt
- [ ] **Edge case'leri test et** � JS rendering gerektiren site, 404, timeout, b�y�k site

### Task 7.2: Puppeteer MCP Kurulumu (VPS)

- [ ] **Chromium ba��ml�l�klar�n� y�kle** (Ubuntu/Debian)
  `ash
  sudo apt update
  sudo apt install -y chromium-browser libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libpango-1.0-0 libcairo2 libasound2
  `

- [ ] **Puppeteer MCP'yi OpenCode'a register et**
  `ash
  npx -y @anthropic/mcp-puppeteer --version
  `

- [ ] **OpenCode MCP konfig�rasyonuna ekle** � mcps.json'daki tan�m� OpenCode'un kendi mcp.json/opencode.json dosyas�na entegre et

- [ ] **Test: Puppeteer ile site tara**
  `
  /market funnel https://example.com
  `
  Expected: Puppeteer MCP ile site render edilip analiz ediliyor.

- [ ] **RAM kullan�m�n� �l�** � htop ile Chromium headless RAM t�ketimini izle, 400MB alt�nda m�?
- [ ] **Fallback mekanizmas�n� test et** � Puppeteer MCP yan�t vermedi�inde WebFetch'e d���yor mu?

### Task 7.3: PDF Rapor Deste�i

- [ ] **Python reportlab kurulumu**
  `ash
  pip install reportlab
  `

- [ ] **Test: Markdown � PDF d�n���m�**
  `ash
  python scripts/generate_pdf_report.py --input MARKETING-REPORT.md --output test.pdf
  `
  Expected: 	est.pdf olu�ur, t�m sayfalar eksiksiz.

- [ ] **Fallback test et** � reportlab kurulu de�ilse hata mesaj� do�ru mu?

### Task 7.4: Template Dizini VPS'e Kopyala

- [ ] 	emplates/roles/marketing-agent/ dizini olu�tur
  `ash
  mkdir -p /opt/personalautonomy/templates/roles/marketing-agent/skills
  `

- [ ] **Dosyalar� kopyala:**
  `ash
  cp marketing-agent/AGENTS.md /opt/personalautonomy/templates/roles/marketing-agent/AGENTS.md
  cp -r marketing-agent/skills/* /opt/personalautonomy/templates/roles/marketing-agent/skills/
  cp marketing-agent/mcps.json /opt/personalautonomy/templates/roles/marketing-agent/mcps.json
  `

- [ ] **Script'leri deploy et:**
  `ash
  cp marketing-agent/scripts/*.py /opt/personalautonomy/scripts/
  chmod +x /opt/personalautonomy/scripts/*.py
  `

- [ ] **Template'leri deploy et:**
  `ash
  cp -r marketing-agent/templates/ /opt/personalautonomy/templates/marketing/
  `

- [ ] **Symlink testi** � manage-workspace.sh create ws-test-uuid marketing-agent ile workspace olu�tur, symlink'ler do�ru �al���yor mu?

### Task 7.5: Agent Prompt Kalibrasyonu

- [ ] **T�rk�e kalitesini kontrol et** � T�m SKILL.md'ler T�rk�e, terimler tutarl� m�?
- [ ] **Tutarl�l�k testi** � Ayn� URL i�in 2 farkl� zamanda /market report �al��t�r, skorlar tutarl� m�?
- [ ] **Derinlik testi** � Agent y�zeysel mi yoksa derinlemesine analiz mi yap�yor?
- [ ] **Output kalitesi** � ��kt�lar m��teriye direkt sunulabilir kalitede mi?
- [ ] **KPI �nerileri** � Agent her ��kt�da KPI �neriyor mu?

### Task 7.6: Otonomi ve Kendi Kendine �al��ma

- [ ] **Skill zincirlerini otonom yap** � Agent, kullan�c� s�ylemeden hangi skill'i kullanaca��n� do�ru tespit ediyor mu?
- [ ] **Hata yakalama** � Ge�ersiz URL, timeout, bo� sayfa durumlar�n� zarif�e handle ediyor mu?
- [ ] **Kendi ��kt�lar�n� okuyabilme** � /market report ��kt�s�ndan sonra /market report-pdf otomatik tetiklenebiliyor mu?
- [ ] **Session'lar aras� haf�za** � Ayn� kullan�c� tekrar geldi�inde �nceki analizleri hat�rl�yor mu? (Varsa context)

### Task 7.7: admin rol� i�in Agent Yap�land�rmas�

- [ ] **Admin i�in agent template olu�tur** � Varsa 	emplates/roles/admin/ dizini
- [ ] **Admin AGENTS.md yaz** � Kullan�c� y�netimi, workspace y�netimi, monitoring yetenekleri
- [ ] **Admin skill'leri tan�mla** � Kullan�c� olu�turma, session izleme, log inceleme

### Task 7.8: Final Do�rulama ve Dok�mantasyon

- [ ] **T�m skill'leri u�tan uca test et** � Her /market komutu i�in 1 ger�ek site
- [ ] **Performans testi** � 5 paralel subagent ile audit ne kadar s�r�yor?
- [ ] **Kaynak kullan�m�** � Agent + Puppeteer + OpenCode toplam RAM/CPU kullan�m�
- [ ] **Kullan�c� dok�mantasyonu yaz** � Hangi komut ne i�e yarar? (AGENTS.md zaten var, g�zden ge�ir)
- [ ] **Gelecek repolar i�in TODO** � GitHub'da buldu�un di�er marketing repolar�n� incele, entegre edilecekleri listele

---

**Bu phase VPS al�nd�ktan ve OpenCode kurulduktan sonra yap�lacak. �imdilik plan olarak kaydedildi.**

---

## Phase 7 G�ncellemesi: Marketing Agent v3 � coreyhaines31/marketingskills Entegrasyonu

**Tarih:** 2026-05-30
**Durum:** Skill tan�mlar� tamamland�. 36 skill marketing-agent/skills/ alt�nda haz�r.

### Entegre edilen 28 skill:
product-marketing, paywalls, copywriting, copy-editing, cold-email, emails, social, video, image, seo-audit, ai-seo, competitor-profiling, directory-submissions, content-strategy, aso, ads, ad-creative, analytics, referrals, churn-prevention, community-marketing, launch, pricing, prospecting, marketing-ideas, marketing-psychology, customer-research, marketing-plan

### Korunan 7 �zel skill:
market-funnel, market-ads, market-competitors, market-proposal, market-report, market-report-pdf, market-brand

### Kald�r�lan 4 eski skill (repo versiyonuyla de�i�tirildi):
market-emails � emails, market-social � social, market-seo � seo-audit, market-launch � launch

### Video/Image notu:
API entegrasyonu yok. Sadece strateji/script/prompt �retiyorlar. Proje geli�tirme a�amas�nda Midjourney/DALL-E/HeyGen API entegrasyonu yap�lacak.

### VPS'te yap�lacaklar (Phase 7.1-7.8):
Beklemede. VPS al�n�nca ve OpenCode kurulunca uygulanacak.

---

### Task 7.9: Social Post Agent � Konu�arak ��erik �retimi

> **Ama�:** Pazarlama Asistan? kullan?c?n?n OpenCode ile do?al sohbet halindeyken, ge?mi? payla??mlar? ve proje ba?lam?n? dikkate alarak g?nl?k sosyal medya g?nderisi haz?rlamas?. Kullan?c? teknik detaylarla u?ra?maz ? agent i?i yapar, kullan?c? sadece onaylar.

#### Neden n8n/Telegram/cron de�il?

Kullan�c� zaten OpenCode ile konu�uyor. Ayr� bir araca gitmesine, ayr� bir bot'a mesaj atmas�na gerek yok. Ak�� do�al sohbet i�inde ilerler. Otomasyon de�il, \"insan + AI i�birli�i\" modeli.

#### Mimari

`
Marketing Agent (Web Chat)
    -  "Bug�nk� Instagram g�nderisini haz�rlayal�m"
    �
OpenCode social-post agent
    -
    +�� ? product-marketing context'ini okur
    +�� ? post-history.md'den son 10 g�nderiyi okur
    +�� ? social skill'ten stratejiyi referans al�r
    +�� ? Kullan�c�ya 1-2 soru sorar:
    -      "Bug�n e�itim i�eri�i mi, �r�n tan�t�m� m�?"
    -      "�u anki odak noktam�z: X �zelli�inin lansman�. Buna uygun mu?"
    +�� ? copywriting skill ile caption + hashtag yazar
    +�� ? image skill ile g�rsel promptu �retir
    +�� ? Kullan�c�ya sorar: "Bu prompt ile g�rsel �retmemi onayl�yor musun?"
    +�� ? Onay � Minimax API �a�r�s� � g�rsel workspace'e kaydedilir
    +�� ? Kullan�c�ya sunar:
    -      -�������������������������������
    -      - ? G�nderin Haz�r!            -
    -      -                              -
    -      - ?? G�rsel: haz�r (indir)     -
    -      -                              -
    -      - ?? Caption:                   -
    -      - "Proje teslim tarihlerini     -
    -      -  ka��rmaktan s�k�ld�n m�?    -
    -      -  ..."                        -
    -      -                              -
    -      - #?? #proje #verimlilik        -
    -      -                              -
    -      - ?? Web aray�z�nden            -
    -      -    'Payla��mlar' sekmesinden  -
    -      -    g�rseli indirip            -
    -      -    kullanabilirsin.           -
    -      L������������������������������-
    +�� ? Onaylan�nca post-history.md'ye ekler
    L�� ? Kullan�c� web UI'dan g�rseli indirir, platformda payla��r
`

#### Bile�enler

| # | Bile�en | A��klama | Konum |
|---|---------|----------|-------|
| 1 | **social-post agent** | T�m ak��� y�neten �zel OpenCode agent'� | 	emplates/roles/marketing-agent/agents/social-post.md |
| 2 | **post-history.md** | Workspace'te ge�mi� g�nderilerin log'u. Tarih, platform, caption, hashtag, g�rsel path'i. Her yeni g�nderide buraya yaz�l�r. | Workspace k�k dizini |
| 3 | **Minimax image script** | Prompt al�r, Minimax API'sine POST atar, g�rseli workspace'e kaydeder. | scripts/minimax_generate_image.py |
| 4 | **Web UI \"Payla��mlar\" sekmesi** | Kullan�c�n�n �retilen t�m g�nderileri listeleyip g�rselleri indirebildi�i aray�z. | pps/web/src/routes/posts.tsx |
| 5 | **Disk temizleme cron** | 30 g�nden eski g�rselleri siler (disk dolmas�n). | VPS crontab:   3 * * * find ... -mtime +30 -delete |

#### social-post agent davran�� kurallar�

Agent **teknik olmayan** kullan�c�lar i�indir. �u kurallara uyar:

1. **Kullan�c�ya asla teknik detay sorma.** \"Minimax API endpoint'i ne olsun?\" gibi sorular YOK.
2. **Kullan�c�ya asla \"�u promptu kullanarak image �retebilirsin\" deme.** Onun yerine \"Bu prompt ile g�rsel �retmemi onayl�yor musun?\" de. ��i sen yap.
3. **Az sor, �ok i� yap.** Maksimum 1-2 soru sor. Gerisini sen hallet.
4. **Ge�mi�i bil.** post-history.md'den son g�nderileri oku, ayn� �eyi tekrarlama.
5. **Ba�lam� bil.** product-marketing context'inden �r�n�, social skill'ten stratejiyi oku.
6. **Sonucu net g�ster.** G�nderi haz�r oldu�unda caption, hashtag, g�rsel durumunu d�zenli g�ster.
7. **Web UI'a y�nlendir.** Kullan�c�ya \"Payla��mlar sekmesinden g�rseli indirebilirsin\" de. Dosya yolu verme.
8. **T�rk�e konu�.** T�m ileti�im T�rk�e.

#### post-history.md format�

`markdown
# Post History

## 2026-05-30 � Instagram
- **T�r:** E�itim
- **Caption:** Proje teslim tarihlerini ka��rmaktan s�k�ld�n m�? ��te 3 ad�mda...
- **Hashtag:** #proje #verimlilik #saas
- **G�rsel:** posts/2026-05-30-instagram.png
- **Durum:** ? Payla��ld�

## 2026-05-29 � Twitter
- **T�r:** Sosyal kan�t
- **Caption:** M��terimiz TechCorp, ProjectFlow ile haftada 5 saat kazand�...
- **Hashtag:** #ba�ar� #m��teri
- **G�rsel:** posts/2026-05-29-twitter.png
- **Durum:** ? Payla��ld�
`

#### Minimax Image Script (Python)

scripts/minimax_generate_image.py:

`python
"""
Minimax Image Generation Script
Kullan�m: python minimax_generate_image.py --prompt "..." --output posts/image.png
"""
import sys, json, argparse, requests, os
from pathlib import Path

MINIMAX_API_KEY = os.environ.get("MINIMAX_API_KEY")
MINIMAX_IMAGE_URL = "https://api.minimax.chat/v1/image/generation"  # kontrol edilecek

def generate(prompt: str, output_path: str):
    headers = {
        "Authorization": f"Bearer {MINIMAX_API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "image-01",
        "prompt": prompt,
        "n": 1,
        "size": "1080x1080"
    }
    resp = requests.post(MINIMAX_IMAGE_URL, json=body, headers=headers, timeout=60)
    data = resp.json()
    
    # G�rseli indir
    image_url = data["data"][0]["url"]
    img = requests.get(image_url)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_bytes(img.content)
    print(json.dumps({"status": "ok", "path": output_path}))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    generate(args.prompt, args.output)
`

#### Web UI \"Payla��mlar\" Sekmesi

pps/web/src/routes/posts.tsx:

- Kullan�c�n�n t�m g�nderilerini listeleyen tablo
- Her g�nderi: tarih, platform, t�r, caption �nizlemesi
- G�rsel thumbnail + indirme butonu
- \"Payla��ld�\" tik i�areti (checkbox)
- Filtre: platforma g�re, tarihe g�re
- Basit, temiz tasar�m

#### Disk Temizleme

`ash
# Her gece 03:00'te 30 g�nden eski g�rselleri sil
0 3 * * * find /opt/personalautonomy/workspaces/*/posts/ -type f -mtime +30 -delete
`

Veya bu i�lem workspace-manager servisine hook olarak eklenebilir.

> **NOT:** G�rsel �retimi i�in hangi API'nin kullan�laca�� (Minimax, DALL-E, Stable Diffusion, Midjourney vb.) implementasyon a�amas�nda kararla�t�r�lacakt�r. Se�im kriterleri: API maliyeti, g�rsel kalitesi, prompt uyumlulu�u, rate limit, SDK/API kolayl���. Yukar�daki kod �rnekleri referans ama�l�d�r, se�ilen API'ye g�re g�ncellenecektir.
