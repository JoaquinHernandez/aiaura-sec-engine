# aiaura-sec-engine
# 🛡️ AuraGuardian (aiaura-sec-engine)

[![DevSecOps](https://img.shields.io/badge/DevSecOps-Autonomous-blue.svg)](#) [![Powered By](https://img.shields.io/badge/Powered_By-AIAura.me-purple.svg)](https://aiaura.me) [![Python 3.11+](https://img.shields.io/badge/Python-3.11+-yellow.svg)](#) [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](#)

**AuraGuardian** is a zero-friction, autonomous DevSecOps engine. It doesn't just scan for vulnerabilities—it leverages the multi-model intelligence of **AIAura** to analyze exploits, rewrite secure code, and automatically open Pull Requests with the fix.

By wrapping industry-standard tools (like Semgrep) in an intelligent LLM-driven orchestration layer, AuraGuardian bridges the gap between vulnerability discovery and remediation.

---

## ✨ Features

- **Autonomous Remediation:** Automatically generates production-ready code fixes for identified SAST/DAST vulnerabilities.
- **Zero-Touch PR Creation:** Branches the repository, applies the patched code, and opens a GitHub Pull Request with a detailed threat analysis.
- **AIAura Intelligence Engine:** Powered by `https://aiaura.me`, utilizing models like DeepSeek-R1 for complex vulnerability context resolution.
- **IDE Native (FastMCP):** Includes a local Model Context Protocol (MCP) server to trigger scans and generate AI fixes directly inside your editor.
- **CI/CD Native:** Drops seamlessly into GitHub Actions to protect the `main` branch continuously.

---

## 🏗️ Architecture Flow

1. **Trigger:** A push or PR initiates the pipeline.
2. **Scan:** Lightweight Semgrep execution generates a structural vulnerability report.
3. **Analyze:** The JSON payload is routed to the `aiaura.me` API.
4. **Remediate:** AIAura returns the patched code block and threat explanation.
5. **Commit:** AuraGuardian creates a new branch (`aura-sec-fix/*`) and opens a Pull Request.

---

## 🚀 Quickstart

### Prerequisites
- Python 3.11+
- An active `AIAURA_API_KEY` from [aiaura.me](https://aiaura.me)
- A `GITHUB_TOKEN` with repository write access

### Installation

Clone the repository and install the required dependencies:

```bash
git clone [https://github.com/yourusername/aiaura-sec-engine.git](https://github.com/yourusername/aiaura-sec-engine.git)
cd aiaura-sec-engine
pip install -r requirements.txt
