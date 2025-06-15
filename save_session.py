# save_session.py

import requests
import json
import getpass
import sys
from utils import log_success, log_failure, get_config_path, get_session_path

# --- config.json 読み込み ---
config_path = get_config_path()

try:
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
except FileNotFoundError:
    log_failure(f"設定ファイルが見つかりません: {config_path}")
    exit(1)

# --- ユーザー名・パスワード取得 ---
username = config.get("username", "")
password = config.get("password", "")

if not username:
    username = input("VRChat Username: ")

if not password:
    password = getpass.getpass("VRChat Password: ")

# --- セッション作成 ---
session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Content-Type": "application/json"
})

# --- 認証 ---
from requests.auth import HTTPBasicAuth

response = session.get(
    "https://vrchat.com/api/1/auth/user",
    auth=HTTPBasicAuth(username, password)
)

if response.status_code != 200:
    log_failure(f"ログイン失敗: {response.status_code} {response.json()}")
    exit(1)

# --- 2FA チェック ---
if response.json().get("requiresTwoFactorAuth", False):
    print("2FA required!")
    twofa_code = input("Enter 2FA TOTP code: ")
    verify_resp = session.post(
        "https://vrchat.com/api/1/auth/twofactorauth/totp/verify",
        json={"code": twofa_code}
    )
    if not verify_resp.json().get("verified", False):
        log_failure("2FA 認証失敗！")
        exit(1)
    else:
        log_success("2FA 認証成功！")

# --- セッション保存 ---
session_cookie = session.cookies.get("auth")
if not session_cookie:
    log_failure("auth Cookie 取得失敗")
    exit(1)

session_data = {
    "username": username,
    "auth": session_cookie
}

session_path = get_session_path()

with open(session_path, "w", encoding="utf-8") as f:
    json.dump(session_data, f)

log_success(f"セッション保存完了！ ({session_path})")

input("終了します。ウィンドウを閉じてください。")
sys.exit()