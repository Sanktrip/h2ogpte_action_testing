# filename: fetch_pr3_details.py
# execution: true
import os
import json
import requests

# GitHub repository and PR details
owner = "Sanktrip"
repo = "h2ogpte_action_testing"
pr_number = 3

# Authentication using the provided PAT
token = "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"
if not token:
    raise EnvironmentError("GITHUB_PAT_TMP environment variable not set")

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json",
    'X-GitHub-Api-Version': '2022-11-28'
}

# 1. Get PR metadata
pr_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
pr_resp = requests.get(pr_url, headers=headers)
pr_resp.raise_for_status()
pr_data = pr_resp.json()

# 2. List changed files in the PR
files_url = pr_data["url"] + "/files"
files_resp = requests.get(files_url, headers=headers)
files_resp.raise_for_status()
files_data = files_resp.json()

# Prepare a summary of changed files
summary_lines = [
    f"PR #{pr_number}: {pr_data.get('title','(no title)')}",
    f"Base branch: {pr_data['base']['ref']}",
    f"Head branch: {pr_data['head']['ref']}",
    f"Author: {pr_data['user']['login']}",
    f"Created at: {pr_data['created_at']}",
    f"Number of changed files: {len(files_data)}",
    "",
    "Changed files:",
    "```",
]
for f in files_data:
    status = f["status"]  # added, modified, removed, renamed
    filename = f["filename"]
    additions = f["additions"]
    deletions = f["deletions"]
    changes = f["changes"]
    summary_lines.append(f"{status.upper():8} {filename} (+{additions}/-{deletions}, total {changes})")
summary_lines.append("```")
summary_text = "\n".join(summary_lines)

# 3. Fetch the full content of each changed file from the head branch
file_contents = {}
for f in files_data:
    # Use raw_url provided by the API (points to the blob in the head commit)
    raw_url = f["raw_url"]
    content_resp = requests.get(raw_url, headers=headers)
    content_resp.raise_for_status()
    file_contents[f["filename"]] = content_resp.text

# 4. Write the summary and the file contents to disk for later analysis
os.makedirs("pr3_review", exist_ok=True)

# Write summary
with open("pr3_review/summary.txt", "w", encoding="utf-8") as sf:
    sf.write(summary_text)

# Write each changed file's content
for path, content in file_contents.items():
    # Preserve directory structure inside pr3_review
    full_path = os.path.join("pr3_review", path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as cf:
        cf.write(content)

# Print helpful output for the user
print("=== PR Summary ===")
print(summary_text)
print("\nFile contents have been saved under the 'pr3_review/' directory.")
print("You can now open those files to inspect the logical changes.")