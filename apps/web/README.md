# Interface Web

Aplicação Next.js com App Router, TypeScript e interface responsiva para apresentar o projeto e consultar o estado do catálogo pela API Node.

## Executar

```bash
cd apps/web
npm install
NEXT_PUBLIC_API_URL=http://localhost:3001 npm run dev
```

A interface não incorpora resultados eleitorais fictícios. Sem API, informa indisponibilidade; sem manifesto CKAN, informa que a descoberta ainda precisa ser executada.
