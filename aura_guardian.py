import json
import requests
import argparse
import os
import time
from github import Github

AIAURA_API_URL = "https://aiaura.me/api/v1/analyze"
AIAURA_API_KEY = os.getenv("AIAURA_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def analyze_with_aiaura(threat_payload):
    """Fetches the secure code fix from AIAura."""
    headers = {"Authorization": f"Bearer {AIAURA_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "deepseek-r1",
        "system_prompt": "You are an automated DevSecOps tool. Return ONLY the fully patched, production-ready code block. No markdown wrappers.",
        "vulnerability_context": threat_payload
    }
    try:
        response = requests.post(AIAURA_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        return response.json().get("solution_code"), response.json().get("explanation")
    except Exception as e:
        print(f"[!] AIAura Engine Error: {e}")
        return None, None

def create_remediation_pr(repo_name, file_path, patched_code, explanation, threat_id):
    """Commits the AIAura fix to a new branch and opens a Pull Request."""
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(repo_name)
    
    # 1. Create a new branch
    main_branch = repo.get_branch(repo.default_branch)
    branch_name = f"aura-sec-fix/{threat_id}-{int(time.time())}"
    repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=main_branch.commit.sha)
    
    # 2. Update the vulnerable file
    contents = repo.get_contents(file_path, ref=repo.default_branch)
    commit_message = f"🔒 Security Auto-Fix: Resolves {threat_id}"
    repo.update_file(contents.path, commit_message, patched_code, contents.sha, branch=branch_name)
    
    # 3. Open the Pull Request
    pr_body = f"### AuraGuardian Automated Remediation\n**AIAura** detected and resolved a `{threat_id}` vulnerability.\n\n**Engine Analysis:**\n{explanation}"
    pr = repo.create_pull(title=commit_message, body=pr_body, head=branch_name, base=repo.default_branch)
    print(f"[+] Successfully created PR: {pr.html_url}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", required=True, help="Path to JSON scan report")
    parser.add_argument("--repo", required=True, help="GitHub repository (e.g., owner/repo)")
    args = parser.parse_args()

    with open(args.report, 'r') as f:
        findings = json.load(f).get("results", [])

    for finding in findings:
        threat_id = finding.get('check_id')
        file_path = finding.get("path")
        print(f"[*] Processing: {threat_id} in {file_path}")
        
        threat_payload = {
            "file": file_path,
            "vuln_type": finding.get("extra", {}).get("message"),
            "code_snippet": finding.get("extra", {}).get("lines")
        }
        
        patched_code, explanation = analyze_with_aiaura(threat_payload)
        
        if patched_code:
            create_remediation_pr(args.repo, file_path, patched_code, explanation, threat_id.replace('.', '-'))

if __name__ == "__main__":
    if not GITHUB_TOKEN or not AIAURA_API_KEY:
        print("[!] Error: AIAURA_API_KEY and GITHUB_TOKEN environment variables are required.")
        exit(1)
    main()
