AI Finance Coach — Guide rapide

1) Générer le dataset
   - Exécute : python generate_dataset.py
   - Produira : users_profiles.csv et transactions.csv

2) Agréger pour ML
   - Exécute : python aggregate_for_ml.py
   - Produira : dataset_ml.csv

3) Entraîner le modèle
   - Exécute : python train_model.py
   - Produira : model/finance_pipeline.pkl et model/meta.pkl

4) Lancer l'application Streamlit
   - Cd dans le dossier app/ puis :
     streamlit run streamlit_app.py
   - Ou depuis la racine en adaptant les chemins.

5) API LLM
   - Définis ta clé : export MISTRAL_API_KEY="ta_cle"
   - Modifie utils/mistral_api.py si ton fournisseur a un format différent.

Disclaimer :
Ce prototype donne des estimations et des conseils génériques. Il n'est pas un conseil financier professionnel.