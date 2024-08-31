// src/routes/test/+server.ts
import type { RequestHandler } from '@sveltejs/kit';
import { getDb } from '$lib/db';

export const GET: RequestHandler = async () => {
  try {
    const db = await getDb();
    
    // Run the desired query
    const result = await db.all('SELECT * FROM player_game_stats LIMIT 10');

    return new Response(JSON.stringify({
      success: true,
      data: result
    }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' }
    });
  } catch (error) {
    console.error('Error executing the query:', error);
    return new Response(JSON.stringify({
      success: false,
      error: 'Failed to execute query',
      details: error instanceof Error ? error.message : 'Unknown error'
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
};


