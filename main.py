"""B站票务查询工具
功能：查询B站活动余票状态并通知
版本：Ver_0.0.2
"""

import time
from datetime import datetime
import requests
from colorama import Fore, Style, init


def clear_screen(enable=True):
    """清空控制台屏幕"""
    if enable:
        print("\033c", end="")


def fetch_ticket_status(api_url, api_headers):
    """查询票务状态并显示结果"""
    try:
        response = requests.get(api_url, headers=api_headers, timeout=10)
        response.raise_for_status()

        data = response.json()
        if data['code'] != 0:
            print(Fore.RED + f"API返回错误: {data['msg']}" + Style.RESET_ALL)
            return False

        tickets = data['data']['screen_list']
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n当前时间: {current_time}")
        print(f"当前所查询的项目名称是: {data['data']['name']}\n")

        table = []
        for screen in tickets:
            for ticket in screen['ticket_list']:
                status = ticket['sale_flag']['display_name']
                if status not in ["不可售", "已售罄", "暂时售罄"]:
                    status = Fore.RED + status + Style.RESET_ALL

                desc = ticket['screen_name'] + \
                       ("普通票" if ticket['desc'] == "普通票" else ticket['desc'])
                table.append([desc, status])

        # 计算列宽并打印表格
        if table:
            max_desc_len = max(len(row[0]) for row in table)
            max_status_len = max(len(row[1]) for row in table)

            header = f"{Fore.CYAN}{'票种'.ljust(max_desc_len)}" \
                     f"{'状态'.ljust(max_status_len)}{Style.RESET_ALL}"
            print(header)
            print('-' * len(header))

            for desc, status in table:
                print(f"{Fore.YELLOW}{desc.ljust(max_desc_len)}{Style.RESET_ALL}\t{status}")
        else:
            print(Fore.YELLOW + "未找到票务信息" + Style.RESET_ALL)

        return True

    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"网络请求失败: {str(e)}" + Style.RESET_ALL)
        return False


def get_user_settings():
    """获取用户配置"""
    user_config_defalut = {
        'project_id': '102194',  # 默认项目ID
        'query_interval': 3,  # 默认查询间隔(秒)
        'retry_interval': 5,  # 失败后重试间隔(秒)
        'enable_clear': False,  # 默认关闭清屏
        'headers': {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/58.0.3029.110 Safari/537.36"
        }
    }
    print(f"{Fore.CYAN}=== B站票务查询工具配置 ===")
    user_config_defalut['project_id'] = input(f"请输入项目ID(默认:{user_config_defalut['project_id']}): ") or user_config_defalut['project_id']

    try:
        interval = input(f"请输入查询间隔(秒，默认:{user_config_defalut['query_interval']}): ")
        user_config_defalut['query_interval'] = int(interval) if interval else user_config_defalut['query_interval']
    except ValueError:
        print(Fore.RED + "无效输入，使用默认值" + Style.RESET_ALL)

    # 用户选择是否开启清屏
    clear_input = input("是否开启清屏功能？(y/n，默认:n): ").lower()
    user_config_defalut['enable_clear'] = clear_input == 'y'

    return user_config_defalut


def main(config):
    """主程序"""
    init(autoreset=True)
    if config['enable_clear']:
        clear_screen(True)  # 初始清屏（仅当用户启用时）

    print(f"{Fore.CYAN}=== B站票务查询工具 ===")
    api_url = f"https://show.bilibili.com/api/ticket/project/getV2?version=134&id={config['project_id']}"

    try:
        while True:
            if not fetch_ticket_status(api_url, config['headers']):
                print(Fore.YELLOW + f"将在{config['retry_interval']}秒后重试..." + Style.RESET_ALL)
                time.sleep(config['retry_interval'])
                continue

            print(f"\n{Fore.GREEN}下次查询将在 {config['query_interval']} 秒后开始...{Style.RESET_ALL}")
            time.sleep(config['query_interval'])
            clear_screen(config['enable_clear'])  # 根据用户设置决定是否清屏

    except KeyboardInterrupt:
        print(f"\n{Fore.CYAN}程序已手动终止{Style.RESET_ALL},正在关闭程序。")
        time.sleep(1.5)  # 添加1.5秒延迟


if __name__ == "__main__":
    print("当前版本号:Ver_0.0.2。")
    user_config = get_user_settings()
    main(user_config)
