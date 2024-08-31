// src/routes/api/+server.ts
import type { RequestHandler } from '@sveltejs/kit';

export const GET: RequestHandler = async () => {
  return new Response(
    JSON.stringify({ message: 'API route is working!' }),
    {
      status: 200,
      headers: { 'Content-Type': 'application/json' }
    }
  );
};

