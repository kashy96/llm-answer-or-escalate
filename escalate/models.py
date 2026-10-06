"""Thin clients for the models under test.

gemini: Google AI Studio API (needs GEMINI_API_KEY)
ollama: any open model served locally by Ollama (llama3.1, qwen2.5, ...)
"""

import os
import re
import time

import requests


class DailyQuotaExceeded(RuntimeError):
    """The API's per-day request quota is used up; retrying today will not help."""


class Gemini:
    def __init__(self, model, requests_per_minute=None):
        from google import genai

        self.client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
        self.model = model
        # space requests evenly instead of bursting into the per-minute limit
        self.min_interval = 60.0 / requests_per_minute if requests_per_minute else 0.0
        self._last = 0.0

    def generate(self, system, prompt, temperature=0.0):
        from google.genai import types

        wait = self._last + self.min_interval - time.monotonic()
        if wait > 0:
            time.sleep(wait)
        self._last = time.monotonic()

        resp = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system,
                temperature=temperature,
                response_mime_type="application/json",
            ),
        )
        return resp.text or ""


class Ollama:
    def __init__(self, model, host="http://localhost:11434"):
        self.model = model
        self.host = host.rstrip("/")

    def generate(self, system, prompt, temperature=0.0):
        resp = requests.post(
            f"{self.host}/api/chat",
            json={
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt},
                ],
                "stream": False,
                "format": "json",
                "options": {"temperature": temperature},
            },
            timeout=300,
        )
        resp.raise_for_status()
        return resp.json()["message"]["content"]


def build(spec):
    provider = spec["provider"]
    if provider == "gemini":
        return Gemini(spec["model"], spec.get("requests_per_minute"))
    if provider == "ollama":
        return Ollama(spec["model"], spec.get("host", "http://localhost:11434"))
    raise ValueError(f"unknown provider: {provider}")


def with_retries(call, attempts=6, wait=2.0, max_wait=120.0):
    for i in range(attempts):
        try:
            return call()
        except Exception as exc:  # rate limits, timeouts, dropped connections
            message = str(exc)
            if "PerDay" in message:
                raise DailyQuotaExceeded(message) from exc
            if i == attempts - 1:
                raise
            # use the server's own "retry in Ns" hint when it gives one
            hint = re.search(r"retry in ([0-9.]+)s", message)
            delay = float(hint.group(1)) + 1 if hint else wait * 2**i
            delay = min(delay, max_wait)
            print(f"    request failed ({exc.__class__.__name__}), retrying in {delay:.0f}s")
            time.sleep(delay)
