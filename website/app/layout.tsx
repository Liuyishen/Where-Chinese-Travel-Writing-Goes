import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Where Chinese-Language Travel Writing Goes",
  description: "A research archive of place, mobility, and cultural imagination in Chinese-language travel writing, 1980–2025.",
  other: {
    "codex-preview": "development",
  },
  icons: {
    icon: "/favicon.svg",
    shortcut: "/favicon.svg",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  );
}
