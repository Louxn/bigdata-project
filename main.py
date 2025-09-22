import os
import time
import random
import pandas as pd
from datetime import datetime
from scripts.reddit import create_reddit_client, search_subreddit

# Fichier CSV principal
csv_file = "data/raw/reddit_posts.csv"

# 1. Vérifier si le fichier existe
if os.path.exists(csv_file):
    print(f"📂 Le fichier {csv_file} existe déjà. Chargement des posts existants...")
    df = pd.read_csv(csv_file)
    print(f"✅ {len(df)} posts chargés depuis le CSV.")
else:
    print("🚀 Fichier CSV introuvable. Lancement de la collecte des posts Reddit...")

    # Créer le client Reddit
    reddit = create_reddit_client()

    # Subreddits et mots-clés
    subreddits = ["investing", 
    "stocks", 
    "wallstreetbets", 
    "cryptocurrency", 
    "bitcoin", 
    "solana",
    "ethtrader", 
    "finance", 
    "stockmarket", 
    "teslainvestorsclub",
    "teslainvestors",
    "apple",
    "applestock",
    "amazon",
    "amazonstock",
    "microsoft",
    "techstocks",
    "nvidia",
    "google",
    "facebook",
    "financeinvestments", 
    "stocktrading",        
    "moneytalks",
    "financialindependence",
    "investing_news"]
    keywords = ["stock market", "financial markets", "investing", "stocks", "equities", "bonds", "capital markets", "trading",
    "dividends", "bull market", "bear market", "market volatility", "recession", "inflation", "interest rates", "capital gains",
    "risk management", "portfolio", "asset management", "fundamental analysis", "technical analysis", "value investing",
    "growth investing", "dividend investing", "day trading", "swing trading", "investment strategy", "stock picking", 
    "short selling", "margin trading", "volatility index", "financial independence", "long-term investment", "tax on investments",
    "Tesla stock", "Tesla motors", "Tesla earnings", "Elon Musk", "Tesla share price", "Tesla investment", "Tesla future", 
    "Tesla Model 3", "Tesla Cybertruck", "Tesla production", "Apple stock", "Apple earnings", "iPhone sales", "Apple dividend", 
    "Apple innovation", "Apple future", "Apple growth", "Tim Cook", "Apple market share", "Apple revenue", "Amazon stock", 
    "Amazon earnings", "Amazon prime", "Amazon growth", "AWS", "Jeff Bezos", "Amazon revenue", "Amazon future", "Microsoft stock",
    "Microsoft earnings", "Microsoft cloud", "Azure", "Microsoft future", "Bill Gates", "Microsoft growth", "Microsoft revenue", 
    "NVIDIA stock", "NVIDIA earnings", "NVIDIA GPUs", "NVIDIA stock split", "NVIDIA AI", "NVIDIA future", "Google stock", 
    "Alphabet stock", "Google earnings", "Google revenue", "Google search", "Google cloud", "Alphabet future", "Google AI", 
    "Google advertising", "Facebook stock", "Meta stock", "Facebook earnings", "Facebook advertising", "Meta future", "Facebook growth", 
    "Mark Zuckerberg", "Meta platforms", "Bitcoin", "Ethereum", "cryptocurrency", "blockchain", "DeFi", "NFTs", "altcoins", "stablecoins", 
    "cryptocurrency investment", "crypto market", "Bitcoin mining", "cryptocurrency regulation", "Bitcoin price", "Ethereum price", 
    "altcoins investment", "economic downturn", "global recession", "government stimulus", "trade war", "Federal Reserve", 
    "interest rate hike", "quantitative easing", "market crash", "US dollar", "inflation rate", "economic growth", "GDP growth", 
    "unemployment rate", "central bank policy", "global trade", "interest rates cut", "fiscal policy", "monetary policy", 
    "federal reserve chair", "US economy", "growth stocks", "value stocks", "blue-chip stocks", "small-cap stocks", "mid-cap stocks", 
    "penny stocks", "index funds", "ETFs", "mutual funds", "REITs", "commodities", "precious metals", "real estate investments", 
    "ESG investing", "impact investing", "emerging markets", "sector ETFs", "investment strategy", "asset allocation", "diversification",
    "long-term investment", "risk tolerance", "portfolio management", "financial planning", "retirement planning", "investment advisor",
    "financial advisor", "tax strategy", "estate planning", "financial independence", "wealth management", "crowd psychology", 
    "social trading", "economic indicators", "market sentiment", "technical indicators", "earnings report", "quarterly results", 
    "stock split", "IPO", "merger and acquisition", "corporate earnings", "dividend payout", "buyback program", "earnings guidance", 
    "market correction", "stock upgrade", "stock downgrade", "market speculation", "Solana", "SOL", "BTC", "ETH"]

    # Liste pour stocker tous les posts
    all_posts = []

    # Collecte des posts
    for subreddit in subreddits:
        for keyword in keywords:
            print(f"🔍 Recherche de '{keyword}' dans r/{subreddit}...")
            try:
                posts = search_subreddit(reddit, subreddit, keyword, limit=50)
                for post in posts:
                    post["subreddit"] = subreddit
                    post["keyword"] = keyword
                all_posts.extend(posts)
                time.sleep(random.uniform(2, 5))  # pause pour éviter rate limit
            except Exception as e:
                print(f"⚠️ Erreur sur r/{subreddit} avec '{keyword}' : {e}")
                time.sleep(10)

    # Créer dossier data/raw si nécessaire
    os.makedirs("data/raw", exist_ok=True)

    # Convertir en DataFrame et supprimer doublons
    df = pd.DataFrame(all_posts)
    df.drop_duplicates(subset="id", inplace=True)

    # Sauvegarder le CSV principal
    df.to_csv(csv_file, index=False, encoding="utf-8")
    print(f"✅ {len(df)} posts collectés et sauvegardés dans {csv_file}")


# ========================
# 📊 ANALYSE DES SENTIMENTS
# ========================

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Télécharger le lexique (une seule fois)
nltk.download('vader_lexicon')

# Initialiser l'analyseur
sia = SentimentIntensityAnalyzer()

# Assurer que les colonnes sont bien en string (évite NaN -> float)
df['title'] = df['title'].fillna("").astype(str)
df['selftext'] = df['selftext'].fillna("").astype(str)

# Fonction pour analyser le sentiment d'un texte
def get_sentiment(text):
    if not isinstance(text, str) or text.strip() == "":
        return 0.0
    return sia.polarity_scores(text)['compound']

# Appliquer sur les colonnes 'title' et 'selftext'
df['sentiment_title'] = df['title'].apply(get_sentiment)
df['sentiment_selftext'] = df['selftext'].apply(get_sentiment)

# Score global = moyenne des deux
df['sentiment_overall'] = df[['sentiment_title','sentiment_selftext']].mean(axis=1)

# ========================
# 📊 ANALYSE / VISUALISATION
# ========================

print("🔎 Aperçu des posts avec sentiment :")
print(df[['title', 'subreddit', 'keyword', 'sentiment_overall']].head(10))

print("\n📈 Statistiques globales des sentiments :")
print(df['sentiment_overall'].describe())

print("\n📊 Moyenne du sentiment par subreddit :")
print(df.groupby('subreddit')['sentiment_overall'].mean().sort_values(ascending=False))

print("\n📊 Moyenne du sentiment par mot-clé :")
print(df.groupby('keyword')['sentiment_overall'].mean().sort_values(ascending=False))

# Histogramme
import matplotlib.pyplot as plt

plt.hist(df['sentiment_overall'], bins=20, edgecolor='black')
plt.title("Distribution des scores de sentiment")
plt.xlabel("Sentiment (-1 = négatif, +1 = positif)")
plt.ylabel("Nombre de posts")
plt.show()

# Sauvegarde du CSV enrichi
output_file = "data/raw/reddit_posts_with_sentiment.csv"
df.to_csv(output_file, index=False, encoding="utf-8")
print(f"\n✅ Fichier enrichi sauvegardé : {output_file}")

