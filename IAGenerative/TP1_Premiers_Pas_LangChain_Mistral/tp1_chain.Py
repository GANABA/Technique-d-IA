from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_core.runnables import ConfigurableField
import os
from dotenv import load_dotenv
import json

load_dotenv()
os.getenv("MISTRAL_API_KEY")

model = ChatMistralAI(
    model="mistral-large-latest", 
    temperature=0
).configurable_fields(
    temperature=ConfigurableField(
        id = "llm_temperature",
        description = "Température du modèle de langage",
        name="LLM Temperature",
    )
)

prompt = ChatPromptTemplate.from_template(
    """Fais-moi une blague sur le sujet : {sujet}
    
Réponds UNIQUEMENT avec un objet JSON au format suivant :
{{
  "setup": "la question ou le début de la blague",
  "punchline": "la chute de la blague"
}}

N'ajoute AUCUN texte avant ou après le JSON."""
)

json_output_parser = JsonOutputParser()

#output_parser = StrOutputParser()

chain = prompt | model | json_output_parser


print("GÉNÉRATEUR DE BLAGUES")
print("Entrez vos sujets (ligne vide pour terminer)\n")

listeSujets = []
temperatures = [0.0, 0.7]

while True:
    sujet = input(f"Sujet #{len(listeSujets) + 1} : ").strip()

    if not sujet:
        if len(listeSujets) == 0:
            print("Vous devez entrer au moins un sujet !")
            continue
        else:
            break
    
    listeSujets.append(sujet)
    print(f"Sujet ajouté : {sujet}\n")

# === GÉNÉRATION DES BLAGUES ===
print("\n" + "="*60)
print("GÉNÉRATION DES BLAGUES...")
print("="*60 + "\n")

for i, sujet in enumerate(listeSujets, 1):
    print(f"Blague #{i} - Sujet : {sujet}")
    print("-" * 60)
    
    for temp in temperatures:
        print(f"\nTempérature = {temp}")
        print("-" * 60)
        
        reponse = chain.invoke(
            {"sujet": sujet},
            config={"configurable" : {"llm_temperature": temp}}
        )
    
        print(json.dumps(reponse, indent=4, ensure_ascii=False))
    
        #print(f"Setup : {reponse['setup']}")
        #print(f"Punchline : {reponse['punchline']}")
        #print(reponse)
    
    print("\n" + "="*60 + "\n")
