import { createServer } from "node:http";
import { readFile } from "node:fs/promises";
import { resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const repositoryRoot = resolve(here, "../../..");

export async function handleRequest(request, response, root = repositoryRoot) {
  const url = new URL(request.url || "/", "http://localhost");
  const send = (status, body) => {
    response.writeHead(status, {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "no-store",
      "x-content-type-options": "nosniff",
    });
    response.end(JSON.stringify(body));
  };

  if (request.method !== "GET") {
    response.setHeader("allow", "GET");
    return send(405, { error: "method_not_allowed" });
  }
  if (url.pathname === "/health" || url.pathname === "/api/v1/health") {
    return send(200, { status: "ok", service: "brasil-eleitoral-api", version: "v1" });
  }
  if (url.pathname === "/api/v1/source") {
    try {
      const source = await readFile(resolve(root, "catalog/sources/tse.yml"), "utf8");
      response.writeHead(200, { "content-type": "text/yaml; charset=utf-8",
        "cache-control": "public, max-age=300", "x-content-type-options": "nosniff" });
      return response.end(source);
    } catch {
      return send(404, { error: "source_catalog_not_found" });
    }
  }
  if (url.pathname === "/api/v1/catalog") {
    try {
      const catalogDir = resolve(root, "catalog/tse/datasets");
      const manifest = JSON.parse(await readFile(resolve(catalogDir, "manifest.json"), "utf8"));
      const entries = Array.isArray(manifest.datasets) ? manifest.datasets : [];
      const datasets = await Promise.all(entries.map(async (entry) => {
        const relativePath = typeof entry.path === "string" ? entry.path : "";
        // Manifest entries must be plain JSON filenames inside the catalog directory.
        if (!/^[A-Za-z0-9][A-Za-z0-9._-]{0,199}\.json$/.test(relativePath)) return null;
        try {
          const dataset = JSON.parse(await readFile(resolve(catalogDir, relativePath), "utf8"));
          return {
            id: dataset.id, name: dataset.name, title: dataset.title,
            notes: dataset.notes, description: dataset.notes,
            organization: dataset.organization || "Sem órgão",
            metadata_modified: dataset.metadata_modified,
            resources: Array.isArray(dataset.resources) ? dataset.resources : [],
          };
        } catch {
          return null;
        }
      }));
      const available = datasets.filter(Boolean);
      return send(200, {
        source: "tse", generated: true, complete: Boolean(manifest.complete),
        discovered_at: manifest.discovered_at,
        dataset_count: Number(manifest.dataset_count || available.length),
        datasets: available,
      });
    } catch (error) {
      if (error.code === "ENOENT") {
        return send(200, { source: "tse", generated: false, datasets: [],
          message: "Execute scripts/discover_tse_catalog.py em ambiente com acesso ao portal do TSE." });
      }
      return send(500, { error: "catalog_unavailable" });
    }
  }
  return send(404, { error: "not_found" });
}

export function createApiServer(root = repositoryRoot) {
  return createServer((request, response) => {
    handleRequest(request, response, root).catch(() => {
      if (!response.headersSent) {
        response.writeHead(500, { "content-type": "application/json; charset=utf-8" });
      }
      response.end(JSON.stringify({ error: "internal_server_error" }));
    });
  });
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const port = Number(process.env.PORT || 3001);
  if (!Number.isInteger(port) || port < 1 || port > 65535) {
    throw new Error("PORT must be an integer between 1 and 65535");
  }
  createApiServer().listen(port, "0.0.0.0", () => {
    process.stdout.write("Brasil Eleitoral API listening on port " + port + "\n");
  });
}
