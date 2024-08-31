// src/routes/sql-editor/run-query/+server.ts
import type { RequestHandler } from '@sveltejs/kit';
import { getDb } from '$lib/db';

export const POST: RequestHandler = async ({ request }) => {
  try {
    const { query } = await request.json();
    const db = await getDb();

    // Execute the SQL query
    const result = await db.all(query);

    return new Response(
      JSON.stringify({ success: true, data: result }),
      {
        status: 200,
        headers: { 'Content-Type': 'application/json' },
      }
    );
  } catch (error) {
    console.error('Error executing the query:', error);
    return new Response(
      JSON.stringify({
        success: false,
        error: 'Failed to execute query',
        details: error instanceof Error ? error.message : 'Unknown error',
      }),
      {
        status: 500,
        headers: { 'Content-Type': 'application/json' },
      }
    );
  }
};

