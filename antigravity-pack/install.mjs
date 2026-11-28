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

const PLUGIN_NAMES = [
  "rea-security-forensics",
  "architecture-studio",
  "engineering-craft",
  "ecc-core",
  "ecc-languages",
  "ecc-agentic-ai",
  "ecc-ops-business",
  "claude-code-setup",
  "replica-suite",
  "remotion-suite",
  "hyperframes",
  "ghost-editor",
  "ffmpeg-skill",
  "whisper-captions",
  "yt-dlp-media",
  "higgsfield-studio",
  "claude-shorts",
  "openmontage-studio",
  "playwright-qa",
  "chrome-devtools-plugin"
];

function resolvePythonExecutable() {
  const candidates =
    process.platform === "win32"
      ? [
          { cmd: "python", prefix: [] },
          { cmd: "py", prefix: ["-3"] },
          { cmd: "python3", prefix: [] }
        ]
      : [
          { cmd: "python3", prefix: [] },
          { cmd: "python", prefix: [] }
        ];

  for (const { cmd, prefix } of candidates) {
    const res = spawnSync(
      cmd,
      [...prefix, "-c", "import sys; print(sys.executable) if sys.version_info >= (3, 10) else sys.exit(1)"],
      { encoding: "utf8", shell: false }
    );
    if (res.status === 0) {
      const exe = (res.stdout || "").trim().split(/\r?\n/).pop();
      if (exe && fs.existsSync(exe)) {
        return exe;
      }
    }
  }
  return process.platform === "win32" ? "python" : "python3";
}

const pythonExe = resolvePythonExecutable();

const planned = [
  `Install @playwright/mcp & chrome-devtools-mcp in ${mcpRuntimesDir}`,
  ...PLUGIN_NAMES.map((name) => {
    const verb =
      name === "chrome-devtools-plugin" || name === "playwright-qa" || name === "ffmpeg-skill"
        ? "Deploy/wire plugin"
        : "Deploy plugin";
    return `${verb}: ${name} -> ${path.join(targetPluginsDir, name)}`;
  }),
  `Wire ffmpeg-skill local stdio MCP using Python: ${pythonExe}`,
  "Wire higgsfield-studio Streamable HTTP MCP: https://mcp.higgsfield.ai/mcp"
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

function syncPluginDirectory(srcDir, destDir) {
  const copyFilter = (source) => path.basename(source) !== "__pycache__";
  try {
    fs.rmSync(destDir, { recursive: true, force: true, maxRetries: 3, retryDelay: 100 });
    fs.cpSync(srcDir, destDir, { recursive: true, filter: copyFilter });
  } catch (err) {
    if (err && (err.code === "EPERM" || err.code === "EBUSY")) {
      // Running IDEs/MCP hosts on Windows can hold open handles inside a plugin dir; update files in place.
      fs.cpSync(srcDir, destDir, { recursive: true, force: true, filter: copyFilter });
    } else {
      throw err;
    }
  }
}

for (const pluginName of PLUGIN_NAMES) {
  const srcDir = path.join(packPluginsDir, pluginName);
  const destDir = path.join(targetPluginsDir, pluginName);
  syncPluginDirectory(srcDir, destDir);

  const templatePath = path.join(destDir, "mcp_config.template.json");
  if (fs.existsSync(templatePath)) {
    const ffmpegSkillMcpServer = path.join(destDir, "mcp", "server.py");
    const rawTemplate = fs.readFileSync(templatePath, "utf8");
    const rendered = rawTemplate
      .replaceAll("{{NODE_EXE}}", process.execPath.replaceAll("\\", "\\\\"))
      .replaceAll("{{PYTHON_EXE}}", pythonExe.replaceAll("\\", "\\\\"))
      .replaceAll("{{PLAYWRIGHT_CLI}}", playwrightCli.replaceAll("\\", "\\\\"))
      .replaceAll("{{CHROME_DEVTOOLS_CLI}}", chromeDevtoolsCli.replaceAll("\\", "\\\\"))
      .replaceAll("{{FFMPEG_SKILL_MCP_SERVER}}", ffmpegSkillMcpServer.replaceAll("\\", "\\\\"));
    fs.writeFileSync(path.join(destDir, "mcp_config.json"), rendered, "utf8");
    fs.rmSync(templatePath, { force: true });
  }
}

console.log(`\nSuccessfully installed all ${PLUGIN_NAMES.length} REA Enhanced Antigravity plugins!`);
console.log("Recommended Marketplace plugins to enable alongside this pack:");
console.log("  - Superpowers (antigravity-plugins-partners/plugin/superpowers)");
console.log("  - Context7    (antigravity-plugins-partners/plugin/context7)");
