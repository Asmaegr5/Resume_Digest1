import streamlit as st
import pandas as pd
from utils import extract_text_from_pdf, extract_entities, convert_to_row, nlp

st.set_page_config(page_title="CV Analyzer - RH", layout="wide")

# --- Sidebar ---
with st.sidebar:
    st.title("📋 Guide")
    st.markdown("""
    Bienvenue dans l'outil **d'analyse intelligente de CVs**.
    
    ### Étapes :
    1. Charge un ou plusieurs fichiers PDF
    2. Clique sur **Analyser les CVs**
    3. Télécharge le fichier CSV généré
    
    ---  
    """)
    st.info("Modèle NER personnalisé utilisé pour extraire les entités clés.")

# --- Header ---
st.markdown("<h1 style='text-align: center; color: #4B8BBE;'>📄 Outil d'Analyse de CVs RH</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: grey;'>Propulsé par spaCy & Streamlit</h4>", unsafe_allow_html=True)
st.markdown("---")

uploaded_files = st.file_uploader("🚀 Déposez un ou plusieurs CVs en PDF ici :", type="pdf", accept_multiple_files=True)

if st.button("🔍 Analyser les CVs") and uploaded_files:
    data = []
    with st.spinner("🧠 Traitement des fichiers..."):
        for file in uploaded_files:
            text = extract_text_from_pdf(file)
            entities = extract_entities(text, nlp)
            row = convert_to_row(entities)
            data.append(row)

    df = pd.DataFrame(data)

    st.success("✅ Analyse terminée ! Résultat ci-dessous :")
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Télécharger les résultats au format CSV", data=csv, file_name="CVs_analyzes.csv", mime="text/csv")
else:
    st.markdown("**⏳ En attente de fichiers...**")
