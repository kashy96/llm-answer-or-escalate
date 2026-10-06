"""Metrics for selective answering.

`correct` is a boolean array (answer == label) and `conf` a float array in
[0, 1]. Higher confidence should mean "more likely to be right".
"""

import numpy as np


def accuracy(correct):
    return float(np.mean(correct))


def confident_error_rate(correct, conf, threshold=0.8):
    """Share of all questions answered wrongly with confidence >= threshold.

    This is the failure we care most about: a wrong answer the system would
    not have escalated.
    """
    return float(np.mean(~correct & (conf >= threshold)))


def ece(correct, conf, bins=10):
    """Expected calibration error with equal-width bins."""
    idx = np.minimum((conf * bins).astype(int), bins - 1)
    total = 0.0
    for b in range(bins):
        m = idx == b
        if m.any():
            total += m.mean() * abs(correct[m].mean() - conf[m].mean())
    return float(total)


def risk_coverage(correct, conf):
    """Answer the most confident questions first.

    Returns (coverage, risk): after answering the top i questions, coverage is
    i / n and risk is the error rate among those i.
    """
    order = np.argsort(-conf, kind="stable")
    errors = np.cumsum(~correct[order])
    answered = np.arange(1, len(correct) + 1)
    return answered / len(correct), errors / answered


def aurc(correct, conf):
    """Area under the risk-coverage curve. Lower is better."""
    _, risk = risk_coverage(correct, conf)
    return float(risk.mean())


def errors_caught(correct, conf, escalation_rate):
    """Escalate the least confident share of questions; what share of all errors does that catch?"""
    wrong = ~correct
    if not wrong.any():
        return float("nan")
    n_escalated = int(round(escalation_rate * len(correct)))
    escalated = np.argsort(conf, kind="stable")[:n_escalated]
    return float(wrong[escalated].sum() / wrong.sum())


def bootstrap_ci(stat, *arrays, n=1000, seed=0, alpha=0.05):
    rng = np.random.default_rng(seed)
    size = len(arrays[0])
    values = []
    for _ in range(n):
        i = rng.integers(0, size, size)
        values.append(stat(*(a[i] for a in arrays)))
    lo, hi = np.nanpercentile(values, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    return float(lo), float(hi)
