import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Brasil Eleitoral DataLab",
  description: "Catálogo público e análise reproduzível de dados eleitorais brasileiros.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="pt-BR"><body>{children}</body></html>;
}
