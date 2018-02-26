#python 2
import urllib2,cookielib #  resquest website
import pandas as pd
from bs4 import BeautifulSoup
site='http://ru.investing.com/economic-calendar/'

hdr = {'User-Agent': 'Chrome/23.0.1271.64'}

req = urllib2.Request(site, headers=hdr)
page = urllib2.urlopen(req)

content = page.read()
soup = BeautifulSoup(content, "html.parser")
table = soup.find('table', {"id": "economicCalendarData"})
tbody = table.find('tbody')
rows = tbody.findAll('tr', {"class": "js-event-item"})
result=[]

def parse_invest(bulls):
    for tr in rows:
      news = {'time':None, 'country':None, 'impact':None, 'url':None, 'name':None,'actual':None}
      news['time']=tr.attrs['data-event-datetime']
      cols = tr.find('td', {"class": "flagCur"})
      flag = cols.find('span')
      news['country'] = flag.get('title')
      impact = tr.find('td', {"class": "sentiment"})
      bull = impact.findAll('i', {"class": "grayFullBullishIcon"})
      news['impact'] = len(bull)
      event = tr.find('td', {"class": "event"})
      a = event.find('a')
      news['url'] = "http://ru.investing.com" + a['href']
      news['name'] = a.text.strip()
      bold = tr.find('td', {"class": "bold"})
      news['actual'] = bold.text.strip()
      if len(bull) >= bulls  :#select bull
       result.append(news)
    return(result)

df=parse_invest(2)
table=pd.DataFrame(df)
print table

table.to_csv("C://Users/a.bittaraev/PycharmProjects/table.csv", encoding= "utf-8", sep=";", index=True)







