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
