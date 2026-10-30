import test from "node:test";
import assert from "node:assert/strict";
import { mkdtemp, mkdir, writeFile, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { createApiServer } from "./server.js";

async function withServer(run) {
  const root = await mkdtemp(join(tmpdir(), "brasil-eleitoral-api-"));
  const server = createApiServer(root);
  await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
  const address = server.address();
  try {
    await run(`http://127.0.0.1:${address.port}`, root);
  } finally {
    await new Promise((resolve, reject) => server.close((error) => error ? reject(error) : resolve()));
    await rm(root, { recursive: true, force: true });
  }
}

test("health endpoint returns service status", async () => {
  await withServer(async (base) => {
    const response = await fetch(base + "/health");
    assert.equal(response.status, 200);
    assert.equal((await response.json()).status, "ok");
  });
});

test("catalog endpoint reads valid dataset JSON files", async () => {
  await withServer(async (base, root) => {
    const directory = join(root, "catalog", "tse", "datasets");
    await mkdir(directory, { recursive: true });
    await writeFile(join(directory, "dataset-1.json"), JSON.stringify({
      id: "dataset-1", name: "resultados", title: "Resultados eleitorais",
      resources: [{ id: "resource-1", format: "CSV" }]
    }));
    await writeFile(join(directory, "manifest.json"), JSON.stringify({
      complete: true, dataset_count: 1, discovered_at: "2026-10-30T00:00:00Z",
      datasets: [{ path: "dataset-1.json" }]
    }));
    const response = await fetch(base + "/api/v1/catalog");
    assert.equal(response.status, 200);
    const body = await response.json();
    assert.equal(body.generated, true);
    assert.equal(body.datasets.length, 1);
    assert.equal(body.datasets[0].title, "Resultados eleitorais");
    assert.equal(body.datasets[0].resources[0].format, "CSV");
  });
});

test("catalog endpoint rejects unsafe manifest paths", async () => {
  await withServer(async (base, root) => {
    const directory = join(root, "catalog", "tse", "datasets");
    await mkdir(directory, { recursive: true });
    await writeFile(join(directory, "manifest.json"), JSON.stringify({
      datasets: [{ path: "../outside.json" }]
    }));
    const response = await fetch(base + "/api/v1/catalog");
    assert.equal(response.status, 200);
    assert.deepEqual((await response.json()).datasets, []);
  });
});

test("unknown routes return 404 and unsupported methods return 405", async () => {
  await withServer(async (base) => {
    assert.equal((await fetch(base + "/missing")).status, 404);
    assert.equal((await fetch(base + "/health", { method: "POST" })).status, 405);
  });
});
