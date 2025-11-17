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
}

# === TROIS QUESTIONS DIFFÉRENTES ===
questions = [
    "Qu'est-ce que le modèle mistral-large-latest ?",
    "Comment fonctionne le fine-tuning d'un modèle de langage ?",
    "Explique-moi les transformers en IA."
]

# === ASSOCIER CHAQUE QUESTION À UN STYLE ===
styles_associes = ["technique_concis", "humoristique", "tres_concis"]

# === TARIFS ===
PRIX_INPUT_PAR_1M = 0.4  # €
PRIX_OUTPUT_PAR_1M = 2   # €

# === INITIALISATION DU MODÈLE ===
llm = ChatMistralAI(
    model="mistral-small-latest",
    temperature=0.7
)

print("="*70)
print("EXERCICE 5.2 - ESTIMATION DES COÛTS")
print("="*70)

resultats = []

# === UNE REQUÊTE PAR QUESTION ===
for i, question in enumerate(questions):
    nom_style = styles_associes[i]
    message_sys = messages_systeme[nom_style]

    print(f"\n{'='*70}")
    print(f"TEST #{i+1} - Style: {nom_style.upper()}")
    print('='*70)
    print(f"Question : {question}")
    print(f"Message système : {message_sys}")
    print("-"*70)

    # Création du prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", message_sys),
        ("user", "{input}")
    ])
    
    chain = prompt | llm
    result = chain.invoke({"input": question})

    print("\nRÉPONSE :")
    print(result.content)
    
    # Métadonnées
    input_tokens = result.usage_metadata.get('input_tokens')
    output_tokens = result.usage_metadata.get('output_tokens')
    total_tokens = result.usage_metadata.get('total_tokens')

    # Calcul des coûts
    cout_input = (input_tokens / 1_000_000) * PRIX_INPUT_PAR_1M
    cout_output = (output_tokens / 1_000_000) * PRIX_OUTPUT_PAR_1M
    cout_total = cout_input + cout_output

    print("\nMÉTADONNÉES :")
    print(f"Input tokens  : {input_tokens:>6}")
    print(f"Output tokens : {output_tokens:>6}")
    print(f"Total tokens  : {total_tokens:>6}")
        
    print("\nCOÛTS ESTIMÉS :")
    print(f"Coût input    : {cout_input:.8f} €")
    print(f"Coût output   : {cout_output:.8f} €")
    print(f"Coût total    : {cout_total:.8f} €")

    resultats.append({
        "test_num": i+1,
        "style": nom_style,
        "question": question,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
        "cout_input": cout_input,
        "cout_output": cout_output,
        "cout_total": cout_total
    })

    if i < len(questions) - 1:
        print("\nPause de 4 secondes...")
        time.sleep(4)

# === ANALYSE ===
print("\n" + "="*90)
print("ANALYSES")
print("="*90)

total_tokens_cumul = sum(r['total_tokens'] for r in resultats)
cout_total_cumul = sum(r['cout_total'] for r in resultats)

print(f"\nSTATISTIQUES GLOBALES :")
print(f"Nombre de requêtes testées : {len(resultats)}")
print(f"Total tokens consommés      : {total_tokens_cumul}")
print(f"Coût total cumulé           : {cout_total_cumul:.8f} €")
print(f"Coût moyen par requête      : {cout_total_cumul/len(resultats):.8f} €")
