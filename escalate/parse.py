import json
import re

LABELS = ("yes", "no", "maybe")


def parse(text):
    """Pull (answer, confidence, ok) out of a model reply.

    Confidence is returned on a 0-1 scale. `ok` is False when the reply was not
    the JSON we asked for; the answer is then recovered from the first
    yes/no/maybe in the text and the confidence is None.
    """
    match = re.search(r"\{.*?\}", text or "", re.S)
    if match:
        try:
            obj = json.loads(match.group(0))
            answer = str(obj.get("answer", "")).strip().lower()
            conf = float(obj.get("confidence"))
            if answer in LABELS:
                # we ask for 0-100, but some models reply with a fraction
                if conf > 1 or conf == int(conf):
                    conf /= 100
                return answer, min(max(conf, 0.0), 1.0), True
        except (ValueError, TypeError):
            pass
    words = re.findall(r"\b(yes|no|maybe)\b", (text or "").lower())
    return (words[0] if words else "maybe"), None, False
