# autolaunch.py

import requests
import json
import sys
from utils import log_success, log_failure, get_config_path, get_session_path, invite_myself, invite_other

# --- 設定ファイル読み込み ---
config_path = get_config_path()

try:
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
except FileNotFoundError:
    log_failure(f"設定ファイルが見つかりません: {config_path}")
    exit(1)

# --- セッション情報読み込み ---
session_path = get_session_path()

try:
    with open(session_path, "r", encoding="utf-8") as f:
        session_data = json.load(f)
except FileNotFoundError:
    log_failure("session.json が見つかりません！ まず save_session.py を実行してください。")
    exit(1)

# --- セッション作成 ---
session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Content-Type": "application/json"
})
session.cookies.set("auth", session_data["auth"], domain="vrchat.com")

# userId取得
r = session.get("https://vrchat.com/api/1/auth/user")
user_info = r.json()
userId = user_info.get("id")

# --- インスタンスごとに処理 ---
instances = config.get("instances", [])

for idx, instance in enumerate(instances, 1):
    # --- インスタンス作成処理 ---
    print(f"\n=== {idx} 件目のインスタンスを作成します ===")

    # --- 共通パラメータ ---
    worldId = instance.get("worldId")
    region = instance.get("region", "jp")
    instanceType = instance.get("instanceType")

    # --- post_data 構築 ---
    post_data = {
        "worldId": worldId,
        "region": region,
    }

    # --- 自身にインバイトを送るのか、他者に送るのか判定 ---
    if instance.get("userId"):
        #もし自身のIdと違うIdが指定されていたら
        if instance.get("userId") != userId:
            should_invite_other = True
            target_user_id = instance.get("userId")
        else:
            should_invite_other = False
            target_user_id = userId
    #定義が無いなら自身にインバイト
    else:
        should_invite_other = False
        target_user_id = userId

    # --- group, group+の場合 ---
    if instanceType in ["group", "group+"]:
        post_data["type"] = "group"
        post_data["ownerId"] = instance.get("groupId")
        for opt_key in ("queueEnabled", "ageGate"):
            val = instance.get(opt_key)
            if val is not None:
                post_data[opt_key] = val
        
        roleids = []
        if instanceType in ["group"]:
            log_success("Group インスタンスを作成します！")
            post_data["groupAccessType"] = "members"

            # --- Groupの場合のみ、rolenamesからroleIdsを取得する ---
            
            roleNames = instance.get("roleNames", [])
            groupId = instance.get("groupId")

            group_info_url = f"https://vrchat.com/api/1/groups/{groupId}?includeRoles=true&purpose=other"
            group_response = session.get(group_info_url)

            if group_response.status_code != 200:
                log_failure(f"Group 情報取得失敗！（Status: {group_response.status_code}）")
                sys.exit(1)

            group_json = group_response.json()
            roles = group_json.get("roles", [])

            if roleNames:
                log_success(f"指定された roleNames → roleIds を取得します: {roleNames}")
                for role in roles:
                    if role["name"] in roleNames:
                        roleids.append(role["id"])

                if not roleids:
                    log_failure("指定された roleNames に該当する roleIds が見つかりませんでした！")
                    sys.exit(1)
                else:
                    log_success(f"roleNames → roleIds 変換成功！: {roleids}")
            else:
                # roleNames 未指定 → すべての roleIds を入れる！
                log_success("roleNames 未指定 → 全 roleIds を追加します。")
                for role in roles:
                    roleids.append(role["id"])
                log_success(f"全 roleIds: {roleids}")
        # --- group+ 処理 ---
        else:
            log_success("Group+ インスタンスを作成します！")
            post_data["groupAccessType"] = "plus"
            

        post_data["roleIds"] = roleids

    # --- group, group+以外の場合 ---
    else:
        if instanceType != "public":
            post_data["ownerId"] = userId
        
        if instanceType == "invite+":
            post_data["type"] = "private"
            post_data["canRequestInvite"] = True
        if instanceType == "invite":
            post_data["type"] = "private"
        elif instanceType == "friends":
            post_data["type"] = "friends"
        elif instanceType == "friends+":
            post_data["type"] = "hidden"
        elif instanceType == "public":
            post_data["type"] = "public"

    # --- インスタンス作成 ---
    response = session.post("https://vrchat.com/api/1/instances", json=post_data)

    print("Status:", response.status_code)
    try:
        response_json = response.json()
        print("Response JSON:", response_json)
    except Exception:
        print("Response Text:", response.text)
        response_json = {}

    if response.status_code in (401, 403):
        log_failure("セッションが無効または期限切れです。")
        print("対処法：save_session.py を再実行して新しいセッションを保存してください。")
        sys.exit(1)
    elif response.status_code in (200, 201):            
        log_success("インスタンス作成成功！")
    else:
        log_failure(f"インスタンス作成失敗！（Status: {response.status_code}）")
        sys.exit(1)

    # --- 招待処理
    log_success("招待処理開始")

    # --- instance_id_full取得
    instance_id_full = response_json.get("id")
    if not instance_id_full:
        log_failure("インスタンスIDが取得できませんでした！")
        sys.exit(1)

    if should_invite_other:
        invite_other(session, instance_id_full, target_user_id)
    else:
        invite_myself(session, instance_id_full)
    
    print(instance_id_full)
    
print("\n✅ すべてのインスタンス立上げが完了しました！")
input("終了します。ウィンドウを閉じてください。")
sys.exit()