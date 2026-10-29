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


test("catalog endpoint expands manifest entries into dashboard datasets", async () => {
  const root = await mkdtemp(join(tmpdir(), "electoral-api-catalog-"));
  const catalogDir = join(root, "catalog/tse/datasets");
  await mkdir(catalogDir, { recursive: true });
  await writeFile(join(catalogDir, "resultados.json"), JSON.stringify({
    id: "dataset-1", name: "resultados", title: "Resultados eleitorais",
    notes: "Dados de votação", organization: "Tribunal Superior Eleitoral",
    metadata_modified: "2026-10-01", resources: [{ id: "resource-1", format: "CSV" }]
  }));
  await writeFile(join(catalogDir, "manifest.json"), JSON.stringify({
    complete: true, dataset_count: 1, discovered_at: "2026-10-29T00:00:00Z",
    datasets: [{ name: "resultados", path: "resultados.json", sha256: "abc" }]
  }));
  const server = createApiServer(root);
  await new Promise(resolve => server.listen(0, "127.0.0.1", resolve));
  const base = "http://127.0.0.1:" + server.address().port;
  try {
    const response = await fetch(base + "/api/v1/catalog");
    const body = await response.json();
    assert.equal(response.status, 200);
    assert.equal(body.generated, true);
    assert.equal(body.datasets.length, 1);
    assert.equal(body.datasets[0].title, "Resultados eleitorais");
    assert.equal(body.datasets[0].organization, "Tribunal Superior Eleitoral");
    assert.equal(body.datasets[0].resources[0].format, "CSV");
  } finally {
    await new Promise(resolve => server.close(resolve));
    await rm(root, { recursive: true, force: true });
  }
});
