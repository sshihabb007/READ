#!/usr/bin/env node
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const args = new Set(process.argv.slice(2));
const dryRun = args.has("--dry-run");
const rootDir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const packPluginsDir = path.join(rootDir, "antigravity-pack", "plugins");
const agyConfigDir = path.join(os.homedir(), ".gemini", "config");
const targetPluginsDir = path.join(agyConfigDir, "plugins");
const mcpRuntimesDir = path.join(agyConfigDir, "mcp-runtimes");

const planned = [
  `Install @playwright/mcp & chrome-devtools-mcp in ${mcpRuntimesDir}`,
  `Deploy plugin: rea-security-forensics -> ${path.join(targetPluginsDir, "rea-security-forensics")}`,
  `Deploy plugin: architecture-studio -> ${path.join(targetPluginsDir, "architecture-studio")}`,
  `Deploy plugin: engineering-craft -> ${path.join(targetPluginsDir, "engineering-craft")}`,
  `Deploy plugin: playwright-qa -> ${path.join(targetPluginsDir, "playwright-qa")}`,
  `Deploy/wire plugin: chrome-devtools-plugin -> ${path.join(targetPluginsDir, "chrome-devtools-plugin")}`
];

console.log("REA Enhanced Antigravity Pack Installer");
console.log("Planned actions:");
for (const item of planned) {
  console.log(`  - ${item}`);
}

if (dryRun) {
  console.log("\nDry run complete (no files written). Pass without --dry-run to install.");
  process.exit(0);
}

fs.mkdirSync(targetPluginsDir, { recursive: true });
fs.mkdirSync(mcpRuntimesDir, { recursive: true });

const runtimePkgPath = path.join(mcpRuntimesDir, "package.json");
if (!fs.existsSync(runtimePkgPath)) {
  fs.writeFileSync(
    runtimePkgPath,
    JSON.stringify({ name: "agy-mcp-runtimes", private: true, version: "1.0.0" }, null, 2) + "\n",
    "utf8"
  );
}

const npmCmd = process.platform === "win32" ? "npm.cmd" : "npm";
const npmRes = spawnSync(
  npmCmd,
  ["install", "--no-audit", "--no-fund", "@playwright/mcp", "chrome-devtools-mcp"],
  { cwd: mcpRuntimesDir, stdio: "inherit", shell: process.platform === "win32" }
);
if (npmRes.status !== 0) {
  console.error("Failed to install MCP runtimes in", mcpRuntimesDir);
  process.exit(npmRes.status ?? 1);
}

const playwrightCli = path.join(mcpRuntimesDir, "node_modules", "@playwright", "mcp", "cli.js");
const chromeDevtoolsCli = path.join(
  mcpRuntimesDir,
  "node_modules",
  "chrome-devtools-mcp",
  "out",
  "Default",
  "gen",
  "src",
  "bin",
  "chrome-devtools-mcp.js"
);

for (const pluginName of [
  "rea-security-forensics",
  "architecture-studio",
  "engineering-craft",
  "playwright-qa",
  "chrome-devtools-plugin"
]) {
  const srcDir = path.join(packPluginsDir, pluginName);
  const destDir = path.join(targetPluginsDir, pluginName);
  fs.rmSync(destDir, { recursive: true, force: true });
  fs.cpSync(srcDir, destDir, { recursive: true });

  const templatePath = path.join(destDir, "mcp_config.template.json");
  if (fs.existsSync(templatePath)) {
    const rawTemplate = fs.readFileSync(templatePath, "utf8");
    const rendered = rawTemplate
      .replaceAll("{{NODE_EXE}}", process.execPath.replaceAll("\\", "\\\\"))
      .replaceAll("{{PLAYWRIGHT_CLI}}", playwrightCli.replaceAll("\\", "\\\\"))
      .replaceAll("{{CHROME_DEVTOOLS_CLI}}", chromeDevtoolsCli.replaceAll("\\", "\\\\"));
    fs.writeFileSync(path.join(destDir, "mcp_config.json"), rendered, "utf8");
    fs.rmSync(templatePath, { force: true });
  }
}

console.log("\nSuccessfully installed all REA Enhanced Antigravity plugins!");
console.log("Recommended Marketplace plugins to enable alongside this pack:");
console.log("  - Superpowers (antigravity-plugins-partners/plugin/superpowers)");
console.log("  - Context7    (antigravity-plugins-partners/plugin/context7)");
