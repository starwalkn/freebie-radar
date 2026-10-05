import requests
import json
import os
import sys
import time
from datetime import datetime

# Windows Console UTF-8 Fix
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# --- 配置区 ---
# 1. 在 Telegram 找 @BotFather 传 /newbot，30秒就能拿到 BOT_TOKEN
# 2. 建立一个公开频道（例如 @FreeGameRadar），把你的 Bot 加为管理员（具有 Post Messages 权限）
# 3. 将你的频道用户名填在 TARGET_CHANNEL（例如 "@FreeGameRadar"）
BOT_TOKEN = os.environ.get("TG_BOT_TOKEN") or "YOUR_BOT_TOKEN_HERE"
TARGET_CHANNEL = os.environ.get("TG_CHANNEL") or "@YOUR_CHANNEL_HERE"

HISTORY_FILE = "posted_games_history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def send_telegram_message(caption, photo_url=None):
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("[Demo Mode] BOT_TOKEN 尚未设置，以下为待推播内容预览：")
        print("--------------------------------------------------")
        print(caption)
        print(f"附图: {photo_url}")
        print("--------------------------------------------------\n")
        return True

    if photo_url:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        data = {
            "chat_id": TARGET_CHANNEL,
            "photo": photo_url,
            "caption": caption,
            "parse_mode": "HTML"
        }
    else:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": TARGET_CHANNEL,
            "text": caption,
            "parse_mode": "HTML",
            "disable_web_page_preview": False
        }
    
    try:
        res = requests.post(url, data=data, timeout=10)
        return res.json().get("ok", False)
    except Exception as e:
        print(f"[-] Telegram 推播失败: {e}")
        return False

def check_epic_free_games(history):
    print("[*] 正在扫描 Epic Games Store 免费游戏列表...")
    url = "https://store-site-backend-static-ipv4.ak.epicgames.com/freeGamesPromotions?locale=en-US&country=US&allowCountries=US"
    try:
        r = requests.get(url, timeout=15)
        data = r.json()
        elements = data["data"]["Catalog"]["searchStore"]["elements"]
        
        for item in elements:
            title = item.get("title")
            page_slug = item.get("productSlug") or (item.get("catalogNs", {}).get("mappings", [{}])[0].get("pageSlug", ""))
            promotions = item.get("promotions") or {}
            current_promos = promotions.get("promotionalOffers", [])
            
            # 判断是否为当前正在进行的 100% 免费游戏
            if current_promos and len(current_promos) > 0:
                offers = current_promos[0].get("promotionalOffers", [])
                for offer in offers:
                    discount = offer.get("discountSetting", {})
                    if discount.get("discountPercentage") == 0:
                        # 0 元免费
                        game_id = f"epic_{item.get('id')}"
                        if game_id not in history:
                            # 提取封面图
                            image_url = None
                            for img in item.get("keyImages", []):
                                if img.get("type") in ["OfferImageWide", "DieselStoreFrontWide", "Thumbnail"]:
                                    image_url = img.get("url")
                                    break
                            
                            end_date = offer.get("endDate", "")[:10]
                            claim_url = f"https://store.epicgames.com/p/{page_slug}" if page_slug else "https://store.epicgames.com/free-games"
                            
                            msg = (
                                f"🔥 <b>【Epic 喜加一】限时 100% 免费领取！</b>\n\n"
                                f"🎮 <b>游戏名称</b>：{title}\n"
                                f"💰 <b>原价</b>：<s>{item.get('price', {}).get('totalPrice', {}).get('fmtPrice', {}).get('originalPrice', 'Paid')}</s> &rarr; <b>$0.00 (FREE)</b>\n"
                                f"⏳ <b>截止日期</b>：{end_date}\n\n"
                                f"👉 <a href='{claim_url}'>点击直达领取页面 ↗</a>\n\n"
                                f"<i>⚡ 全网免费福利雷达 • 绝不错过任何喜加一</i>"
                            )
                            print(f"[+] 发现新免费游戏: {title}")
                            if send_telegram_message(msg, image_url):
                                history.append(game_id)
                                save_history(history)
                                time.sleep(2)
    except Exception as e:
        print(f"[-] Epic 抓取异常: {e}")

def check_steam_free_games(history):
    print("[*] 正在扫描 Steam 100% 折扣限免游戏列表...")
    url = "https://store.steampowered.com/api/featuredcategories/?l=english"
    try:
        r = requests.get(url, timeout=15)
        data = r.json()
        specials = data.get("specials", {}).get("items", [])
        for item in specials:
            discount = item.get("discount_percent", 0)
            final_price = item.get("final_price", 1)
            # 100% OFF 且 现价为 0
            if discount == 100 or final_price == 0:
                app_id = item.get("id")
                game_id = f"steam_{app_id}"
                if game_id not in history:
                    title = item.get("name")
                    header_img = item.get("header_image")
                    claim_url = f"https://store.steampowered.com/app/{app_id}"
                    
                    msg = (
                        f"🔥 <b>【Steam 喜加一】限时 100% 免费永久保留！</b>\n\n"
                        f"🎮 <b>游戏名称</b>：{title}\n"
                        f"💰 <b>原价</b>：<s>Paid</s> &rarr; <b>$0.00 (FREE TO KEEP)</b>\n\n"
                        f"👉 <a href='{claim_url}'>点击直达 Steam 商店 ↗</a>\n\n"
                        f"<i>⚡ 全网免费福利雷达 • 绝不错过任何喜加一</i>"
                    )
                    print(f"[+] 发现新 Steam 免费游戏: {title}")
                    if send_telegram_message(msg, header_img):
                        history.append(game_id)
                        save_history(history)
                        time.sleep(2)
    except Exception as e:
        print(f"[-] Steam 抓取异常: {e}")

if __name__ == "__main__":
    history = load_history()
    check_epic_free_games(history)
    check_steam_free_games(history)
    print("[*] 检查完毕。")
