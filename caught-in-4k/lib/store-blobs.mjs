// Netlify Blobs storage. Same four method surface as the disk store.
export async function createBlobStore(name) {
  const { getStore } = await import('@netlify/blobs');
  const store = getStore({ name, consistency: 'strong' });
  return {
    async get(key) {
      return await store.get(key, { type: 'text' });
    },
    async set(key, value) {
      await store.set(key, value);
    },
    async delete(key) {
      await store.delete(key);
    },
    async list(prefix) {
      const res = await store.list({ prefix });
      return (res.blobs || []).map((b) => b.key).sort();
    }
  };
}
