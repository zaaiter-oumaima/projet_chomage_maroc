import os
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Indicateurs de la Banque mondiale (pays : Maroc = MAR)
INDICATEURS = {
    "Chômage total (%)": "SL.UEM.TOTL.ZS",
    "Chômage des jeunes 15-24 (%)": "SL.UEM.1524.ZS",
    "Croissance du PIB (%)": "NY.GDP.MKTP.KD.ZG",
    "Participation des femmes au marché du travail (%)": "SL.TLF.CACT.FE.ZS",
}

def telecharger(code):
    url = f"https://api.worldbank.org/v2/country/MAR/indicator/{code}?format=json&per_page=100"
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    donnees = r.json()[1]
    return pd.Series({int(d["date"]): d["value"] for d in donnees if d["value"] is not None})

df = pd.DataFrame({nom: telecharger(code) for nom, code in INDICATEURS.items()}).sort_index()
df = df.loc[2000:]

os.makedirs("data", exist_ok=True)
df.to_csv("data/chomage_maroc.csv", index_label="annee")
print(df.round(1))

# Graphique 1 : chômage total vs jeunes
fig, ax = plt.subplots(figsize=(10, 5))
df[["Chômage total (%)", "Chômage des jeunes 15-24 (%)"]].plot(ax=ax, marker="o")
ax.set_title("Chômage au Maroc depuis 2000 (Banque mondiale)")
ax.set_xlabel("Année")
ax.set_ylabel("% de la population active")
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("graphique_chomage.png", dpi=150)

# Graphique 2 : croissance du PIB vs chômage
fig, ax = plt.subplots(figsize=(10, 5))
df[["Croissance du PIB (%)", "Chômage total (%)"]].plot(ax=ax, marker="o")
ax.set_title("Croissance du PIB et chômage au Maroc")
ax.set_xlabel("Année")
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("graphique_pib_chomage.png", dpi=150)

print("Terminé ! Regarde les fichiers dans ton dossier.")