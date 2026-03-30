def get_debater_prompt(topic: str, side: str) -> str:
    return f"""
Eres un debatiente.

Tema:
{topic}

Tu postura:
{side}

Tu tarea:
- Escribe un argumento inicial claro y persuasivo.
- Da entre 2 y 4 razones sólidas.
- Usa ejemplos si ayudan.
- Mantén un tono serio pero natural.
- No uses markdown.
- Máximo 180 palabras.
""".strip()


def get_judge_prompt(topic: str, argument_a: str, argument_b: str) -> str:
    return f"""
Eres un juez imparcial de debates.

Tema:
{topic}

Argumento del debatiente A:
{argument_a}

Argumento del debatiente B:
{argument_b}

Evalúa cuál argumentó mejor en conjunto.

Devuelve SOLO un JSON válido.
No añadas texto antes ni después.
No uses markdown.
No uses bloques de código.

Formato exacto:
{{
  "winner": "A",
  "reason": "explicación breve",
  "scores": {{
    "A": 0,
    "B": 0
  }}
}}

Reglas:
- "winner" debe ser "A", "B" o "EMPATE"
- "scores" debe tener enteros entre 0 y 10
- "reason" debe ser breve y clara
""".strip()


# La dejo por si luego quieres reactivar una segunda ronda
def get_reply_prompt(topic: str, side: str, your_previous_argument: str, opponent_argument: str) -> str:
    return f"""
Eres un debatiente.

Tema:
{topic}

Tu postura:
{side}

Tu argumento anterior:
{your_previous_argument}

Argumento del rival:
{opponent_argument}

Escribe una réplica breve.
- Responde a lo más fuerte del rival.
- Refuerza tu postura.
- No repitas literalmente lo anterior.
- No uses markdown.
- Máximo 120 palabras.
""".strip()