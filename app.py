import json
import streamlit as st

from prompts import get_debater_prompt, get_judge_prompt
from models import generate_argument, generate_judgment

st.set_page_config(page_title="LLM Debate Judge", layout="wide")
st.title("Debate entre LLMs con juez automático")

st.write(
    "Introduce un tema y deja que dos LLMs generen argumentos opuestos. "
    "Luego un tercer paso actúa como juez."
)


def extract_json_block(text: str):
    text = text.strip()

    # Caso ideal: ya es JSON puro
    try:
        return json.loads(text)
    except Exception:
        pass

    # Intento de rescate si el modelo mete texto extra
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        candidate = text[start:end + 1]
        return json.loads(candidate)

    raise ValueError("No se pudo extraer JSON válido.")


topic = st.text_input(
    "Tema del debate",
    placeholder="Ej: ¿La IA destruirá más empleo del que crea?"
)

side_a = st.text_input("Postura A", value="A favor")
side_b = st.text_input("Postura B", value="En contra")

show_raw = st.checkbox("Mostrar salida cruda del juez", value=False)

if st.button("Generar debate"):
    if not topic.strip():
        st.warning("Escribe un tema antes de generar el debate.")
        st.stop()

    try:
        with st.spinner("Generando argumentos..."):
            prompt_a = get_debater_prompt(topic, side_a)
            prompt_b = get_debater_prompt(topic, side_b)

            a1, model_a = generate_argument(prompt_a)
            b1, model_b = generate_argument(prompt_b)

        with st.spinner("Generando veredicto..."):
            judge_prompt = get_judge_prompt(topic, a1, b1)
            judge_raw, judge_model = generate_judgment(judge_prompt)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Debatiente A")
            st.write(f"**Modelo:** {model_a}")
            st.write(f"**Postura:** {side_a}")
            st.write(a1)

        with col2:
            st.subheader("Debatiente B")
            st.write(f"**Modelo:** {model_b}")
            st.write(f"**Postura:** {side_b}")
            st.write(b1)

        st.subheader("Veredicto del juez")
        st.write(f"**Modelo juez:** {judge_model}")

        try:
            parsed = extract_json_block(judge_raw)
            st.json(parsed)
        except Exception:
            st.warning("El juez no devolvió JSON limpio.")
            st.code(judge_raw)

        if show_raw:
            st.subheader("Salida cruda del juez")
            st.code(judge_raw)

    except Exception as e:
        st.error(f"Error al generar el debate: {e}")