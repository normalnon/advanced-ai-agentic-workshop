#!/usr/bin/env python3
"""
run_sleep_research.py

Automates a full literature‑search → research‑wiki ingestion workflow
for the topic **“Impact of sleep deprivation on cognitive performance.”**

Steps:
1. Query PubMed, OpenAlex, and arXiv (last 3 years, English).
2. Merge & deduplicate results.
3. For each paper:
   - build a slug (first author + year + short keyword)
   - write a markdown file under research‑wiki/papers/
   - log the addition.
4. Re‑generate the wiki query_pack (budget‑constrained summary).

Requires:
- `requests` (available in the plugin environment)
- Antigravity’s canonical helper `tools/research_wiki.py` (resolved automatically).

Run:
    cd /Users/anon.sae/Downloads/advanced-ai-agentic-workshop/plugin
    python3 run_sleep_research.py
"""

import json
import os
import re
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict

import requests

# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------
TOPIC = "sleep deprivation cognitive performance"
YEARS_BACK = 3
WIKI_ROOT = Path(
    "skills/Auto-claude-code-research-in-sleep/skills/research-wiki"
)  # relative to plugin root
PAPERS_DIR = WIKI_ROOT / "papers"
LOG_FILE = WIKI_ROOT / "log.md"

# ----------------------------------------------------------------------
# Helper utilities
# ----------------------------------------------------------------------
def slugify(title: str) -> str:
    """Make a short, filesystem‑safe slug from a title."""
    title = title.lower()
    title = re.sub(r"[^a-z0-9]+", "_", title)
    return title.strip("_")[:30]

def safe_write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fp:
        fp.write(content)

def log(message: str):
    ts = datetime.utcnow().isoformat() + "Z"
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as fp:
        fp.write(f"{ts} – {message}\n")

# ----------------------------------------------------------------------
# 1️⃣ Search APIs
# ----------------------------------------------------------------------
def pubmed_search(query: str) -> List[Dict]:
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    params = {
        "db": "pubmed",
        "term": query,
        "mindate": datetime.now().year - YEARS_BACK,
        "maxdate": datetime.now().year,
        "retmax": "200",
        "sort": "pub+date",
        "field": "title",
        "retmode": "json",
    }
    r = requests.get(f"{base}/esearch.fcgi", params=params, timeout=15)
    r.raise_for_status()
    ids = r.json()["esearchresult"]["idlist"]
    if not ids:
        return []
    params = {"db": "pubmed", "id": ",".join(ids), "retmode": "json"}
    r = requests.get(f"{base}/esummary.fcgi", params=params, timeout=15)
    r.raise_for_status()
    records = r.json()["result"]
    papers = []
    for pid in ids:
        rec = records[pid]
        papers.append({
            "title": rec.get("title"),
            "authors": [a["name"] for a in rec.get("authors", [])],
            "doi": rec.get("elocationid", "").replace("doi:", ""),
            "year": int(rec.get("pubdate", "0")[:4]),
            "source": "PubMed",
            "pmid": pid,
        })
    return papers

def openalex_search(query: str) -> List[Dict]:
    url = "https://api.openalex.org/works"
    params = {
        "filter": f"from_publication_date:{datetime.now().year - YEARS_BACK}-01-01,open_access.is_oa:true",
        "search": query,
        "per-page": "200",
        "sort": "publication_date:desc",
    }
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    data = r.json()
    papers = []
    for item in data.get("results", []):
        papers.append({
            "title": item.get("title"),
            "authors": [a["author"]["display_name"] for a in item.get("authorships", [])],
            "doi": item.get("doi", ""),
            "year": int(item.get("publication_year", 0)),
            "source": "OpenAlex",
            "openalex_id": item.get("id"),
        })
    return papers

def arxiv_search(query: str) -> List[Dict]:
    base = "http://export.arxiv.org/api/query"
    url = f"{base}?search_query=all:{query}&start=0&max_results=100"
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    import xml.etree.ElementTree as ET
    root = ET.fromstring(r.text)
    ns = {"a": "http://www.w3.org/2005/Atom"}
    papers = []
    for entry in root.findall("a:entry", ns):
        title = entry.find("a:title", ns).text.strip().replace("\n", " ")
        authors = [a.text for a in entry.findall("a:author/a:name", ns)]
        doi = ""
        for link in entry.findall("a:link", ns):
            if link.attrib.get("title") == "doi":
                doi = link.attrib.get("href").replace("https://doi.org/", "")
        year = int(entry.find("a:published", ns).text[:4])
        arxiv_id = entry.find("a:id", ns).text.split('/')[-1]
        papers.append({
            "title": title,
            "authors": authors,
            "doi": doi,
            "year": year,
            "source": "arXiv",
            "arxiv_id": arxiv_id,
        })
    return papers

# ----------------------------------------------------------------------
# 2️⃣ Merge & deduplicate
# ----------------------------------------------------------------------
def merge_papers(*lists: List[Dict]) -> List[Dict]:
    seen = {}
    merged = []
    for lst in lists:
        for p in lst:
            key = p.get("doi") or p.get("arxiv_id") or p.get("pmid")
            if not key:
                key = re.sub(r"\W+", "", p["title"]).lower()[:30]
            if key not in seen:
                seen[key] = True
                merged.append(p)
    merged.sort(key=lambda x: x.get("year", 0), reverse=True)
    return merged

# ----------------------------------------------------------------------
# 3️⃣ Write markdown entries
# ----------------------------------------------------------------------
def write_paper_md(paper: Dict):
    slug = slugify(paper["title"]) or "paper"
    node_id = f"paper:{slug}"
    file_path = PAPERS_DIR / f"{slug}.md"
    front = [
        "---",
        "type: paper",
        f"node_id: {node_id}",
        f"title: \"{paper['title']}\"",
        f"authors: [{', '.join([f'\"{a}\"' for a in paper['authors'][:5]])}]",
        f"year: {paper['year']}",
        f"venue: \"{paper['source']}\"",
        "external_ids:",
        f"  doi: \"{paper.get('doi', '')}\"",
        f"  pmid: \"{paper.get('pmid', '')}\"",
        f"  arxiv: \"{paper.get('arxiv_id', '')}\"",
        "tags: []",
        f"added: {datetime.utcnow().isoformat()}Z",
        "---",
        "",
        f"# {paper['title']}",
        "",
        "## One-line thesis",
        "",
        "_(Add a concise statement of the paper’s core contribution)_",
        "",
        "## Problem / Gap",
        "",
        "## Method",
        "",
        "## Key Results",
        "",
        "## Assumptions",
        "",
        "## Limitations / Failure Modes",
        "",
        "## Reusable Ingredients",
        "",
        "## Open Questions",
        "",
        "## Claims",
        "",
        "## Connections",
        "",
        "## Relevance to This Project",
        "",
        "",
    ]
    safe_write(file_path, "\n".join(front))
    log(f"Added paper markdown: {file_path.name}")

# ----------------------------------------------------------------------
# 4️⃣ Rebuild query_pack via canonical helper
# ----------------------------------------------------------------------
def rebuild_query_pack():
    cwd = Path.cwd()
    possible = [
        cwd / ".aris" / "tools" / "research_wiki.py",
        cwd / "tools" / "research_wiki.py",
    ]
    aris_repo = os.getenv("ARIS_REPO", "")
    if aris_repo:
        possible.append(Path(aris_repo) / "tools" / "research_wiki.py")
    script = next((p for p in possible if p.is_file()), None)
    if not script:
        print("❗️ research_wiki.py not found – run `install_aris.sh` or set ARIS_REPO.")
        return
    os.system(f"python3 {script} query_pack {WIKI_ROOT}")

# ----------------------------------------------------------------------
# Main driver
# ----------------------------------------------------------------------
def main():
    print(f"🔎 Searching literature for: {TOPIC}")
    pubmed = pubmed_search(TOPIC)
    print(f"• PubMed:   {len(pubmed)} papers")
    openalex = openalex_search(TOPIC)
    print(f"• OpenAlex: {len(openalex)} papers")
    arxiv = arxiv_search(TOPIC)
    print(f"• arXiv:    {len(arxiv)} papers")
    papers = merge_papers(pubmed, openalex, arxiv)
    print(f"🔗 Merged & deduped: {len(papers)} unique papers")
    PAPERS_DIR.mkdir(parents=True, exist_ok=True)
    for p in papers:
        write_paper_md(p)
        time.sleep(0.05)
    log(f"Literature ingest completed – {len(papers)} papers added for topic '{TOPIC}'")
    print("⚙️ Rebuilding wiki query_pack …")
    rebuild_query_pack()
    print("✅ Done – research-wiki is up-to-date!")

if __name__ == "__main__":
    main()
