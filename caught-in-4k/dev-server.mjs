// Local dev server. Serves the single static file and routes /api/* into the
// exact same handler that runs on Netlify, backed by a folder on disk.
import http from 'node:http';
import { promises as fs } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { handle } from './lib/handler.mjs';
import { createDiskStore } from './lib/store-disk.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));

export async function startServer(options = {}) {
  const dataDir = options.dataDir || path.join(here, '.data');
  const store = createDiskStore(dataDir);
  const publicDir = path.join(here, 'public');

  const server = http.createServer(async (req, res) => {
    try {
      const url = new URL(req.url, 'http://localhost');
      if (url.pathname.startsWith('/api')) {
        let raw = '';
        for await (const chunk of req) raw += chunk;
        let body = null;
        if (raw) { try { body = JSON.parse(raw); } catch { body = null; } }
        const result = await handle({
          method: req.method,
          path: url.pathname,
          query: Object.fromEntries(url.searchParams),
          body,
          headers: req.headers
        }, store);
        res.writeHead(result.status, result.headers);
        res.end(result.body);
        return;
      }
      const file = url.pathname === '/' || url.pathname === '/host' ? '/index.html' : url.pathname;
      const full = path.join(publicDir, path.normalize(file).replace(/^(\.\.[/\\])+/, ''));
      const data = await fs.readFile(full);
      const type = full.endsWith('.html') ? 'text/html; charset=utf-8' : 'application/octet-stream';
      res.writeHead(200, { 'content-type': type, 'cache-control': 'no-store' });
      res.end(data);
    } catch (err) {
      res.writeHead(err.code === 'ENOENT' ? 404 : 500, { 'content-type': 'text/plain' });
      res.end(err.code === 'ENOENT' ? 'Not found' : 'Server error');
    }
  });

  await new Promise((resolve) => server.listen(options.port || 0, resolve));
  const port = server.address().port;
  return {
    port,
    url: 'http://127.0.0.1:' + port,
    dataDir,
    store,
    close: () => new Promise((resolve) => server.close(resolve))
  };
}

if (process.argv[1] && process.argv[1].endsWith('dev-server.mjs')) {
  const started = await startServer({ port: Number(process.env.PORT || 8888) });
  console.log('Caught in 4K is running at ' + started.url);
  console.log('Host screen: ' + started.url + '/host');
}
