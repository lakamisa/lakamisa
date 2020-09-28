#Author: Chatchawal Sangkeettrakarn
#Date: September 20,2020.

from fastapi import FastAPI
import uvicorn
import numpy as np
import re
import requests
from bs4 import BeautifulSoup
from fastapi.responses import PlainTextResponse
import math

app = FastAPI()

def result(res):
    return {"result":res}

@app.get("/")
async def main():
    return 'Hello World'

@app.get("/test")
async def test():
    return 'Test Tutorial'

@app.get("/add")
async def add(a: int = 0, b: int = 0):
    return a+b

@app.get("/mul")
async def mul(a: int = 0, b: int = 0):
    return a*b


def tonumlist(li):
    ls = li.split(',')
    for i in range(len(ls)):
        ls[i] = float(ls[i])
    return list(ls)

@app.get("/asc")
async def asc(li):
    ls = tonumlist(li)
    ls.sort()
    return ls

@app.get("/desc")
async def desc(li):
    ls = tonumlist(li)
    ls.sort(reverse=True)
    return ls

@app.get("/sum")
async def sum(li):
    ls = tonumlist(li)
    return np.sum(np.array(ls))

@app.get("/avg")
async def avg(li):
    ls = tonumlist(li)
    return np.average(ls)

@app.get("/mean")
async def mean(li):
    ls = tonumlist(li)
    return np.mean(ls)

@app.get("/max")
async def max(li):
    ls = tonumlist(li)
    return np.amax(ls)

@app.get("/min")
async def min(li):
    ls = tonumlist(li)
    return np.amin(ls)

@app.get("/pow")
async def pow(a: int = 0, b: int = 0):
    return math.pow(a,b)



@app.get("/muti2")
async def muti2(li):
    ls = tonumlist(li)
    sum = 1
    for i in ls :
        a = i
        sum = sum * a
        
    return sum


@app.get("/ascii")
async def ascii(li):
    sumword = ""
    for i in li :
        word = hex(ord(i))+","
        sumword = sumword + word
    return sumword



@app.get("/validation-ctzid")
async def validation_ctzid(text):
    if(len(text) != 13):
        return False
    
    sum = 0
    listdata = list(text)
    
    for i in range(12):
        sum+=int(listdata[i])*(13-i)
        
    d13 = sum%11
            
    d13 = 1 if d13==0 else 0 if d13==1 else 11-d13
    
    if d13==int(listdata[12]):
        return True
    else:
        return False

@app.get("/validation-email")
async def validation_email(text):  
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if re.search(regex,text):
        return True
    else:
        return False
    
    
@app.get("/google-search",response_class=PlainTextResponse)
def google_search(text):
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:81.0) Gecko/20100101 Firefox/81.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    #url = 'https://www.google.com/search?q=' + str(text) + '&biw=1396&bih=657&dpr=1.38'
    url = 'https://www.google.com/search?q=' + str(text) + '&source=lmns&tbm=vid&bih=657&biw=1396&hl=en&sa=X&ved=2ahUKEwjAw_POxIvsAhVBXpQKHRrUBjQQ_AUoAnoECAEQAg'
    res = requests.get(url, headers = headers)
    soup = BeautifulSoup(res.content, 'html.parser')
    
    t = soup.findAll('div', {'class':"r"})
    i = 0
    result = ''
    for a in t:
        href = a.a['href']
        head = a.h3.text
        result = result + head + '<br>' + href + '<br><br>'
        i += 1
        if(i >= 5):
            break
    
    return(result)


@app.get("/youtube-search",response_class=PlainTextResponse)
def youtube_search(text):
    
    headers = {
        # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:81.0) Gecko/20100101 Firefox/81.0',
        # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        # 'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate',
        # 'DNT': '1',
        # 'Connection': 'keep-alive',
        # 'Upgrade-Insecure-Requests': '1'
        
        #'method': 'GET,path: /',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,th-TH;q=0.8,th;q=0.7',
        'cache-control': 'max-age=0',

        # 'sec-fetch-dest': 'document',
        # 'sec-fetch-mode': 'navigate',
        # 'sec-fetch-site': 'none',
        # 'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
        #'x-client-data': 'CJK2yQEIprbJAQjEtskBCKmdygEImbXKAQisx8oBCPXHygEI58jKAQjpyMoBCKzJygEItMvKAQiQzsoBCNnXygEYxMDKAQ=='
    }
    url = 'https://www.youtube.com/results?search_query=' + str(text)
    res = requests.get(url, headers = headers)
    soup = BeautifulSoup(res.content, 'html.parser')
    
    t = soup.findAll('div', {'class':"r"})
    i = 0
    result = ''
    for a in t:
        href = a.a['href']
        head = a.h3.text
        result = result + head + '<br>' + href + '<br><br>'
        i += 1
        if(i >= 5):
            break
    
    return(result)


if __name__ == '__main__':
   uvicorn.run(app, host="0.0.0.0", port=80, debug=True) 
