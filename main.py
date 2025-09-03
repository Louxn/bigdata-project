import os
import pandas as pd
from scripts.reddit import create_reddit_client, search_subreddit

# 1. Créer une instance du client Reddit
reddit = create_reddit_client()

# 2. Définir les subreddits et mots-clés pour la recherche
subreddits = [
    "investing", 
    "stocks", 
    "wallstreetbets", 
    "personalfinance", 
    "cryptocurrency", 
    "bitcoin", 
    "solana",
    "solanacryptocurrency",
    "ethtrader", 
    "finance", 
    "stockmarket", 
    "teslamotors",
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

keywords = [
    "stock market", "financial markets", "investing", "stocks", "equities", "bonds", "capital markets", "trading",
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
    "market correction", "stock upgrade", "stock downgrade", "market speculation", "Solana", "SOL", "BTC", "ETH"
]

# 3. Liste pour stocker tous les posts récupérés
all_posts = []

# 4. Lancer la recherche dans chaque subreddit avec les mots-clés définis
for subreddit in subreddits:
    for keyword in keywords:
        print(f"🔍 Recherche de '{keyword}' dans r/{subreddit}...")
        posts = search_subreddit(reddit, subreddit, keyword, limit=50)
        
        # Ajouter le subreddit et le mot-clé à chaque post
        for post in posts:
            post["subreddit"] = subreddit
            post["keyword"] = keyword
            
        # Ajouter les posts à la liste globale
        all_posts.extend(posts)

# 5. Créer le dossier pour les fichiers CSV si il n'existe pas
os.makedirs("data/raw", exist_ok=True)

# 6. Sauvegarder les posts récupérés dans un fichier CSV
df = pd.DataFrame(all_posts)
df.to_csv("data/raw/reddit_posts.csv", index=False, encoding="utf-8")

print(f"✅ {len(df)} posts sauvegardés dans data/raw/reddit_posts.csv")
