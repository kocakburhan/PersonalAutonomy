# PersonalAutonomy - Tasarım Dokümanı

**Tarih:** 2026-05-27
**Durum:** Onaylandı
**Proje Tipi:** Multi-tenant AI Agent Platform

---

## Özet

PersonalAutonomy, teknik olmayan kullanıcıların kişiselleştirilmiş AI agent sistemleriyle OpenCode üzerinden etkileşime girmesini sağlayan bir web platformudur. VPS'te çalışan OpenCode'a web arayüzü üzerinden erişim sunar. Her kullanıcı kendi rolüne özel agent, skill, MCP konfigürasyonuyla çalışır.

---

## Bölüm 1: Genel Mimari

```
┌─────────────────────────────────────────────────────────────┐
│                      KULLANICI                               │
│              (Telefon / Tablet / PC)                         │
└─────────────────────┬───────────────────────────────────────┘
                      │ HTTPS
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    VERCEL (Frontend)                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  PersonalAutonomy Web App (Portal fork + extensions)  │   │
│  │  ├─ /login          → Giriş sayfası                    │   │
│  │  ├─ /chat/:session  → OpenCode sohbet arayüzü          │   │
│  │  └─ /admin          → Admin panel                      │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────┬───────────────────────────────────────┘
                      │ API calls (Nitro fetch + JWT)
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    VPS (Ubuntu 24.04 LTS)                    │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Docker (sadece PostgreSQL)                         │    │
│  │  ┌──────────────────────────────┐                   │    │
│  │  │ PostgreSQL 16    :5432       │                   │    │
│  │  │ Volume: /data/postgres       │                   │    │
│  │  └──────────────────────────────┘                   │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Host Servisleri (PM2)                              │    │
│  │                                                     │    │
│  │  ┌──────────┐     ┌──────────────────┐              │    │
│  │  │  Nginx   │────►│  Nitro API       │              │    │
│  │  │  :443    │     │  :3000           │              │    │
│  │  │  (SSL)   │     │  user:nitro-run  │              │    │
│  │  └──────────┘     └────────┬─────────┘              │    │
│  │                            │                        │    │
│  │              ┌─────────────┴───────────┐            │    │
│  │              ▼                         ▼            │    │
│  │  /workspaces/user-1/        /workspaces/user-2/     │    │
│  │  OpenCode PID 1001          OpenCode PID 1002       │    │
│  │  user: ws-abc123            user: ws-def456         │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### Veri Akışı (Sohbet Mesajı)

1. Kullanıcı `/chat` sayfasında mesaj yazar
2. Frontend, Nitro API'ye mesajı gönderir (JWT token ile)
3. Nitro, isteği doğrular, kullanıcının workspace'ini bulur
4. Nitro, o workspace'teki OpenCode server'a SDK üzerinden isteği iletir
5. OpenCode, kullanıcının AGENTS.md/agent/skill bağlamında cevap üretir
6. Cevap SSE stream olarak frontend'e döner

---

## Bölüm 2: İzolasyon Mimarisi

### Katman 1: Süreç + Dosya Sistemi

```
Her kullanıcı için:
├── Ayrı Linux kullanıcısı (ws-{uuid})
│   ├── no sudo
│   ├── no shell login (/sbin/nologin)
│   └── sadece kendi grubu
├── Ayrı workspace dizini /workspaces/{user-id}/
│   ├── chmod 700 (sadece sahibi okuyabilir)
│   └── chown ws-{uuid}:ws-{uuid}
└── OpenCode süreci → ws-{uuid} olarak spawn edilir
```

### Katman 2: Resource Limits

| Limit | Değer | Amaç |
|---|---|---|
| `RLIMIT_AS` (max RAM) | 4 GB | Memory bomb önleme |
| `RLIMIT_CPU` (max CPU sn) | 600s (10 dk) | Infinite loop kesme |
| `RLIMIT_NPROC` (max process) | 30 | Fork bomb önleme |
| `RLIMIT_NOFILE` (max open file) | 256 | File descriptor abuse |
| `RLIMIT_FSIZE` (max file size) | 500 MB | Disk abuse önleme |
| Execution timeout | 15 dk | Yanıt gelmezse kill |

### Katman 3: Kural (Asla Root)

```
ASLA:
  ✗ OpenCode root olarak çalışmaz
  ✗ Nitro API root olarak çalışmaz (nitro-runner kullanıcısı)
  ✗ workspace kullanıcılarının sudo yetkisi yok

HER ZAMAN:
  ✓ Nitro API → nitro-runner kullanıcısı
  ✓ OpenCode → ws-{uuid} kullanıcısı
  ✓ Sudo sadece manage-workspace.sh wrapper script üzerinden
```

### Sudoers Konfigürasyonu

`/etc/sudoers.d/nitro-runner`:
```
nitro-runner ALL=(root) NOPASSWD: /opt/personalautonomy/scripts/manage-workspace.sh
```

`manage-workspace.sh` sadece `ws-*` prefix'li kullanıcılarla, sadece `/workspaces` altındaki işlemlere izin verir.

### Süreç Yönetimi

- Port atama: `net.createServer().listen(0)` ile atomik boş port
- Süreç kill: `process.kill(-PGID, 'SIGTERM')` ile tüm süreç ağacı
- Handshake timeout: SDK bağlantısı için 10 saniye timeout
- Zombi temizliği: 30 dk idle session → kill
- Loglama: her süreç `stdout/stderr` → `/workspaces/{userId}/logs/agent.log`

### Dosya İzin Modeli

```
/workspaces/{user-id}/
├── AGENTS.md        → root:root, chmod 444 (read-only)
├── skills/          → root:root, chmod 555 (read-only)
├── agents/          → root:root, chmod 555 (read-only)
├── mcps.json        → root:root, chmod 444 (read-only)
├── data/            → ws-xxx:ws-xxx, chmod 700 (yazılabilir)
└── logs/            → ws-xxx:ws-xxx, chmod 700 (yazılabilir)
```

---

## Bölüm 3: Veritabanı ve Veri Modeli

PostgreSQL 16 + Drizzle ORM

### Tablolar

**users**
| Kolon | Tip | Açıklama |
|---|---|---|
| id | UUID PK | |
| username | VARCHAR(50) UNIQUE | Login için |
| email | VARCHAR(255) UNIQUE NULLABLE | Login için alternatif (opsiyonel) |
| password_hash | VARCHAR(255) | bcrypt |
| display_name | VARCHAR(100) | |
| is_active | BOOLEAN | Admin deaktive edebilir |
| role_id | FK → roles | |
| resource_limits_override | JSONB | null ise default |
| created_at | TIMESTAMP | |
| updated_at | TIMESTAMP | |
| deleted_at | TIMESTAMP NULLABLE | Soft delete |

**roles**
| Kolon | Tip | Açıklama |
|---|---|---|
| id | SERIAL PK | |
| name | VARCHAR(50) | historian, marketer, admin |
| description | TEXT | |
| template_path | VARCHAR(255) | templates/roles/{name}/ |
| is_default | BOOLEAN | |

**role_permissions**
| Kolon | Tip | Açıklama |
|---|---|---|
| id | UUID PK | |
| role_id | FK → roles | |
| permission | VARCHAR(100) | workspace:create, user:manage, admin:access |

**workspaces**
| Kolon | Tip | Açıklama |
|---|---|---|
| id | UUID PK | |
| user_id | FK → users | |
| name | VARCHAR(100) | |
| slug | VARCHAR(100) | |
| linux_user | VARCHAR(50) | ws-a1b2c3d4 |
| workspace_path | VARCHAR(500) | /workspaces/{user-id} |
| is_active | BOOLEAN | |
| created_at | TIMESTAMP | |
| updated_at | TIMESTAMP | |
| deleted_at | TIMESTAMP NULLABLE | Soft delete |

**workspace_config**
| Kolon | Tip | Açıklama |
|---|---|---|
| id | UUID PK | |
| workspace_id | FK → workspaces | |
| agents_json | JSONB | Agent tanımları |
| skills_json | JSONB | Skill listesi |
| mcps_json | JSONB | MCP sunucu yapılandırması |
| agents_md_text | TEXT | AGENTS.md içeriği |
| resource_limits | JSONB | Per-workspace limit override |

**opencode_sessions**
| Kolon | Tip | Açıklama |
|---|---|---|
| id | UUID PK | |
| workspace_id | FK → workspaces | |
| user_id | FK → users | |
| opencode_sid | VARCHAR(100) | OpenCode session ID |
| status | VARCHAR(20) | active, idle, closed |
| model | VARCHAR(50) | |
| created_at | TIMESTAMP | |
| last_active | TIMESTAMP | |

**chat_messages**
| Kolon | Tip | Açıklama |
|---|---|---|
| id | UUID PK | |
| session_id | FK → opencode_sessions | |
| role | VARCHAR(10) | user, assistant |
| content | TEXT | |
| created_at | TIMESTAMP | |

**sessions** (auth)
| Kolon | Tip | Açıklama |
|---|---|---|
| id | UUID PK | |
| user_id | FK → users | |
| token | VARCHAR(500) | JWT |
| expires_at | TIMESTAMP | |
| created_at | TIMESTAMP | |

**user_files**
| Kolon | Tip | Açıklama |
|---|---|---|
| id | UUID PK | |
| user_id | FK → users | |
| workspace_id | FK → workspaces | |
| filename | VARCHAR(255) | |
| file_path | VARCHAR(500) | |
| file_size | BIGINT | |
| mime_type | VARCHAR(100) | |
| created_at | TIMESTAMP | |
| updated_at | TIMESTAMP | |

**audit_logs**
| Kolon | Tip | Açıklama |
|---|---|---|
| id | UUID PK | |
| user_id | FK → users (nullable) | |
| action | VARCHAR(100) | |
| entity_type | VARCHAR(50) | |
| entity_id | UUID | |
| old_value | JSONB | |
| new_value | JSONB | |
| ip_address | VARCHAR(45) | |
| created_at | TIMESTAMP | |

---

## Bölüm 4: Auth ve Session Yönetimi

### Kimlik Doğrulama

- Login: `username` veya `email` + şifre
- Şifre: bcrypt hash (cost factor 12)
- JWT access token, 24 saat ömür
- Rate limiting: 15 başarısız deneme → 15 dk blok (username bazlı)
- Admin endpoint'leri: `role: admin` middleware kontrolü

### Session Yönetimi

- Bir kullanıcı birden fazla session'a sahip olabilir
- Admin panelden tüm session'lar görüntülenebilir ve force-kill yapılabilir
- Token expire → login sayfasına yönlendirme

---

## Bölüm 5: Workspace ve OpenCode Entegrasyonu

### Workspace Yaşam Döngüsü

1. Admin kullanıcı oluşturur → DB'ye kayıt
2. `manage-workspace.sh create ws-{uuid}` ile Linux kullanıcısı + dizin
3. Rol template'i workspace'e kopyalanır
4. Çekirdek dosyalar root:root, chmod 444/555
5. Kullanıcıya giriş bilgisi iletilir

### Role Template Sistemi

```
templates/roles/historian/
├── AGENTS.md
├── skills/  (llm-wiki, vb.)
├── agents/
└── mcps.json

templates/roles/marketer/
├── AGENTS.md
├── skills/  (deep-research, competitive-teardown, landing-page-generator, product-manager-toolkit, product-strategist, product-discovery, product-analytics, roadmap-communicator, experiment-designer, ux-researcher-designer, ui-design-system, enhance-prompt, saas-scaffolder, vb.)
├── agents/
└── mcps.json
```

### OpenCode Süreç Yönetimi

- **Start:** `POST /api/sessions/start` → spawn OpenCode (resource limits + linux user), SDK connect, DB kayıt
- **Message:** `POST /api/sessions/:id/message` → SDK üzerinden mesaj, SSE stream
- **Stop:** `DELETE /api/sessions/:id` → `kill(-PGID, 'SIGTERM')`, DB status update
- **Handshake timeout:** 10 saniye → süreç kill + hata dön

### Housekeeping

- Cron: 30 dk idle session → kill
- Logout → session kapat
- VPS restart → tüm workspace süreçleri temizlenir

---

## Bölüm 6: Frontend ve Kullanıcı Deneyimi

### Sayfalar

| Rota | Açıklama |
|---|---|
| `/login` | Giriş ekranı |
| `/chat` | Ana sohbet arayüzü (portal + auth + session sidebar) |
| `/admin` | Admin dashboard |
| `/admin/users` | Kullanıcı yönetimi |
| `/admin/roles` | Rol tanımları, template yönetimi |
| `/admin/sessions` | Aktif oturumlar |
| `/admin/logs` | Kullanıcı log'ları, audit trail |
| `/admin/files` | Kullanıcı dosyaları |

### Chat Arayüzü

- Portal'ın mevcut chat UI'si korunur
- Eklenenler: header (kullanıcı adı + rol rozeti + logout), session sidebar, file upload
- Markdown render: react-markdown + remark-gfm (portal'da mevcut)
- Reconnect: `fetch` + `ReadableStream` + expo-backoff (1s → 2s → 4s, max 30s)
- 30 saniyeden uzun kopma → "Oturum zaman aşımına uğradı"

### Admin Panel

- Tam yetkili kullanıcı/dosya/session/workspace yönetimi
- Agent log'larını canlı okuma
- Audit trail görüntüleme
- Responsive (mobile-first)

---

## Bölüm 7: Deployment Mimarisi

### VPS Dizin Yapısı

```
/opt/personalautonomy/
├── docker-compose.yml       → sadece PostgreSQL
├── nitro/                   → Nitro API
├── scripts/
│   └── manage-workspace.sh  → sudoers wrapper
├── templates/roles/         → Rol şablonları
├── workspaces/              → Kullanıcı workspace'leri
├── data/postgres/           → PG volume
├── logs/                    → PM2 log'ları
└── nginx/sites-enabled/
    └── api.conf
```

### Güvenlik Duvarı (UFW)

```
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP → HTTPS redirect
ufw allow 443/tcp   # HTTPS (Nginx)
ufw enable
```

Dinamik portlar sadece localhost'ta açıktır, dış dünyaya kapalıdır. OpenCode süreçleri sadece Nitro üzerinden erişilebilir.

### Nginx Konfigürasyonu

- SSL termination (Let's Encrypt)
- CORS: sadece `https://personalautonomy.vercel.app`
- OPTIONS preflight: 204 No Content
- `/api/*` → `proxy_pass http://localhost:3000`

### CI/CD

```
GitHub Actions (main push):
  1. SSH → VPS
  2. cd /opt/personalautonomy && git pull
  3. pnpm install --dir nitro
  4. pm2 restart nitro-api
  5. Vercel auto-deploy (frontend)
```

### Secrets

- `.env` GitHub'a push'lanmaz (`.gitignore`)
- VPS'te manuel: `/opt/personalautonomy/nitro/.env`
- DB şifresi, JWT secret, API key'leri burada

---

## Teknoloji Stack Özeti

| Katman | Teknoloji |
|---|---|
| Frontend | React 19, React Router, IntentUI, Tailwind CSS, @opencode-ai/sdk |
| Backend API | Nitro (Bun), Drizzle ORM |
| Veritabanı | PostgreSQL 16 (Docker) |
| AI Engine | OpenCode CLI (host üzerinde PM2 ile yönetilen) |
| Reverse Proxy | Nginx (host) |
| Process Manager | PM2 (host) |
| Frontend Hosting | Vercel |
| Backend Hosting | VPS (Ubuntu 24.04) |
| CI/CD | GitHub Actions |
| İzolasyon | Linux users, chmod, resource limits, wrapper script |
