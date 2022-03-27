import { config } from 'dotenv';
// config({ path: `.env.${process.env.NODE_ENV || 'development'}.local` });
config({ path: `.env` });
export const CREDENTIALS = process.env.CREDENTIALS === 'true';
export const { NODE_ENV, PORT, SECRET_KEY, LOG_FORMAT, LOG_DIR, ORIGIN, AUTH_ADDR, AUTH_PORT, AUTHMODE, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB } =
  process.env;
