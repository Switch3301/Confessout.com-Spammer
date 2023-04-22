from tls_client import Session
from bs4 import BeautifulSoup
import random
from threading import Thread
from colorama import Fore
import os
from datetime import datetime

sent = 0
failed = 0
errors = 0


__threads__ = 100

def title():
    os.system('title Confessout Spammer - Sent {} - Failed {} - Errors - {} - Threads {}'.format(sent,failed,errors,__threads__))

os.system('cls' if os.name == 'nt' else 'clear')

__API__ = 'https://www.confessout.com/sendMessage'
__proxies__ = 'proxies.txt'


@staticmethod
def format_message(message):
    messagef =  str(message) + ' |.gg/switchuwu |' + str(random.randint(0,99))
    return messagef

@staticmethod
def GetFormattedProxy(filename):
    proxy = random.choice(open(filename, encoding="cp437").read().splitlines()).strip()
    if '@' in proxy:
        return proxy
    elif len(proxy.split(':')) == 2:
        return proxy
    else:
        if '.' in proxy.split(':')[0]:
            return ':'.join(proxy.split(':')[2:]) + '@' + ':'.join(proxy.split(':')[:2])
        else:
            return ':'.join(proxy.split(':')[:2]) + '@' + ':'.join(proxy.split(':')[2:])


class Main:
    def __init__(self,username,message)-> None:
        self.message = message
        self.username = username.replace('https://www.confessout.com/','').strip()     
        self.url = 'https://www.confessout.com/{}'.format(self.username)
        self.session = Session(client_identifier='chrome110')
        self.headers = {
            'authority': 'www.confessout.com',
            'method': 'GET',
            'path': '/{}'.format(self.username),
            'scheme': 'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.8',
            'sec-ch-ua': '"Chromium";v="112", "Brave";v="112", "Not:A-Brand";v="99"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'sec-gpc': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
        }

        s = self.session.get(self.url, headers=self.headers,proxy = f'http://{GetFormattedProxy(__proxies__)}')
        try:
            XSRF_TOKEN  = s.cookies.get('XSRF-TOKEN')
            laravel_session = s.cookies.get('laravel_session')
            self.cookies = 'XSRF-TOKEN={}; laravel_session={}'.join(XSRF_TOKEN,laravel_session)
        except:
            self.cookies = ''

        self.token = BeautifulSoup(s.text, 'html.parser').find('input', {'name': '_token'})['value']



    def confess(self,thread_num):
        global sent,failed,errors
        data = f'_token={self.token}&reciever={self.username}&message={self.message}'
        headers = {
            'authority': 'www.confessout.com',
            'method': 'POST',
            'path': '/sendMessage',
            'scheme': 'https',
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.8',
            'content-length': str(len(data)),
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'cookie': self.cookies,
            'origin': 'https://www.confessout.com',
            'referer': self.url,
            'sec-ch-ua': '"Chromium";v="112", "Brave";v="112", "Not:A-Brand";v="99"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
        }
        s = self.session.post(__API__, data=data, headers=headers,proxy = f'http://{GetFormattedProxy(__proxies__)}')
        if s.headers['Location'] == 'https://www.confessout.com/signup?message=sent':
            print(Fore.LIGHTBLACK_EX + f'[THREAD {thread_num}] ' +  Fore.RESET + Fore.WHITE + ' Successfully posted message' + Fore.RESET)
            sent+=1
        elif s.status_code == 200:
            print(Fore.LIGHTBLACK_EX + f'[THREAD {thread_num}] ' +  Fore.RESET + Fore.WHITE + ' Successfully posted message' + Fore.RESET)
            sent+=1
        else:
            print(Fore.LIGHTRED_EX + f'[THREAD {thread_num}] ' +  Fore.RESET + Fore.WHITE + 'Failed to Post message' + Fore.RESET)
            failed +=1


def main(username,message,thread_number):
    try:
        message = format_message(message)
        kuni = Main(username = username,message=message)
        kuni.confess(thread_num = thread_number)
        title()
    except Exception as e:
        print(e)
        errors +=1
        title()
    

message = 'Hello baby'
username = 'fukiwubdi'

def loop(i):
    if len(str(i)) == 1:
        i = '0' + str(i)
    while True:
        main(username = username,message=message,thread_number=i)

for i in range(__threads__):
    Thread(target = loop,args=(i,)).start()


