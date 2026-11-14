"""Build a self-hosted SVG from public repository metadata only (stdlib only)."""

import argparse
from collections import Counter
from datetime import datetime, timezone
from html import escape
import json
import os
from pathlib import Path
import subprocess
from urllib.request import Request, urlopen


def public_repos(username, local):
    repos = []
    for page in range(1, 101):
        path = f"/users/{username}/repos?per_page=100&page={page}&type=owner"
        if local:
            result = subprocess.run(
                ["gh", "api", path], check=True, capture_output=True, text=True,
                encoding="utf-8",
            )
            batch = json.loads(result.stdout)
        else:
            headers = {"Accept": "application/vnd.github+json", "User-Agent": "Herz1-profile"}
            if os.environ.get("GITHUB_TOKEN"):
                headers["Authorization"] = "Bearer " + os.environ["GITHUB_TOKEN"]
            with urlopen(Request("https://api.github.com" + path, headers=headers), timeout=30) as response:
                batch = json.load(response)
        repos.extend(repo for repo in batch if not repo.get("private"))
        if len(batch) < 100:
            return repos
    raise RuntimeError("Repository pagination limit reached")


def render(repos):
    originals = [repo for repo in repos if not repo.get("fork")]
    languages = Counter(repo["language"] for repo in originals if repo.get("language"))
    colors = ["#b83a35", "#d76b62", "#c58b42", "#8e6b58", "#5f7d72", "#b8a58c"]
    top = languages.most_common(5)
    remainder = sum(languages.values()) - sum(count for _, count in top)
    if remainder:
        top.append(("Other", remainder))
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    pieces = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="304" viewBox="0 0 960 304" role="img" aria-label="Herz1 public repository statistics">
<style>
 .bg {{fill:#f8f2e8;stroke:#decfc0}} .text {{fill:#28211f}} .muted {{fill:#74645e}}
 text {{font-family:Segoe UI,Arial,sans-serif}}
 @media(prefers-color-scheme:dark) {{.bg{{fill:#171b24;stroke:#3b3540}} .text{{fill:#f8f2e8}} .muted{{fill:#c2b4aa}}}}
</style>
<rect x="1" y="1" width="958" height="302" rx="16" class="bg"/>
<text x="30" y="38" class="muted" font-family="monospace" font-size="12" letter-spacing="2">HERZ1 / PUBLIC SNAPSHOT</text>
<text x="930" y="38" text-anchor="end" class="muted" font-size="11">UPDATED {now} UTC</text>''']
    metrics = [
        (len(repos), "Public repositories"),
        (sum(repo.get("stargazers_count", 0) for repo in repos), "Stars on public repos"),
        (len(languages), "Languages across original repos"),
    ]
    for index, (value, label) in enumerate(metrics):
        x = 30 + index * 310
        pieces.append(f'<text x="{x}" y="101" class="text" font-size="42" font-weight="700">{value}</text>')
        pieces.append(f'<text x="{x}" y="128" class="muted" font-size="13">{label}</text>')
    pieces.append('<path d="M30 151H930" stroke="#b83a35" stroke-opacity=".24"/>')
    pieces.append('<text x="30" y="181" class="muted" font-size="12">LANGUAGES · by primary language of non-fork public repositories</text>')
    x = 30.0
    total = sum(languages.values())
    for index, (language, count) in enumerate(top):
        width = 900 * count / total
        color = colors[index]
        pieces.append(f'<rect x="{x:.2f}" y="198" width="{width:.2f}" height="12" fill="{color}"><title>{escape(language)}: {count} repositories</title></rect>')
        lx = 30 + (index % 3) * 310
        ly = 237 + (index // 3) * 26
        pieces.append(f'<circle cx="{lx + 4}" cy="{ly - 4}" r="4" fill="{color}"/><text x="{lx + 17}" y="{ly}" class="text" font-size="13">{escape(language)} <tspan class="muted">{count / total:.0%}</tspan></text>')
        x += width
    if not top:
        pieces.append('<text x="30" y="234" class="muted" font-size="13">No public language data yet.</text>')
    pieces.append('</svg>')
    return "\n".join(pieces) + "\n"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--username", default="Herz1")
    parser.add_argument("--local", action="store_true", help="Use the existing gh CLI login")
    args = parser.parse_args()
    output = Path(__file__).resolve().parents[1] / "assets" / "snapshot.svg"
    output.write_text(render(public_repos(args.username, args.local)), encoding="utf-8")
    print(f"Updated {output.name}")
