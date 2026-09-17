import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "export",
  trailingSlash: true,
  ...(process.env.GITHUB_ACTIONS
    ? { basePath: "/Where-Chinese-Travel-Writing-Goes" }
    : {}),
};

export default nextConfig;
