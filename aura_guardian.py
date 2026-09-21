import json
import requests
import argparse
import os

AIAURA_API_URL = "https://aiaura.me/api/v1/analyze" # Replace with your actual endpoint
AIAURA_API_KEY = os.getenv("AIAURA_API_KEY")

def analyze_with_aiaura(vulnerability_data):
    """Sends the SAST/DAST finding to AIAura for a solution."""
    
    payload = {
        "model": "deepseek-r1", # Or whichever model handles security best on your backend
        "system_prompt": "You are a DevSecOps Architect. Analyze this vulnerability, explain the exploit, and provide the patched code block.",
        "vulnerability_context": vulnerability_data
    }
    
    headers = {
        "Authorization": f"Bearer {AIAURA_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        print(f"[*] Sending finding to {AIAURA_API_URL}...")
        response = requests.post(AIAURA_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        return response.json().get("solution_code")
    except Exception as e:
        print(f"[!] AIAura Engine Error: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="AuraGuardian: AIAura-powered SAST/DAST Remediation")
    parser.add_argument("--report", required=True, help="Path to the JSON scan report (e.g., semgrep.json)")
    args = parser.parse_args()

    # 1. Load the SAST/DAST report
    with open(args.report, 'r') as f:
        findings = json.load(f)

    # 2. Process findings through AIAura
    for finding in findings.get("results", []):
        print(f"[*] Processing Threat: {finding.get('check_id')}")
        
        threat_payload = {
            "file": finding.get("path"),
            "vuln_type": finding.get("extra", {}).get("message"),
            "code_snippet": finding.get("extra", {}).get("lines")
        }
        
        # 3. Get the solution from your platform
        remediation = analyze_with_aiaura(threat_payload)
        
        if remediation:
            print("[+] AIAura Solution Generated!")
            print("======================================")
            print(remediation)
            print("======================================\n")
            # Next phase: Automate GitHub PR creation with this fix

if __name__ == "__main__":
    main()
