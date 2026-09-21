import subprocess
import json
from fastmcp import FastMCP
from aura_guardian import analyze_with_aiaura

# Initialize the MCP Server
mcp = FastMCP("AuraGuardian-Local")

@mcp.tool()
def scan_and_fix_local_file(file_path: str) -> str:
    """
    Runs a security scan on a specific local file and fetches the AIAura remediation.
    """
    # Run a targeted local scan
    scan_cmd = ["semgrep", "scan", "--config", "auto", "--json", file_path]
    result = subprocess.run(scan_cmd, capture_output=True, text=True)
    
    try:
        report = json.loads(result.stdout)
        findings = report.get("results", [])
    except json.JSONDecodeError:
        return "Error parsing local scan results."

    if not findings:
        return f"No vulnerabilities found in {file_path}."

    responses = []
    for finding in findings:
        threat_payload = {
            "file": finding.get("path"),
            "vuln_type": finding.get("extra", {}).get("message"),
            "code_snippet": finding.get("extra", {}).get("lines")
        }
        
        patched_code, explanation = analyze_with_aiaura(threat_payload)
        
        responses.append(f"### Threat: {finding.get('check_id')}\n")
        responses.append(f"**Engine Explanation:**\n{explanation}\n")
        responses.append(f"**AIAura Patched Code:**\n```python\n{patched_code}\n```\n")

    return "\n".join(responses)

if __name__ == "__main__":
    print("Starting AuraGuardian FastMCP Server...")
    mcp.run()
