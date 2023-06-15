from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon import functions, types
import random
import os
import time


def get_proxies(filename):
    with open(filename, 'r') as f:
        proxies = [line.strip() for line in f]
    return proxies

def join_chanels(content,choice,proxies):
    accounts_list = []
    if choice == "1":
        print('Выбран приватный метод')
        link=str(input("Введите ссылку на канал (без https://t.me/):"))
        for i, proxy in zip(content, proxies):
            proxy = proxy.split(':')
            with TelegramClient(i['session_name'], i['session_app_id'], i['session_app_hash']) as client:
                print(client)
                result = client(functions.messages.ImportChatInviteRequest(
                    hash=link
                ),proxy = (socks.HTTP,proxy[0],proxy[1], True, proxy[2],proxy[3]))
                res = result.stringify()
                if res == 'True':
                    print(f'Аккаунт {i["session_name"]} зашел на {link}')
                    accounts_list.append(
                        {
                            "session_name":i["session_name"],
                            "session_app_id":i['session_app_id'], 
                            "session_app_hash":i['session_app_hash'],
                            "proxy": proxy
                        }
                        )
                    time.sleep(15)
                else:
                     print(f'Аккаунт не {i["session_name"]} зашел на {link}')
                
    if choice == "2":
        print('Выбран публичный метод')
        link=str(input("Введите ссылку на канал (без https://t.me/):"))
        for i, proxy in zip(content, proxies):
            proxy = proxy.split(':')
            with TelegramClient(i['session_name'], i['session_app_id'], i['session_app_hash']) as client:
                print(client)
                result = client(functions.channels.JoinChannelRequest(
                    channel=link
                ),proxy = (socks.HTTP,proxy[0],proxy[1], True, proxy[2],proxy[3]))
                res = result.stringify()
                if res == 'True':
                    print(f'Аккаунт {i["session_name"]} зашел на {link}')
                    accounts_list.append(
                        {
                            "session_name":i["session_name"],
                            "session_app_id":i['session_app_id'], 
                            "session_app_hash":i['session_app_hash'],
                            "proxy": proxy
                        }
                        )
                    time.sleep(15)
                else:
                     print(f'Аккаунт не {i["session_name"]} зашел на {link}')
    
    return accounts_list

def get_messages() -> list:
    with open(os.path.join(os.path.dirname(os.path.relpath(__file__)), 'messages.txt'), 'r') as fp:
        messages = fp.readlines()
    return messages


def send_report(content):
    messages = get_messages()
    target=str(input("Введите название канала: "))
    for i in content:
        proxy = i['proxy'].split(':')
        msg = random.choice(messages).strip()
        with TelegramClient(i['session_name'], i['session_app_id'], i['session_app_hash']) as client:
            result = client(functions.account.ReportPeerRequest(
                peer=target,
                reason=types.InputReportReasonOther(),
                message=msg
            ),proxy = (socks.HTTP,proxy[0],proxy[1], True, proxy[2],proxy[3]))
            print(result)
            time.sleep(8)


list_files = []
content_acc = []
text_input_path = str(input('Введите путь до файлов с аккаунтами: '))

dir_list = os.listdir(text_input_path)
for x in dir_list:
    if x.endswith('.json'):
        list_files.append(x)

for file_list in list_files:
    with open(os.path.join(text_input_path, file_list), 'r') as fp:
        session_string = json.load(fp)
        session_name = session_string['session_file']
        session_app_id = session_string['app_id']
        session_app_hash = session_string['app_hash']
        session_proxy = session_string['proxy']
        content_acc.append(
            {
             "session_name":session_name,
             "session_app_id":session_app_id,
             "session_app_hash":session_app_hash,
            }
            )

acc = []
proxies = get_proxies('proxy.txt')
join_choice=str(input("Выберите вход в ТГ канал: 1 - приватный, 2 - публичный: "))
acc = join_chanels(content_acc,join_choice,proxies)
send_report(acc)



