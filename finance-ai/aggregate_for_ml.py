import pandas as pd

# Charger
df_users = pd.read_csv("users_profiles.csv")
df = pd.read_csv("transactions.csv")

df["date"] = pd.to_datetime(df["date"])
df["montant"] = pd.to_numeric(df["montant"], errors="coerce")

# Garder uniquement les débits (dépenses)
df_debit = df[df["type"] == "debit"].copy()

# Ajouter colonne "mois"
df_debit["mois"] = df_debit["date"].dt.to_period("M")

# Agrégation par mois et utilisateur
df_monthly = df_debit.groupby(["user_id", "mois"])["montant"].sum().reset_index()
df_monthly.rename(columns={"montant": "depenses_mensuelles"}, inplace=True)

# Fusion avec les profils
df_final = df_monthly.merge(df_users, on="user_id")

# Optionnel : convertir "mois" en string
df_final["mois"] = df_final["mois"].astype(str)

df_final.to_csv("dataset_ml.csv", index=False)
print("Dataset ML final généré - dataset_ml.csv")
