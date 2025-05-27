import openai
import os
import PyPDF2
from docx import Document
import streamlit as st
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

# Fonction pour extraire le texte des fichiers PDF
def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, "rb") as f:
        pdf_reader = PyPDF2.PdfReader(f)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

# Fonction pour extraire le texte des fichiers Word
def extract_text_from_word(file_path):
    document = Document(file_path)
    text = ""
    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"
    return text

# Fonction pour interroger gpt-4o-mini
def query_gpt4(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Utiliser gpt-4o-mini ou un autre modèle supporté si vous avez de crédit gpt-4.1
            messages=[
                {"role": "system", "content": "Tu es un assistant commercial pour Ketil media."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500,  # Limiter le nombre de tokens pour économiser des crédits
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Erreur lors de la requête : {str(e)}"

# Chargement des documents et construction de la base de connaissances
def load_documents():
    base_knowledge = ""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(script_dir, "base de connaissance")
    
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Le dossier '{folder_path}' n'existe pas.")
    
    files = os.listdir(folder_path)
    
    for file in files:
        file_path = os.path.join(folder_path, file)
        try:
            if file.endswith(".pdf"):
                base_knowledge += extract_text_from_pdf(file_path) + "\n"
            elif file.endswith(".docx"):
                base_knowledge += extract_text_from_word(file_path) + "\n"
        except Exception as e:
            print(f"Erreur lecture fichier {file_path}: {e}")
    
    return base_knowledge


# Initialisation de la base de connaissances
knowledge_base = load_documents()
# Application Streamlit
def main():
    # Disposition des logos avec des colonnes
    col1, col2, col3 = st.columns([1, 6, 1])  # Colonnes avec des proportions égales

    with col1:
        st.image("ketil_media_logo.png",  width=100)  # Logo de Ketil Media (à gauche)

    with col3:
        st.image("athling_logo.png",  width=140)  # Logo d'Athling (à droite)

    st.title("Assistant commercial Ketil media")
    st.write("Je suis là pour vous aider à rédiger des emails, des recommandations commerciales, et préparer vos rendez-vous.")
    st.info("Version gratuite optimisée pour limiter l'usage des crédits OpenAI.")

    # Champ pour entrer la question
    user_input = st.text_area("Posez votre question ou décrivez votre besoin :", "")
    
    if st.button("Envoyer"):
        if user_input.strip():
            # Construire le prompt avec la base de connaissances
            prompt = f"""
            Base de connaissances sur Radio Classique :
            {knowledge_base}
            
            Question utilisateur :
            {user_input}
            """
            # Obtenir la réponse de GPT-4
            response = query_gpt4(prompt)
            st.write("### Réponse :")
            st.write(response)
        else:
            st.warning("Veuillez entrer une question ou un besoin.")

if __name__ == "__main__":
    main()