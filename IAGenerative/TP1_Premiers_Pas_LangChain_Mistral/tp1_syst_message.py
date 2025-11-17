from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai.chat_models import ChatMistralAI
from dotenv import load_dotenv
import os
import time

load_dotenv()
os.getenv("MISTRAL_API_KEY")
# === DÉFINITION DES DIFFÉRENTS MESSAGES SYSTÈME ===
messages_systeme = {
    "technique_concis": "Vous êtes un rédacteur de documentation technique de classe mondiale. Fournissez des réponses claires et concises.",
    
    "humoristique": "Vous êtes un rédacteur technique avec un sens de l'humour développé. Expliquez les concepts de manière amusante tout en restant précis.",
    
    "tres_concis": "Répondez en maximum 2 phrases courtes. Soyez ultra-concis.",
    
    "detaille": "Vous êtes un expert technique très précis. Fournissez des explications détaillées, complètes et structurées avec des exemples.",
    
    "vulgarisation": "Vous êtes un vulgarisateur scientifique. Expliquez les concepts techniques comme si vous parliez à un enfant de 10 ans, avec des métaphores simples."
}

# === QUESTION À TESTER ===
question = "Qu'est-ce que le modèle mistral-large-latest ?"

# === INITIALISATION DU MODÈLE ===
llm = ChatMistralAI(
    model="mistral-small-latest",
    temperature=0.7
)

# === TESTE DE CHAQUE VARIANTE ===
print("="*70)
print("TEST DE L'IMPACT DU MESSAGE SYSTÈME")
print("="*70)
print(f"\n Question testée : \"{question}\"\n")

resultats = []

for nom_style, message_sys in messages_systeme.items():
    print("\n" + "="*70)
    print(f"STYLE : {nom_style.upper()}")
    print("="*70)
    print(f"Message système : {message_sys}")
    print("-"*70)
    
    # Création du prompt avec ce message système
    prompt = ChatPromptTemplate.from_messages([
        ("system", message_sys),
        ("user", "{input}")
    ])
    
    # Création de la chaîne
    chain = prompt | llm
    
    result = chain.invoke({"input": question})
        
    print("\nRÉPONSE :")
    print(result.content)
        
    # Métadonnées
    input_tokens = result.usage_metadata.get('input_tokens')
    output_tokens = result.usage_metadata.get('output_tokens')
    total_tokens = result.usage_metadata.get('total_tokens')
        
    # Afficher les statistiques
    print("\nMÉTADONNÉES :")
    print(f"Input tokens  : {input_tokens}")
    print(f"Output tokens : {output_tokens}")
    print(f"Total tokens  : {total_tokens}")
    
    # Délai entre chaque requête pour éviter les erreurs 429
    print("\nPause de 3 secondes...")
    time.sleep(3)