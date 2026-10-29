"use client";

import { useEffect, useState } from "react";

type CatalogState = { generated?: boolean; datasets?: unknown[]; message?: string; catalog?: unknown };
export default function Home() {
  const [catalog, setCatalog] = useState<CatalogState | null>(null);
  const [error, setError] = useState("");
  useEffect(() => {
    const endpoint = process.env.NEXT_PUBLIC_API_URL || "http://localhost:3001";
    fetch(endpoint + "/api/v1/catalog")
      .then(async response => {
        if (!response.ok) throw new Error("API respondeu HTTP " + response.status);
        return response.json();
      })
      .then(setCatalog)
      .catch(() => setError("API indisponível. Inicie o serviço Node.js na porta 3001 para consultar o catálogo local."));
  }, []);
  return (
    <main className="shell">
      <header><span className="eyebrow">NR TECH · DADOS PÚBLICOS</span><h1>Brasil Eleitoral <em>DataLab</em></h1>
        <p>Engenharia, rastreabilidade e exploração de dados eleitorais brasileiros.</p></header>
      <section className="panel">
        <h2>Catálogo do TSE</h2>
        {error && <p role="status">{error}</p>}
        {!catalog && !error && <p>Consultando o serviço de catálogo...</p>}
        {catalog && !catalog.generated && <p>{catalog.message || "O catálogo local ainda não foi gerado."}</p>}
        {catalog?.generated && <p>Manifesto de catálogo disponível. Consulte a API para obter os metadados completos.</p>}
        <a href="https://dadosabertos.tse.jus.br/" target="_blank" rel="noreferrer">Abrir Dados Abertos do TSE ↗</a>
      </section>
      <footer>Dados e metadados devem ser interpretados conforme a documentação oficial de cada conjunto.</footer>
    </main>
  );
}
