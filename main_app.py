import os
import PyPDF2
from docx import Document
import streamlit as st
from google import genai

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

# Fonction pour interroger le modèle Gemini
def query_gemini(prompt, api_key):
    try:
        # Configuration du client Gemini
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Erreur lors de la requête Gemini : {str(e)}"

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
    col1, col2, col3 = st.columns([1, 6, 1])

    with col1:
        st.image("ketil_media_logo.png", width=100)

    with col3:
        st.image("athling_logo.png", width=140)

    st.title("Assistant commercial Ketil media")
    st.write("Je suis là pour vous aider à rédiger des emails, des recommandations commerciales, et préparer vos rendez-vous.")
    st.info("Version gratuite optimisée pour limiter l'usage des crédits API.")

    # Champ pour la clé API
    api_key = st.text_input("Entrez votre clé API Google Gemini :", type="password")

    # Vérification de la clé API
    if not api_key:
        st.warning("Veuillez entrer votre clé API pour utiliser l'application.")
        return

    # Champ pour entrer la question
    user_input = st.text_area("Posez votre question ou décrivez votre besoin :", "")
    
    if st.button("Envoyer"):
        if user_input.strip():
            # Construire le prompt avec la base de connaissances
            prompt = f"""
            Vous êtes un assistant commercial expert de Ketil Media et Radio Classique.
            Utilisez la "Base de connaissances sur Radio Classique" fournie ci-dessous pour répondre précisément à la "Question utilisateur".
            Si l'information n'est pas dans la base de connaissances, indiquez que vous ne pouvez pas répondre avec les informations disponibles.

            Base de connaissances sur Radio Classique :
            {knowledge_base}
            
            Question utilisateur :
            {user_input}
            """
            # Obtenir la réponse de Gemini
            response = query_gemini(prompt, api_key)
            st.write("### Réponse :")
            st.write(response)
        else:
            st.warning("Veuillez entrer une question ou un besoin.")

if __name__ == "__main__":
    main()
