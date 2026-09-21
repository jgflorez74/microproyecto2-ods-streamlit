from pathlib import Path
import hashlib
import json
import io
import joblib
import streamlit as st

st.set_page_config(page_title="Texto → ODS", page_icon="🌍", layout="centered")
BASE = Path(__file__).resolve().parent
NOMBRES = {
    1: "Fin de la pobreza", 2: "Hambre cero", 3: "Salud y bienestar",
    4: "Educación de calidad", 5: "Igualdad de género",
    6: "Agua limpia y saneamiento", 7: "Energía asequible y no contaminante",
    8: "Trabajo decente y crecimiento económico", 9: "Industria, innovación e infraestructura",
    10: "Reducción de las desigualdades", 11: "Ciudades y comunidades sostenibles",
    12: "Producción y consumo responsables", 13: "Acción por el clima",
    14: "Vida submarina", 15: "Vida de ecosistemas terrestres",
    16: "Paz, justicia e instituciones sólidas", 17: "Alianzas para lograr los objetivos",
}


@st.cache_resource
def cargar_modelo(huella):
    # Solo cargamos el artefacto propio; Joblib no es seguro para archivos desconocidos.
    archivo = BASE / "modelo_ods.joblib"
    # Los fragmentos permiten subir por la interfaz web sin alterar el modelo.
    datos = archivo.read_bytes() if archivo.exists() else b"".join(
        (BASE / f"modelo_ods.part{i:02d}").read_bytes() for i in range(4))
    if hashlib.sha256(datos).hexdigest() != huella:
        raise ValueError("La huella del modelo no coincide con su ficha.")
    return joblib.load(io.BytesIO(datos))


st.title("Del texto al desarrollo sostenible")
st.caption("Microproyecto 2 · Johan Piraneque y Jose Florez · Bonus Streamlit")
st.write("Escribe un texto en español para identificar el ODS que le asigna nuestro modelo.")
try:
    ficha = json.loads((BASE / "metadata.json").read_text(encoding="utf-8"))
    modelo = cargar_modelo(ficha["sha256"])
except (OSError, ValueError, ImportError, KeyError):
    st.error("No se pudo cargar el modelo. Revisa los archivos exportados y requirements.txt.")
    st.stop()

st.info("Cobertura: ODS 1–16. No podemos identificar ODS 17 porque no está representado en los datos de entrenamiento.")
with st.form("clasificar"):
    texto = st.text_area("Texto para analizar", height=180, max_chars=10000,
                         placeholder="Por ejemplo: La comunidad necesita acceso a agua potable y servicios de saneamiento.")
    enviado = st.form_submit_button("Identificar ODS", type="primary")
if enviado:
    # Estas validaciones impiden clasificar entradas sin informacion util.
    # No normalizamos manualmente: el pipeline mantiene las transformaciones de V2.
    if not texto.strip():
        st.warning("Escribe un texto antes de continuar.")
    elif len(texto) > 10000:
        st.warning("El texto debe tener como máximo 10.000 caracteres.")
    elif modelo.named_steps["tfidf"].transform([texto]).nnz == 0:
        st.warning("No encontramos vocabulario conocido. Prueba con una descripción en español más detallada.")
    else:
        # Predict aplica TF-IDF, SVD y el clasificador ya ajustados, sin reentrenar.
        ods = int(modelo.predict([texto])[0])
        st.success(f"ODS {ods} · {NOMBRES[ods]}")
        st.caption("Predicción orientativa, no una decisión definitiva. Un texto puede relacionarse con varios ODS, pero el modelo devuelve uno.")

with st.expander("Cómo funciona y cuáles son sus límites"):
    st.write(f"Pipeline: TF-IDF → SVD ({ficha['componentes']} componentes) → {ficha['modelo']}.")
    st.write(f"Evaluación en {ficha['n_test']} textos reservados: accuracy {ficha['accuracy_test']:.4f}; F1-macro {ficha['f1_macro_test']:.4f}.")
    st.write("Estas métricas describen el conjunto test, no la confianza en el texto ingresado. No mostramos probabilidades porque los márgenes de LinearSVC no están calibrados.")
    st.write("Puede fallar con textos ambiguos, muy cortos, de otros idiomas o de temas distintos al entrenamiento. Recomendamos revisión humana.")
st.divider()
st.caption("Privacidad: esta aplicación no guarda los textos ni los envía a una API de IA. En la versión web, el texto se procesa en el servidor de Streamlit. No ingreses información personal o confidencial.")
