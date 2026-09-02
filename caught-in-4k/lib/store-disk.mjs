// Disk backed storage, used by the local dev server and the tests.
// Same four method surface as the Netlify Blobs store.
import { promises as fs } from 'node:fs';
import path from 'node:path';

function fileFor(dir, key) {
  return path.join(dir, encodeURIComponent(key));
}

export function createDiskStore(dir) {
  const ready = fs.mkdir(dir, { recursive: true });
  return {
    async get(key) {
      await ready;
      try {
        return await fs.readFile(fileFor(dir, key), 'utf8');
      } catch (err) {
        if (err.code === 'ENOENT') return null;
        throw err;
      }
    },
    async set(key, value) {
      await ready;
      const target = fileFor(dir, key);
      const tmp = target + '.' + Math.random().toString(36).slice(2) + '.tmp';
      await fs.writeFile(tmp, value);
      await fs.rename(tmp, target);
    },
    async delete(key) {
      await ready;
      try {
        await fs.unlink(fileFor(dir, key));
      } catch (err) {
        if (err.code !== 'ENOENT') throw err;
      }
    },
    async list(prefix) {
      await ready;
      const names = await fs.readdir(dir);
      return names
        .filter((n) => !n.endsWith('.tmp'))
        .map((n) => decodeURIComponent(n))
        .filter((k) => k.startsWith(prefix))
        .sort();
    }
  };
}
