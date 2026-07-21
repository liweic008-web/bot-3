import os
import requests

# 1. 從 GitHub Secrets 讀取隱私資訊
HOYO_COOKIE = os.getenv("HOYO_COOKIE")
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")

# 2. 星鐵 (HoYoLAB 國際服) 的官方簽到設定
ACT_ID = "e202303301540311"  # 星鐵簽到活動 ID
SIGN_URL = f"https://sg-public-api.hoyolab.com/event/luna/os/sign?lang=zh-tw&act_id={ACT_ID}"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://act.hoyolab.com/",
    "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cookie": HOYO_COOKIE
}

def do_check_in():
    if not HOYO_COOKIE:
        print("❌ 錯誤：找不到 HOYO_COOKIE，請檢查 GitHub Secrets！")
        return

    # 發送 POST 請求給 HoYoLAB 進行簽到
    response = requests.post(SIGN_URL, headers=headers, json={"act_id": ACT_ID})
    data = response.json()
    
    code = data.get("retcode")
    msg = data.get("message", "未知結果")
    
    # 判斷簽到狀態
    if code == 0:
        status_msg = "🎉 **【星鐵自動簽到成功！】**\n成功領到今天的簽到獎勵囉！"
    elif code == -5003:
        status_msg = "ℹ️ **【星鐵簽到提醒】**\n今天已經簽到過囉，不用重複簽～"
    else:
        status_msg = f"⚠️ **【星鐵簽到失敗】**\n錯誤代碼：`{code}`\n訊息：{msg}"
        
    print(status_msg)
    send_discord_notification(status_msg)

def send_discord_notification(message):
    if not DISCORD_WEBHOOK:
        print("未設定 Discord Webhook，跳過通知發送。")
        return
    
    payload = {"content": message}
    requests.post(DISCORD_WEBHOOK, json=payload)

if __name__ == "__main__":
    do_check_in()
