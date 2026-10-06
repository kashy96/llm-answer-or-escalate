CONDITIONS = ("closed_book", "gold_context", "retrieved")

SYSTEM = (
    "You answer research questions using biomedical abstracts. "
    "Answer yes, no or maybe, and give your confidence that the answer is correct "
    "as a number from 0 to 100. Be honest about uncertainty: a low confidence is "
    "better than a confident wrong answer. "
    'Reply with JSON only, in the form {"answer": "yes|no|maybe", "confidence": <0-100>}.'
)


def _passages(pairs):
    return "\n".join(f"[{section or 'TEXT'}] {text}" for section, text in pairs)


def build(condition, item, hits=()):
    if condition == "closed_book":
        return f"Question: {item.question}"
    if condition == "gold_context":
        evidence = _passages(zip(item.sections, item.contexts))
        return f"Evidence from the study abstract:\n{evidence}\n\nQuestion: {item.question}"
    if condition == "retrieved":
        evidence = _passages((section, text) for _, section, text, _ in hits)
        return (
            "Evidence retrieved from a collection of abstracts (not all of it may be relevant):\n"
            f"{evidence}\n\nQuestion: {item.question}"
        )
    raise ValueError(f"unknown condition: {condition}")
