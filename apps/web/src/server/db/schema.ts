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
  opencodeSessions: many(opencodeSessions),
  userFiles: many(userFiles),
  auditLogs: many(auditLogs),
}));

export const workspacesRelations = relations(workspaces, ({ one, many }) => ({
  user: one(users, { fields: [workspaces.userId], references: [users.id] }),
  config: one(workspaceConfigs),
  opencodeSessions: many(opencodeSessions),
  userFiles: many(userFiles),
}));

export const workspaceConfigsRelations = relations(workspaceConfigs, ({ one }) => ({
  workspace: one(workspaces, {
    fields: [workspaceConfigs.workspaceId],
    references: [workspaces.id],
  }),
}));

export const opencodeSessionsRelations = relations(opencodeSessions, ({ one, many }) => ({
  workspace: one(workspaces, {
    fields: [opencodeSessions.workspaceId],
    references: [workspaces.id],
  }),
  user: one(users, { fields: [opencodeSessions.userId], references: [users.id] }),
  messages: many(chatMessages),
}));

export const chatMessagesRelations = relations(chatMessages, ({ one }) => ({
  session: one(opencodeSessions, {
    fields: [chatMessages.sessionId],
    references: [opencodeSessions.id],
  }),
}));

export const userFilesRelations = relations(userFiles, ({ one }) => ({
  user: one(users, { fields: [userFiles.userId], references: [users.id] }),
  workspace: one(workspaces, { fields: [userFiles.workspaceId], references: [workspaces.id] }),
}));

export const auditLogsRelations = relations(auditLogs, ({ one }) => ({
  user: one(users, { fields: [auditLogs.userId], references: [users.id] }),
}));
