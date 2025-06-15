import sys
import os

# ========================
# ログ出力関数
# ========================
def log_success(message):
    print(f"✅ {message}")

def log_failure(message="続行するには Enter を押してください。"):
    print(f"⚠ {message}")

# ========================
# config読み込み関数
# ========================
def get_config_path(filename="config.json"):
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, filename)

# ========================
# session.json 読み込み関数
# ========================
def get_session_path(filename="session.json"):
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, filename)

# ========================
# 共通: Invite Myself 処理
# ========================
def invite_myself(session, instance_id_full):
    print(f"Invite Myself URL 用 instanceIdFull: {instance_id_full}")
    invite_url = f"https://vrchat.com/api/1/invite/myself/to/{instance_id_full}"
    invite_response = session.post(invite_url, json={})

    print("Invite Status:", invite_response.status_code)
    try:
        print("Invite Response JSON:", invite_response.json())
    except Exception:
        print("Invite Response Text:", invite_response.text)

    if invite_response.status_code in (200, 204):
        log_success("自分自身をインバイトしました！")
    else:
        log_failure(f"インバイト失敗！（Status: {invite_response.status_code}）")

def invite_other(session, instance_id_full, target_user_id):
    print(f"Invite Myself URL 用 instanceIdFull: {instance_id_full}")
    invite_url = f"https://vrchat.com/api/1/invite/{target_user_id}"
    body = {"instanceId": instance_id_full}
    invite_response = session.post(invite_url, json=body)

    print("Invite Status:", invite_response.status_code)
    try:
        print("Invite Response JSON:", invite_response.json())
    except Exception:
        print("Invite Response Text:", invite_response.text)

    if invite_response.status_code == 200:
        log_success(f"{target_user_id} をインスタンスに招待しました！")
    else:
        log_failure(f"インバイト失敗（{invite_response.status_code}）：{invite_response.text}")

                    
                    
                    
