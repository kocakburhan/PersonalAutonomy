import { defineConfig } from "drizzle-kit";

export default defineConfig({
  schema: "./apps/web/src/server/db/schema.ts",
  out: "./apps/web/src/server/db/migrations",
  dialect: "postgresql",
  dbCredentials: {
    url: process.env.DATABASE_URL!,
  },
});
