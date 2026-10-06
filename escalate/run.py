"""Run the experiments and store every model reply as JSONL.

    python -m escalate.run                      # all models, all conditions
    python -m escalate.run --model gemini-flash --limit 10

Results are appended one line per question, so an interrupted run picks up
where it stopped.
"""

import argparse
import json
import os
import time
from collections import Counter
from pathlib import Path

import yaml

from . import data, models, parse, prompts
from .retrieval import PassageIndex


def load_env(path=".env"):
    p = Path(path)
    if not p.exists():
        return
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"'))


def acquire_lock(path, stale_hours=8):
    """One writer per model. A lock older than `stale_hours` is left over from a crash and is replaced."""
    path = Path(path)
    if path.exists() and time.time() - path.stat().st_mtime > stale_hours * 3600:
        path.unlink(missing_ok=True)
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        return False
    os.write(fd, str(os.getpid()).encode())
    os.close(fd)
    return True


def run_condition(model, model_key, condition, items, index, cfg, path):
    path = Path(path)
    done = set()
    if path.exists():
        with path.open(encoding="utf-8") as f:
            done = {json.loads(line)["id"] for line in f if line.strip()}
    todo = [it for it in items if it.id not in done]
    print(f"{model_key} / {condition}: {len(done)} done, {len(todo)} to go")

    n_samples = cfg["confidence"]["consistency_samples"]
    temperature = cfg["confidence"]["sample_temperature"]
    k = cfg["retrieval"]["k"]
    pause = cfg.get("pause_seconds", 0)

    with path.open("a", encoding="utf-8") as f:
        for n, item in enumerate(todo, 1):
            hits = index.search(item.question, k) if condition == "retrieved" else []
            prompt = prompts.build(condition, item, hits)

            raw = models.with_retries(lambda: model.generate(prompts.SYSTEM, prompt, 0.0))
            answer, confidence, ok = parse.parse(raw)

            samples = []
            for _ in range(n_samples):
                reply = models.with_retries(lambda: model.generate(prompts.SYSTEM, prompt, temperature))
                samples.append(parse.parse(reply)[0])
            consistency = Counter(samples)[answer] / len(samples) if samples else None

            retrieved_ids = [h[0] for h in hits]
            record = {
                "id": item.id,
                "model": model_key,
                "condition": condition,
                "label": item.label,
                "answer": answer,
                "confidence": confidence,
                "parsed": ok,
                "consistency": consistency,
                "samples": samples,
                "retrieved_ids": retrieved_ids,
                "gold_retrieved": (item.id in retrieved_ids) if hits else None,
                "raw": raw,
            }
            f.write(json.dumps(record) + "\n")
            f.flush()
            if n % 25 == 0:
                print(f"  {n}/{len(todo)}")
            if pause:
                time.sleep(pause)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", default="config.yaml")
    ap.add_argument("--model", help="only this model (a key under `models` in the config)")
    ap.add_argument("--condition", choices=prompts.CONDITIONS)
    ap.add_argument("--limit", type=int, help="only the first N sampled questions, for a quick check")
    args = ap.parse_args()

    cfg = yaml.safe_load(Path(args.config).read_text(encoding="utf-8"))
    load_env()

    corpus = data.load(data.download(cfg["data"]["path"]))
    items = data.sample(corpus, cfg["data"]["n_questions"], cfg["seed"])
    if args.limit:
        items = items[: args.limit]
    index = PassageIndex(corpus)

    out_dir = Path(cfg["output_dir"]) / "raw"
    out_dir.mkdir(parents=True, exist_ok=True)

    for key, spec in cfg["models"].items():
        if args.model and key != args.model:
            continue
        lock = out_dir / f"{key}.lock"
        if not acquire_lock(lock):
            print(f"{key}: another run is already writing these results ({lock}); skipping.")
            continue
        try:
            model = models.build(spec)
            for condition in prompts.CONDITIONS:
                if args.condition and condition != args.condition:
                    continue
                run_condition(model, key, condition, items, index, cfg, out_dir / f"{key}__{condition}.jsonl")
        except models.DailyQuotaExceeded:
            print(f"{key}: daily API quota reached. Progress is saved; run the same command tomorrow to continue.")
        finally:
            lock.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
