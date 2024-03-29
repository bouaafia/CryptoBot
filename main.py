import requests
import os
import telebot
from telebot import types

TOKEN = "" # Your bot token
API_URL = 'https://api.coingecko.com/api/v3'
last_known_prices = {}
# Go to Newsapi.com and get an api
NEWS_API_KEY = "" # Your APIKEY
users = []

adminId = 6037113802
bot = telebot.TeleBot(TOKEN)
def getnews():
    url = f'https://newsapi.org/v2/everything?q=crypto&sortBy=publishedAt&apiKey={NEWS_API_KEY}'
    response = requests.get(url)
    data = response.json()
    articles = data.get('articles', [])
    if articles:
        news_list = []
        for article in articles[:5]:  
            news_list.append(f"<b>{article['title']}</b>\n{article['description']}\nRead more: {article['url']}")
        return '\n\n'.join(news_list)
    else:
        return "Sorry, no news available at the moment."
@bot.message_handler(commands=['start'])
def start(message):
    welcomemsg = (
        "👋 Welcome to CryptoBot!\n\n"
        "I'm here to provide you with the latest cryptocurrency news, coin prices, and more.\n\n"
        "To get started, use the following commands:\n"
        "/news - Get the latest cryptocurrency news\n"
        "/price - Get the current price and info of a cryptocurrency \n"
        "/help - Learn more about the available commands"
    )
    if message.chat.id not in users :
        users.append(message.chat.id)
        bot.send_message(chat_id= adminId , text=f"New User Join Us ! \nUser : {len(users)}")
    bot.send_message(message.chat.id, welcomemsg)
def getcoinnfo(coin):
    url = f'{API_URL}/coins/{coin}'
    response = requests.get(url)
    data = response.json()
    if 'error' not in data:
        coin_name = data['name']
        coin_symbol = data['symbol'].upper()
        market_data = data['market_data']
        current_price = market_data['current_price']['usd']
        market_cap = market_data['market_cap']['usd']
        volume_24h = market_data['total_volume']['usd']
        circulating_supply = market_data['circulating_supply']
        total_supply = market_data['total_supply']
        return (coin_name, coin_symbol, current_price, market_cap, volume_24h, circulating_supply, total_supply)
    else:
        return None
@bot.message_handler(commands=['info'])
def price(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    coins = ['bitcoin', 'ethereum', 'ripple', 'litecoin', 'cardano', 'dogecoin', 'polkadot', 'stellar', 'chainlink', 'bitcoin-cash', 'binancecoin', 'tether', 'monero', 'cosmos', 'tron', 'nem', 'vechain', 'ethereum-classic', 'theta-token', 'dash', 'neo', 'zcash', 'maker', 'compound', 'crypto-com-chain', 'omisego', 'aave', 'sushi', 'waves', 'huobi-token', 'leo-token', 'ftx-token', 'compound-ether']
    btns = [types.InlineKeyboardButton(coin.capitalize(), callback_data=coin) for coin in coins]
    markup.add(*btns)
    messageid = bot.send_message(message.chat.id, "Select a cryptocurrency:", reply_markup=markup)
    @bot.callback_query_handler(func=lambda call: True)
    def handle_button_click(call):
        
        coin = call.data
        coin_info = getcoinnfo(coin)
        print(coin_info)
        if coin_info:
            coin_name, coin_symbol, current_price, market_cap, volume_24h, circulating_supply, total_supply = coin_info
            info_message = (
                f"*{coin_name} ({coin_symbol})*\n"
                f"💰 Current Price: ${current_price}\n"
                f"📊 Market Cap: ${market_cap}\n"
                f"📈 24h Volume: ${volume_24h}\n"
                f"🌐 Circulating Supply: {circulating_supply}\n"
                f"🔢 Total Supply: {total_supply}\n\n"
                f"For more information, visit [CoinGecko](https://www.coingecko.com/en/coins/{coin})"
            )
            bot.edit_message_text(text=info_message , chat_id=call.message.chat.id  , parse_mode='Markdown' , message_id=messageid.id)
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, text=f"Sorry, I couldn't find the information for {coin}." , message_id=messageid.id)
@bot.message_handler(commands=['news'])
def news(message):
    news = getnews()
    bot.send_message(message.chat.id, news , parse_mode="HTML")
@bot.message_handler(commands=['help'])
def help(message):
    help_message = (
        "Here are the available commands:\n\n"
        "/news - Get the latest cryptocurrency news\n"
        "/info - Get the current info of a cryptocurrency\n"
        "/help - Learn more about the available commands"
    )
    bot.send_message(message.chat.id, help_message)
bot.infinity_polling()
