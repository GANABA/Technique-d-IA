# utils/mistral_api.py
import os
from dotenv import load_dotenv

from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage

# Charger les variables d'environnement
load_dotenv()
API_KEY = os.getenv("MISTRAL_API_KEY")

if not API_KEY:
    raise ValueError("ERREUR : la variable d'environnement MISTRAL_API_KEY n'est pas définie.")

# Création du modèle LLM
def get_llm(model_name="mistral-small", temperature=0.3, max_tokens=600):
    """
    Initialise un modèle MistralAI via LangChain.
    """
    return ChatMistralAI(
        model=model_name,
        temperature=temperature,
        max_tokens=max_tokens,
        mistral_api_key=API_KEY,
    )

def call_mistral(prompt, model="mistral-small", temperature=0.3, max_tokens=600):
    """
    Appelle le modèle MistralAI via LangChain et retourne le texte.
    """
    llm = get_llm(model, temperature, max_tokens)

    msg = HumanMessage(content=prompt)
    response = llm.invoke([msg])

    # La réponse est un objet LangChain -> response.content contient le texte
    return response.content
