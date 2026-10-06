"""PubMedQA (PQA-L): the 1,000 expert-labelled research questions.

Each item is a question written from the title of a PubMed article, the
article's abstract without its conclusion (split into labelled sections),
and a yes / no / maybe answer given by the annotators.
"""

import json
import random
from dataclasses import dataclass
from pathlib import Path

import requests

PQAL_URL = "https://raw.githubusercontent.com/pubmedqa/pubmedqa/master/data/ori_pqal.json"


@dataclass
class Item:
    id: str
    question: str
    contexts: list
    sections: list
    label: str


def download(path, url=PQAL_URL):
    path = Path(path)
    if path.exists():
        return path
    path.parent.mkdir(parents=True, exist_ok=True)
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    path.write_bytes(resp.content)
    return path


def load(path):
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    items = []
    for pmid, row in raw.items():
        contexts = row["CONTEXTS"]
        sections = row.get("LABELS") or [""] * len(contexts)
        items.append(Item(pmid, row["QUESTION"], contexts, sections, row["final_decision"]))
    return items


def sample(items, n, seed):
    """Stratified sample, so the yes/no/maybe mix matches the full set."""
    if not n or n >= len(items):
        return list(items)
    rng = random.Random(seed)
    groups = {}
    for it in items:
        groups.setdefault(it.label, []).append(it)
    picked = []
    for label in sorted(groups):
        group = groups[label]
        k = round(n * len(group) / len(items))
        picked += rng.sample(group, min(k, len(group)))
    rng.shuffle(picked)
    return picked
