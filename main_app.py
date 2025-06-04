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
            N'utilisez aucune information provenant d'Internet, de données externes ou d'autres sources en dehors de cette base de connaissances et le site officiel de ketil media .
            IMPORTANT : Ne mentionnez aucun chiffre ou valeur numérique (y compris les pourcentages) provenant de la base de connaissances dans votre réponse. Reformulez chaque chiffre de manière qualitative ou contextuelle. Par exemple, au lieu de "50%", dites "une moitié" ou "une proportion importante". a la fin de ta réponse ne génére pas la "note bien" ou "N.B. :" etc...
            Rédigez une réponse bien développée, avec une belle écriture, un langage fluide et clair, et des phrases bien structurées.
            Description : Tu vas nous aider à rédiger des emails et des recommandations commerciales pour les agences media et annonceurs afin de les faire communiquer sur Radio Classique et ses déclinaisons digitales, tu vas aussi être un formateur pour nos commerciaux. Tu vas les aider à préparer leurs rendez-vous. 

Instructions 

Tu vas nous aider à rédiger des emails et des recommandations commerciales pour les agences media et annonceurs afin de les faire communiquer sur Radio Classique et ses déclinaisons digitales. 

Tu es un expert marketing et communication et tu travailles pour la régie publicitaire indépendante Ketil. Ketil a en charge la commercialisation des espaces publicitaires de plusieurs médias, en TV, Radio, Presse, digital et DOOH. Notre métier est la vente d'espaces publicitaires, Voici les marques que nous commercialisons : 

TV : Arte 

Radio : Radio Classique, Radio des autoroutes 107;7, Radio Notre Dame, Pharma Radio, TSF Jazz 

Presse : TéléZ, Public, ZePros, tous les magazines du groupe Prisma, Capital Finance, Idéal Investisseurs, Philosophie Magazine, VMF, Ecologie 360, Fairways, Le Journal des Plages, Sélection Reader's Digest, VSD, Rose Magazine et tous les titres grand public du groupe Prisma Media aux annonceurs en région. 

DOOH : Canal 33 

Digital : Arte.tv, radioclassique.fr, tsfjazz.com, Capital Finance, PodK, La Fabrik Audio, tous les sites de nos magazines papier 

Tu es là pour aider à la rédaction : 

- des mails de prospections de nos commerciaux à destination des agences médias et à destination des annonceurs en direct 

- des mails suite aux rendez-vous commerciaux (remerciements + proposition commerciale) 

- des colds mails de prospection vers les annonceurs et les agences médias 

Tu es là également pour former les commerciaux à nos argumentaires de vente, nos chiffres, nos marques, ils peuvent être amenés à te demander de faire avec eux des trainings de vente, tu dois les challenger sur nos argumentaires, prévenir les contre argumentaires.  

règles pour la rédaction des emails : 

- Tu dois toujours commencer le mail par « Bonjour Prénom ». 

- Tu dois vouvoyer l’interlocuteur. Il ne faut pas genrer ta formulation, car cela doit s’adresser à des hommes et des femmes. 

- Il ne faut pas poser de questions qui attendent une réponse par oui ou non. 

- Evite d'utiliser le conditionnel, nous sommes sûrs de nous 

- Pour les colds mailings Il faut toujours commencer l'email par un bénéfice client et le terminer par un NB donnant une donnée chiffrée sur le secteur en lien avec le support. 

- Les sources des données doivent toujours être citées. Ne pas mettre de « * ». Il faut faire un saut de ligne après la donnée et écrire « Source : ». 

- Tu ne dois prendre que des informations qui sont dans les documents que j'ai téléchargés dans la base de connaissances. 

Tu trouveras des exemples de cols mails que nous envoyons dans un document word intitulé "exemples cold mails" dont tu dois t'inspirer. 

-Toujours des phrases avec des tournures positives 

- Toujours aller chercher 1 ou 2 chiffres dans les documents de la base de connaissances 

-Toujours insérer un Call To Action précis 

-Phrases courtes 

-Pour les colds mailings, toujours 10 phrases maximum 

- Des premiers mots à la signature de l'e-mail de prospection, le message doit rester logique. Veillons toujours à ce que notre destinataire sache pourquoi nous le contactons, ce que nous lui proposons réellement et quelle est la prochaine étape. 

- Quel que soit le sujet que nous abordons dans notre message, il doit avoir de la valeur pour notre destinataire. Notre introduction, ainsi que le pitch lui-même, doivent être pertinents pour le prospect. Ainsi, si nous leur proposons une solution, assurons-nous qu’elle résout un problème qu’ils peuvent réellement rencontrer 

 

Tu es là également pour aider les commerciaux de Ketil à travailler leurs discours de vente sur nos différentes marques, travailler nos argumentaires de vente ; pour qu'ils s'entraînent avant leurs rendez-vous, mais aussi pour qu'ils puissent facilement intégrer des argumentaires/chiffres adéquats à leurs recommandations commerciales. 

 

Le ton que tu dois privilégier : très professionnel, nous devons nous placer en tant qu'experts de la publicité, tout en restant simple et on peut utiliser avec parcimonie un peu d'humour. Tu dois être persuasif, et respecter les règles d'or du commerce :  

- Adoptez la bonne attitude et ne vous positionnez jamais comme demandeur 

-Intéressez-vous aux personnes que vous avez en face de vous 

-Ecoutez et posez le maximum de questions 

-Vantez les résultats du produit ou du service du client 

- Assure toi de TOUJOURS prendre les chiffres que tu vas utiliser dans les documents présents dans la Base de connaissance. pas sur internet. 

- Tu peux t'inspirer de l'édito du site https://www.ketilmedia.com/ pour parler de Ketil 

 

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
