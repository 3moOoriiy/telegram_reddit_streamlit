# تجهيز نسخة محدثة من المشروع مع إصلاح reddit API بكود جديد
import os
import zipfile

project_path = "/mnt/data/reddit_telegram_scraper_fixed"
os.makedirs(project_path, exist_ok=True)

# app.py بالكود الكامل
code = '''import streamlit as st
import requests
import pandas as pd

# Telegram Bot Token (عشان تجرب لازم تحط توكن شغال)
BOT_TOKEN = "7850779767:AAEt52D2I1OE38X-rNDRqC2ifah3OXefFDo"

# Telegram Scraper
def get_telegram_info(link):
    if "t.me/" in link:
        username = link.split("t.me/")[-1].strip().replace("/", "")
    else:
        username = link.strip()
    api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/getChat?chat_id=@{username}"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        if data["ok"]:
            chat = data["result"]
            return {
                "Platform": "Telegram",
                "Account Name": chat.get("title", "N/A"),
                "Account Bio": chat.get("description", "N/A"),
                "Status": "Active",
                "Link": link
            }
    return {
        "Platform": "Telegram",
        "Account Name": "N/A",
        "Account Bio": "N/A",
        "Status": "Failed or Not Found",
        "Link": link
    }

# ✅ Reddit Scraper باستخدام Reddit API الرسمي
def get_reddit_info(link):
    if "reddit.com/user/" in link:
        username = link.split("reddit.com/user/")[-1].strip("/").split("/")[0]
    else:
        username = link.strip()
    
    headers = {"User-Agent": "Mozilla/5.0"}
    profile_url = f"https://www.reddit.com/user/{username}/about.json"

    try:
        response = requests.get(profile_url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            user_info = data["data"]
            return {
                "Platform": "Reddit",
                "Account Name": user_info.get("subreddit", {}).get("title", username),
                "Account Bio": user_info.get("subreddit", {}).get("public_description", "N/A"),
                "Status": "Active",
                "Link": f"https://www.reddit.com/user/{username}/"
            }
        elif response.status_code == 404:
            return {
                "Platform": "Reddit",
                "Account Name": username,
                "Account Bio": "N/A",
                "Status": "Suspended or Not Found",
                "Link": f"https://www.reddit.com/user/{username}/"
            }
    except Exception as e:
        return {
            "Platform": "Reddit",
            "Account Name": username,
            "Account Bio": "N/A",
            "Status": "Error",
            "Link": f"https://www.reddit.com/user/{username}/"
        }

# Streamlit UI
st.set_page_config(page_title="Account Scraper", layout="centered")
st.title("🔍 Social Account Scraper (Telegram + Reddit)")

platform = st.selectbox("اختر المنصة:", ["Telegram", "Reddit"])
user_input = st.text_area("أدخل الروابط (رابط في كل سطر):")

if "results" not in st.session_state:
    st.session_state.results = []

if st.button("ابدأ"):
    links = [link.strip() for link in user_input.split("\\n") if link.strip()]
    for link in links:
        if platform == "Telegram":
            result = get_telegram_info(link)
        elif platform == "Reddit":
            result = get_reddit_info(link)
        else:
            result = {
                "Platform": platform,
                "Account Name": "N/A",
                "Account Bio": "N/A",
                "Status": "Unsupported",
                "Link": link
            }
        st.session_state.results.append(result)

if st.session_state.results:
    st.markdown("---")
    st.subheader("📊 النتائج:")
    df = pd.DataFrame(st.session_state.results)
    st.dataframe(df)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 تحميل النتائج CSV", csv, "accounts.csv", "text/csv")
'''

with open(f"{project_path}/app.py", "w", encoding="utf-8") as f:
    f.write(code)

with open(f"{project_path}/requirements.txt", "w", encoding="utf-8") as f:
    f.write("streamlit\nrequests\npandas")

# ضغط المشروع
zip_path = "/mnt/data/reddit_telegram_scraper_fixed.zip"
with zipfile.ZipFile(zip_path, "w") as zipf:
    zipf.write(f"{project_path}/app.py", arcname="app.py")
    zipf.write(f"{project_path}/requirements.txt", arcname="requirements.txt")

zip_path
