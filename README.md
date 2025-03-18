# **📌 Datathon GFC - Asistente para Resúmenes Evolutivos**

## 🏥 **Descripción del Reto**
### *Creación de un asistente para la elaboración de resúmenes evolutivos para pacientes hospitalizados*

El objetivo de este reto es desarrollar un **asistente basado en inteligencia artificial** que automatice la generación de **resúmenes evolutivos** de pacientes hospitalizados al momento del alta médica.  
Esto permitirá reducir la carga administrativa del personal sanitario y mejorar la calidad y estandarización de los informes clínicos.  

---

## 🧹 **Limpieza de Datos**

Lo primero que hicimos fue limpiar los datos de los archivos CSV, aplicando los conocimientos adquiridos en una asignatura que estamos cursando:

- 📄 **`resumen_evolución.csv`**: Se reemplazaron los valores `NA` por ceros.  
- 💊 **`resumen_medicación.csv`**: Se unificaron las unidades de medida, estableciendo que `1 U = 1 gramo`.  
- 🗂️ **`resumen_notas.csv`**: Se normalizó el formato de fecha para mantener consistencia en todos los registros.  

---

## 📂 **Estructura del Proyecto**
El proyecto se ejecuta en **VSCode** y cuenta con el siguiente directorio raíz:  

📁 **`datathon_gfc/`**  

### 🗂️ **Carpetas y Archivos**
- 📂 `csvs/` → Contiene los archivos de datos proporcionados.  

### 📜 **Código fuente:**
- 📝 **`conversation.py`** → Interpreta la pregunta y genera una respuesta.  
- 📊 **`data_loader.py`** → Carga los datos desde los archivos CSV.  
- 🔍 **`query_handler.py`** → Busca en los datos según la pregunta del usuario.  
- 🛠 **`utils.py`** → Funciones de utilidad para limpieza, formateo y extracción de palabras clave.  
- 🚀 **`main.py`** → Archivo principal que gestiona la interacción con el usuario y coordina los módulos anteriores.  
- 💬 **`interfaz_gui.py`** → Interfaz gráfica basada en Flet para visualizar los mensajes tipo WhatsApp.  
🔗  **`api_client.py`**  → Concecta con la API

---

## ⚙️ **Instalación y Configuración**
### 📌 **Requisitos Previos**
- 🐍 **Python 3.x**  
- 📦 **pip**  
- 🔹 *Recomendado:* Uso de un **entorno virtual** para gestionar dependencias.  

### 💻 **Creación del Entorno Virtual**
#### 🖥️ **macOS/Linux:**
```bash
python3 -m venv myenv
source myenv/bin/activate

#### 🖥️ **Windows:**
python -m venv mi_entorno_w
.\mi_entorno_w\Scripts\Activate.ps1
.\entornAlma\Scripts\Activate.ps1

📦 Instalación de Dependencias
pip install pandas spacy openai langchain flet
python -m spacy download es_core_news_sm

🚀 Ejecución del Asistente
python main.py

🎨 Ejecución de la Interfaz Gráfica
descargar FLET:  pip install flet
ALMA: descargar pip install flet-desktop
abrir INTERFAZ: python3 asistente_gui.py



