from datetime import datetime
from pytz import timezone
import requests
from bs4 import BeautifulSoup
import telegram

KST = datetime.now(timezone("Asia/Seoul"))

token = "5315161500:AAG3hgkmE30vw3xbElvODcFQQySGWO6FK5A"
id = 5286200749
bot = telegram.Bot(token)

def send(bot_text):
	bot.send_message(chat_id=id, text=bot_text)

url = "https://finance.naver.com/"
response = requests.get(url)
html = response.text

def crawling():
	soup = BeautifulSoup(html, "html.parser")
	
	tbody = soup.select_one("#_topItems2")
	trs = tbody.select("tr")
	datas = []

	num = 1
	for tr in trs:
		stock_name = tr.select_one("th > a").get_text()
		stock_current = tr.select_one("td").get_text()
		stock_upRate = tr.select_one("em.up").get_text()
		stock_link = url + tr.select_one("th > a").get("href")
		datas.append([num, stock_name, stock_current, stock_upRate, stock_link])
		num += 1

	ans = (str(KST)[0:10] + "\n" + str(KST)[11:16] + "의 상승TOP!\n\n")
	for data in datas:
		ans += (str(data[0]) + "위 " + data[1] + " " + data[2] + "원 (" + data[3] + ")\n" + data[4] + "\n")
	return ans

send(crawling())