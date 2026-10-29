import test from "node:test";
import assert from "node:assert/strict";
import { mkdtemp, mkdir, writeFile, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { createApiServer } from "../src/server.js";

test("health and catalog routes expose deterministic states", async () => {
  const root = await mkdtemp(join(tmpdir(), "electoral-api-"));
  await mkdir(join(root, "catalog/sources"), { recursive: true });
  await writeFile(join(root, "catalog/sources/tse.yml"), "id: tse\n");
  const server = createApiServer(root);
  await new Promise(resolve => server.listen(0, "127.0.0.1", resolve));
  const address = server.address();
  const base = "http://127.0.0.1:" + address.port;
  try {
    const health = await fetch(base + "/health");
    assert.equal(health.status, 200);
    assert.equal((await health.json()).status, "ok");
    const source = await fetch(base + "/api/v1/source");
    assert.match(await source.text(), /id: tse/);
    const catalog = await fetch(base + "/api/v1/catalog");
    const body = await catalog.json();
    assert.equal(catalog.status, 200);
    assert.equal(body.generated, false);
  } finally {
    await new Promise(resolve => server.close(resolve));
    await rm(root, { recursive: true, force: true });
  }
});

test("unknown routes and non-GET methods are rejected", async () => {
  const root = await mkdtemp(join(tmpdir(), "electoral-api-"));
  const server = createApiServer(root);
  await new Promise(resolve => server.listen(0, "127.0.0.1", resolve));
  const base = "http://127.0.0.1:" + server.address().port;
  try {
    assert.equal((await fetch(base + "/missing")).status, 404);
    assert.equal((await fetch(base + "/health", { method: "POST" })).status, 405);
  } finally {
    await new Promise(resolve => server.close(resolve));
    await rm(root, { recursive: true, force: true });
  }
});
