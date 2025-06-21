import requests
import time
# import json
from datetime import datetime
from colorama import Fore, Style, init
import os


def clear_screen():
    # 判断系统类型
    if os.name == 'nt':  # Windows系统
        os.system('cls')
    else:  # Mac和Linux系统
        os.system('clear')


init(autoreset=True)


# 查询票的状态
def fetch_ticket_status(api_url, api_headers):
    response = requests.get(api_url, headers=api_headers)
    if response.status_code == 200:
        data = response.json()
        if data['code'] == 0:
            tickets = data['data']['screen_list']
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n当前时间: {current_time}")
            table = []
            for screen in tickets:
                for ticket in screen['ticket_list']:
                    status = ticket['sale_flag']['display_name']
                    if status != "不可售" and status != "已售罄" and status != "暂时售罄":
                        status = Fore.RED + status
                    if ticket['desc'] == "普通票":
                        table.append([ticket['screen_name'] + f"普通票\t\t", status])
                    else:
                        table.append([ticket['screen_name'] + ticket['desc'], status])

            # 计算每列的最大宽度
            max_desc_len = max(len(row[0]) for row in table)
            max_status_len = max(len(row[1]) for row in table)

            # 打印表头
            header = f"{Fore.CYAN}{'票种'.ljust(max_desc_len)}{'状态'.ljust(max_status_len)}{Style.RESET_ALL}"
            print(header)
            print('-' * len(header))

            # 打印表格内容
            for row in table:
                desc = Fore.YELLOW + row[0].ljust(max_desc_len) + Style.RESET_ALL
                status = Fore.GREEN + row[1].ljust(max_status_len) + Style.RESET_ALL
                print(f"{desc}\t{status}")
        else:
            print(f"Error: {data['msg']}")
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")


url = "https://show.bilibili.com/api/ticket/project/getV2?version=134&id=102194"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

while True:
    fetch_ticket_status(url, headers)
    time.sleep(1)
    # clear_screen()
