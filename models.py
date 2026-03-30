import os
import time
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise RuntimeError("Falta OPENROUTER_API_KEY en tu .env")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

# Para demo gratis:
# - openrouter/free intenta usar modelos free disponibles
# - openrouter/auto queda como fallback opcional
DEBATER_MODELS = [
    "openrouter/free",
    "openrouter/auto",
]

JUDGE_MODELS = [
    "openrouter/free",
    "openrouter/auto",
]


def _extract_text(response, model: str) -> str:
    if not response or not hasattr(response, "choices") or not response.choices:
        raise RuntimeError(f"El modelo {model} no devolvió choices válidas.")

    message = response.choices[0].message
    if not message or not message.content:
        raise RuntimeError(f"El modelo {model} no devolvió contenido.")

    return message.content.strip()


def call_one_model(prompt: str, model: str, temperature: float = 0.7, max_retries: int = 2) -> str:
    last_error = None

    for attempt in range(max_retries + 1):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature
            )
            return _extract_text(response, model)

        except Exception as e:
            last_error = e
            error_text = str(e).lower()

            # Reintento pequeño si hay rate limit
            if "429" in error_text or "rate limit" in error_text:
                if attempt < max_retries:
                    time.sleep(2 * (attempt + 1))
                    continue

            raise RuntimeError(f"{model}: {e}")

    raise RuntimeError(f"{model}: {last_error}")


def call_model_with_fallback(prompt: str, model_candidates: list[str], temperature: float = 0.7):
    errors = []

    for model in model_candidates:
        try:
            text = call_one_model(prompt, model, temperature=temperature)
            return text, model
        except Exception as e:
            errors.append(str(e))

    joined = " | ".join(errors)
    raise RuntimeError(f"Ningún modelo funcionó. Errores: {joined}")


def generate_argument(prompt: str):
    return call_model_with_fallback(
        prompt=prompt,
        model_candidates=DEBATER_MODELS,
        temperature=0.8
    )


def generate_judgment(prompt: str):
    return call_model_with_fallback(
        prompt=prompt,
        model_candidates=JUDGE_MODELS,
        temperature=0.2
    )