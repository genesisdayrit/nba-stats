// src/lib/db.ts 
import sqlite3 from 'sqlite3';
import { open, Database } from 'sqlite';

// Define a type for the database connection
type SQLiteDatabase = Database<sqlite3.Database, sqlite3.Statement>;

let db: SQLiteDatabase | undefined;

export async function connectToDatabase(): Promise<SQLiteDatabase> {
  // Open the database and return the connection
  db = await open({
    filename: 'src/lib/nba-data.db',
    driver: sqlite3.Database,
  });

  return db;
}

export async function getDb(): Promise<SQLiteDatabase> {
  if (!db) {
    db = await connectToDatabase();
  }
  return db;
}


