import tweepy
import requests
import random
from datetime import datetime

API_KEY = "5NOEoDSIIynrIZ2nOHU0JsIBe"
API_SECRET = "mi1UoenQ8DNdjXgCUTU46DY1RcWXHXzXDcjTR2CsMeb48eX74t"
ACCESS_TOKEN = "1988182419917438977-riQLzAEjcq7iZWfTwbN3qfIoRd4IN8"
ACCESS_TOKEN_SECRET = "Hm2eXS3As55gYkcvvhWdfMNpIowrOWSu3HlNAmd0mWVvu"

client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

def get_crypto_prices():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            'ids': 'bitcoin,ethereum,solana',
            'vs_currencies': 'usd',
            'include_24hr_change': 'true'
        }
        response = requests.get(url, params=params, timeout=10)
        return response.json()
    except:
        return None

def get_crypto_news():
    try:
        url = "https://min-api.cryptocompare.com/data/v2/news/?lang=EN"
        response = requests.get(url, timeout=10)
        data = response.json()
        return data.get('Data', [])[:3]
    except:
        return []

def generate_price_alert():
    data = get_crypto_prices()
    if not data:
        return None
    
    btc = data.get('bitcoin', {})
    price = btc.get('usd', 0)
    change = btc.get('usd_24h_change', 0)
    
    emoji = "📈" if change > 0 else "📉"
    direction = "up" if change > 0 else "down"
    
    return f"{emoji} Bitcoin {direction} {abs(change):.1f}% to ${price:,.0f}\n\n#BTC #Bitcoin"

def generate_market_summary():
    data = get_crypto_prices()
    if not data:
        return None
    
    btc = data.get('bitcoin', {}).get('usd', 0)
    eth = data.get('ethereum', {}).get('usd', 0)
    sol = data.get('solana', {}).get('usd', 0)
    
    return f"📊 Market Check\n\nBTC: ${btc:,.0f}\nETH: ${eth:,.0f}\nSOL: ${sol:,.1f}\n\n#Crypto"

def generate_news_tweet():
    news = get_crypto_news()
    if not news:
        return None
    
    title = news[0].get('title', '')
    if len(title) > 200:
        title = title[:197] + "..."
    
    return f"📰 Crypto News\n\n{title}\n\n#CryptoNews"

EVERGREEN_TWEETS = [
    "💡 Bitcoin Fact: Only 21 million BTC will ever exist. Scarcity is built into the protocol.\n\n#Bitcoin",
    "🔐 Security tip: Never share your private keys. Not your keys, not your coins.\n\n#CryptoSecurity",
    "📚 DCA: Investing fixed amounts regularly reduces timing risk.\n\n#Crypto101",
    "⚡ Lightning Network enables instant Bitcoin transactions with minimal fees.\n\n#Bitcoin",
    "🌐 Blockchain = distributed ledger. No single point of failure.\n\n#Crypto",
    "💎 HODL: Hold On for Dear Life. Long-term crypto strategy.\n\n#Bitcoin",
    "📊 Market cap = Price × Supply. How we measure crypto size.\n\n#CryptoEducation",
    "🔍 Always DYOR: Do Your Own Research before investing.\n\n#Crypto",
    "⚠️ Volatility is normal. Never invest more than you can afford to lose.\n\n#CryptoTips",
    "🏦 DeFi: Financial services without traditional banks.\n\n#DeFi"
]

def post_tweet(content):
    try:
        if content:
            client.create_tweet(text=content)
            print(f"✅ Posted: {content[:50]}...")
            return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def run_bot():
    print(f"🤖 Bot starting at {datetime.now()}")
    hour = datetime.now().hour
    
    if hour in [8, 20]:
        tweet = generate_market_summary()
        if tweet:
            post_tweet(tweet)
            return
    
    if hour == 12:
        tweet = generate_news_tweet()
        if tweet:
            post_tweet(tweet)
            return
    
    data = get_crypto_prices()
    if data:
        btc_change = data.get('bitcoin', {}).get('usd_24h_change', 0)
        if abs(btc_change) > 5:
            tweet = generate_price_alert()
            if tweet:
                post_tweet(tweet)
                return
    
    tweet = random.choice(EVERGREEN_TWEETS)
    post_tweet(tweet)

if __name__ == "__main__":
    run_bot()
