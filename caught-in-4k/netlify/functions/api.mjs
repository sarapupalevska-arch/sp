// Netlify Function entry point. All of the rules live in lib/handler.mjs.
import { handle } from '../../lib/handler.mjs';
import { createBlobStore } from '../../lib/store-blobs.mjs';

let storePromise = null;

export default async function api(request) {
  if (!storePromise) storePromise = createBlobStore('caught-in-4k');
  const store = await storePromise;
  const url = new URL(request.url);
  let body = null;
  if (request.method !== 'GET' && request.method !== 'HEAD') {
    const raw = await request.text();
    if (raw) { try { body = JSON.parse(raw); } catch { body = null; } }
  }
  const headers = {};
  request.headers.forEach((value, key) => { headers[key.toLowerCase()] = value; });
  const result = await handle({
    method: request.method,
    path: url.pathname.replace(/^\/\.netlify\/functions\/api/, '/api'),
    query: Object.fromEntries(url.searchParams),
    body,
    headers
  }, store);
  return new Response(result.body, { status: result.status, headers: result.headers });
}

export const config = { path: '/api/*' };
