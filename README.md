# VRChat Instance AutoLaunch

このツールは、**VRChatのインスタンスをブラウザ操作なしで自動生成&インバイト**できるユーティリティです。  
複数のワールドを一括で立ち上げて、任意のユーザーにインバイトを送ることも可能です🚀

---

## 🛠 構成ファイル
- `config.json` … 投稿内容の設定ファイル
- `session.json` … VRChatの認証セッション情報（`save_session.exe`で作成）
- `save_session.exe` … 事前処理（VRChatにログインしてセッション情報を取得）
- `autolaunch.exe` … メイン処理（投稿処理）

---

## 📌 使い方
1. **`vrc-instance-autolaunch-v*.*.zip` をダウンロードし、解凍。→最新版(https://github.com/hamikuma/vrc-instance-autolaunch/releases/latest)**
2. **`save_session.exe` を実行してVRChatにログインし、`session.json` を作成**
3. **`config.json` を編集し、起動するインスタンスの情報を設定**
4. **`autolaunch.exe` を実行 → VRChatのインスタンスが自動作成されます！**

---

## 📝 `config.json` の設定項目

`config.json` を編集して、立ち上げるインスタンスの内容を設定してください。
`config.json` に既に記載している内容を参考に書き換えてください。以下詳細説明です。

※userId、worldId、groupIdは、VRChat公式(https://vrchat.com/)の各ページのURLに含まれているので、その値を入力してください。

(共通パラメータ)
| **キー** | **内容** | **備考** |
|---------|---------|---------|
| `"username"` | ログインユーザーネーム | 空白なら実行時に入力可能です |
| `"password"` | ログインパスワード | 空白なら実行時に入力可能です |
| `"userId"` | ユーザーID | 自分ではなく他者をinviteする場合は記載してください。例: `"usr_xxxxxxxx-yyyy-zzzz-aaaa-bbbbbbbbbbbb"` |
| `"worldId"` | worldのID | 例: `"wrld_xxxxxxxx-yyyy-zzzz-aaaa-bbbbbbbbbbbb"` |
| `"instanceType"` | インスタンスタイプ | 'group+'、'group'、'friend+'、'friend'、'invite+'、'invite'、'public'のいずれかを指定 |
| `"region"` | リージョン | 'jp'、'usw' など |

(instanceTypeが'group+'または'group'の際に有効なパラメータ)
| **キー** | **内容** | **備考** |
|---------|---------|---------|
| `"groupId"` | グループID | 例: `"grp_xxxxxxxx-yyyy-zzzz-aaaa-bbbbbbbbbbbb"` |
| `"role_names"` | ロールの制限(group時にさらに特定ロールに絞りたい場合) | `"Group Owner"` 、 `"Member"` などをカンマ区切りで入力|
| `"ageGate"` | 年齢制限をかける | `true` or `false` (年齢認証済のuserでなければ立上げ失敗するので注意) |
| `"queueEnabled"` | Instance QueueをONにする | `true` or `false` |


---

## ❌ 注意事項

- 公式でガイドされていないapiを使用しているため、予期しない仕様変更等によって動作しなくなる可能性があります。

---

## 🧑‍💻 更新履歴

- 2025/6/15 初版作成

---

ご要望・不明点・改善点などありましたら気軽にご連絡ください！  
Issue や Pull Request も歓迎します 🙌