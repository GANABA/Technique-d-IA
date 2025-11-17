from langchain_mistralai.chat_models import ChatMistralAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import os

load_dotenv()
os.getenv("MISTRAL_API_KEY")
llm = ChatMistralAI(
    model="mistral-large-latest",
    temperature=0.7,
    # api_key="..."  # facultatif si vous utilisez la variable d'environnement
)

message = HumanMessage(content="Invente un nom original pour un café spatial et explique pourquoi ce nom est pertinent.")
response = llm.invoke([message])

print(response.content)

print(f"Tokens utilisés : {response.usage_metadata}")

# Calcul du coût (tarifs Mistral Medium 3 par M tokens)
PRIX_INPUT_PAR_1M = 0.4 #€
PRIX_OUTPUT_PAR_1M = 2  #€

cout_input = (response.usage_metadata.get("input_tokens") / 1_000_000) * PRIX_INPUT_PAR_1M
cout_output = (response.usage_metadata.get("output_tokens") / 1_000_000) * PRIX_OUTPUT_PAR_1M
cout_total = cout_input + cout_output

print(f"\nCoût approximatif :")
print(f"Coût input  : {cout_input:.6f} €")
print(f"Coût output : {cout_output:.6f} €")
print(f"Coût total  : {cout_total:.6f} €")
