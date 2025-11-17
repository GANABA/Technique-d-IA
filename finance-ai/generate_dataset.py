import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ---------------------
# 1. Génération des profils utilisateurs
# ---------------------

def create_user_profile():
    profils = ["etudiant", "jeune_salarie", "fonctionnaire", "independant", "cadre"]
    villes = ["Paris", "Lyon", "Marseille", "Nantes", "Toulouse", "Bordeaux", "Rennes", "Lille"]
    objectifs = ["économiser", "stabiliser", "investir", "acheter_voiture", "acheter_appartement"]

    profil = random.choice(profils)
    city = random.choice(villes)
    objectif_financier = random.choice(objectifs)
    comportement = random.choice(["économe", "normal", "dépensier"])

    # salaires approximatifs
    salaire_base = {
        "etudiant": random.randint(600, 1100),
        "jeune_salarie": random.randint(1700, 2600),
        "fonctionnaire": random.randint(1800, 3000),
        "independant": random.randint(1600, 4500),
        "cadre": random.randint(3000, 7000),
    }[profil]

    loyer_base = {
        "etudiant": random.randint(350, 600),
        "jeune_salarie": random.randint(500, 900),
        "fonctionnaire": random.randint(500, 950),
        "independant": random.randint(600, 1200),
        "cadre": random.randint(900, 1500),
    }[profil]

    # habitudes
    habitudes_sorties = random.randint(50, 300)
    habitudes_courses = random.randint(150, 500)

    return {
        "profil": profil,
        "salaire": salaire_base,
        "loyer": loyer_base,
        "ville": city,
        "objectif_financier": objectif_financier,
        "comportement": comportement,
        "habitudes_sorties": habitudes_sorties,
        "habitudes_courses": habitudes_courses,
    }


# ---------------------
# 2. Génération des transactions
# ---------------------

def generate_transactions_data(num_users=200, num_months=12):
    all_users = []
    all_transactions = []

    categories_courses = {
        "alimentation": (15, 80),
        "restaurant": (15, 50),
        "shopping": (20, 120),
        "transport": (10, 30),
        "loisirs": (12, 60)
    }

    categories_abonnements = {
        "spotify": 9.99,
        "netflix": 13.99,
        "internet": 29.99,
        "portable": 19.99,
    }

    for user_id in range(1, num_users+1):
        user_profile = create_user_profile()
        user_profile["user_id"] = user_id
        all_users.append(user_profile)

        for m in range(num_months):
            current_date = datetime(2024, 1, 1) + timedelta(days=m*30)

            # Dépenses fixes
            all_transactions.append([
                user_id,
                current_date.strftime("%Y-%m-%d"),
                "loyer",
                user_profile["loyer"],
                "debit"
            ])

            for abo_name, abo_price in categories_abonnements.items():
                all_transactions.append([
                    user_id,
                    current_date.strftime("%Y-%m-%d"),
                    f"abo_{abo_name}",
                    abo_price,
                    "debit"
                ])

            # Salaire
            all_transactions.append([
                user_id,
                current_date.strftime("%Y-%m-%d"),
                "salaire",
                user_profile["salaire"],
                "credit"
            ])

            # Dépenses variables
            mult = {"économe": 0.7, "normal": 1.0, "dépensier": 1.5}[user_profile["comportement"]]

            for d in range(random.randint(30, 60)):  # transactions aléatoires
                category = random.choice(list(categories_courses.keys()))
                base_min, base_max = categories_courses[category]
                amount = round(random.uniform(base_min, base_max) * mult, 2)

                tx_date = current_date + timedelta(days=random.randint(0, 28))

                all_transactions.append([
                    user_id,
                    tx_date.strftime("%Y-%m-%d"),
                    category,
                    amount,
                    "debit"
                ])

    df_users = pd.DataFrame(all_users)
    df_transactions = pd.DataFrame(all_transactions, columns=["user_id", "date", "categorie", "montant", "type"])

    df_users.to_csv("users_profiles.csv", index=False)
    df_transactions.to_csv("transactions.csv", index=False)

    print("Fichiers générés : users_profiles.csv et transactions.csv")
    return df_users, df_transactions


# Générer
generate_transactions_data()
