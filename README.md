# Texto → ODS · Bonus del microproyecto 2

## Modelo distribuido en fragmentos

En este repositorio el archivo del modelo se distribuye en cuatro fragmentos `modelo_ods.part00` a `modelo_ods.part03` para respetar el limite de carga web por archivo. La aplicación los reúne en memoria y verifica la huella SHA-256 antes de cargarlo. Los bytes y las predicciones son iguales al archivo `modelo_ods.joblib` exportado del notebook; no son cuatro modelos. Deben descargarse o actualizarse los cuatro fragmentos juntos. No es necesario conservar el archivo completo junto a ellos.

Aplicación de Johan Piraneque y Jose Florez. Recibe texto libre y aplica el pipeline completo exportado de V3: TF-IDF, SVD y clasificador seleccionado por validación cruzada.

## Ejecutar

En un entorno nuevo Python 3.12, desde esta carpeta:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

No se necesita Excel, NLTK ni reentrenamiento en el servidor. Las stopwords se conservan en el vectorizador serializado. No cargue archivos Joblib de terceros.

## Publicar en Streamlit Community Cloud

1. Subir el contenido de esta carpeta a un repositorio GitHub autorizado, incluyendo `modelo_ods.joblib`, `metadata.json` y `requirements.txt`.
2. Iniciar sesión en la cuenta propia de Streamlit y conectar GitHub.
3. Create app: seleccionar el repositorio y rama reales, y `app.py` como archivo principal. Seleccionar Python 3.12 en Advanced settings.
4. Desplegar y probar desde una ventana sin sesión si se requiere acceso público. Comprobar texto vacío, texto válido y cuatro ejemplos.
5. Registrar la URL en la entrega y conservar evidencia visual. No declarar despliegue terminado solo por superar pruebas locales.

Si se usa una subcarpeta del repositorio, indicar su ruta en el archivo principal. No subir los datos del curso, credenciales o secretos. Revisar la visibilidad del repositorio antes de publicarlo. El archivo del modelo debe mantenerse por debajo del límite GitHub de 100 MB; si lo supera, acordar otra distribución antes de desplegar.

## Limitaciones

Solo ODS 1–16; el conjunto no tiene ODS 17. Predicción monoclase y orientativa. Las métricas agregadas no son confianza individual. No se guardan textos ni se consultan servicios externos de IA, pero los textos viajan al servidor de alojamiento.

## Reexportar

Ejecutar V3 completo desde su carpeta, con `streamlit-ods/app.py` presente. La sección 11 exporta el pipeline ganador, fija versiones y compara todas las predicciones test. Sustituir juntos modelo, ficha y dependencias en el repositorio tras validar.

Documentación: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy
