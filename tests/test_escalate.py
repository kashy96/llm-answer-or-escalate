import json
import random

import numpy as np
import yaml

from escalate import data, metrics, parse, prompts, report
from escalate.retrieval import PassageIndex
from escalate.run import run_condition

# Invented mini-corpus in the PubMedQA format, so the tests run offline.
TINY = {
    str(1000 + i): {
        "QUESTION": q,
        "CONTEXTS": [f"Background on {topic}.", f"Results: {topic} {finding}."],
        "LABELS": ["BACKGROUND", "RESULTS"],
        "final_decision": label,
    }
    for i, (q, topic, finding, label) in enumerate([
        ("Does drug A lower blood pressure?", "drug A", "lowered blood pressure", "yes"),
        ("Does exercise B improve sleep?", "exercise B", "did not change sleep", "no"),
        ("Is marker C linked to relapse?", "marker C", "showed a weak trend", "maybe"),
        ("Does diet D reduce weight?", "diet D", "reduced weight", "yes"),
        ("Does screening E cut mortality?", "screening E", "did not cut mortality", "no"),
        ("Is gene F associated with risk?", "gene F", "was associated with risk", "yes"),
    ])
}


class FakeModel:
    """Right when it sees evidence, a coin flip otherwise."""

    def __init__(self, labels):
        self.labels = labels
        self.rng = random.Random(0)

    def generate(self, system, prompt, temperature=0.0):
        question = prompt.rsplit("Question: ", 1)[1]
        if "Evidence" in prompt:
            return json.dumps({"answer": self.labels[question], "confidence": 90})
        return json.dumps({"answer": self.rng.choice(parse.LABELS), "confidence": 60})


def test_parse_json_and_fallback():
    assert parse.parse('{"answer": "Yes", "confidence": 85}') == ("yes", 0.85, True)
    assert parse.parse('Sure! {"answer": "no", "confidence": 0.3}') == ("no", 0.3, True)
    assert parse.parse("I think the answer is maybe.") == ("maybe", None, False)


def test_metrics_basics():
    correct = np.array([True, True, False, False])
    conf = np.array([0.9, 0.8, 0.3, 0.2])
    assert metrics.accuracy(correct) == 0.5
    assert metrics.errors_caught(correct, conf, 0.5) == 1.0
    assert metrics.confident_error_rate(correct, conf, 0.8) == 0.0
    cov, risk = metrics.risk_coverage(correct, conf)
    assert risk[0] == 0.0 and risk[-1] == 0.5
    # perfectly ordered confidence beats reversed confidence
    assert metrics.aurc(correct, conf) < metrics.aurc(correct, 1 - conf)
    assert metrics.ece(np.array([True, False]), np.array([0.5, 0.5])) == 0.0


def test_stratified_sample(tmp_path):
    path = tmp_path / "pq.json"
    path.write_text(json.dumps(TINY))
    items = data.load(path)
    picked = data.sample(items, 3, seed=1)
    assert len({it.id for it in picked}) == len(picked)
    assert {it.label for it in picked} <= {"yes", "no", "maybe"}


def test_end_to_end(tmp_path):
    path = tmp_path / "pq.json"
    path.write_text(json.dumps(TINY))
    items = data.load(path)
    index = PassageIndex(items)
    assert index.search("drug A blood pressure", 1)[0][0] == "1000"

    cfg = yaml.safe_load(open("config.yaml"))
    cfg["output_dir"] = str(tmp_path / "results")
    cfg["data"]["path"] = str(path)
    cfg["report"]["bootstrap"] = 50
    raw = tmp_path / "results" / "raw"
    raw.mkdir(parents=True)

    model = FakeModel({it.question: it.label for it in items})
    for condition in prompts.CONDITIONS:
        run_condition(model, "fake", condition, items, index, {**cfg, "pause_seconds": 0}, raw / f"fake__{condition}.jsonl")

    df = report.load_runs(raw)
    summary = report.summarise(df, cfg).set_index("condition")
    assert summary.loc["gold_context", "accuracy"] == 1.0
    assert summary.loc["gold_context", "accuracy"] >= summary.loc["closed_book", "accuracy"]

    # re-running skips questions that are already stored
    run_condition(model, "fake", "closed_book", items, index, cfg, raw / "fake__closed_book.jsonl")
    assert sum(1 for _ in open(raw / "fake__closed_book.jsonl")) == len(items)
