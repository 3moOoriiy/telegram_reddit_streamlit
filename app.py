# إنشاء مشروع مدمج يحتوي على كود Reddit (scraping من HTML) وTelegram (باستخدام Bot API)
import os
import zipfile

project_path = "/mnt/data/reddit_telegram_scraper_final"
os.makedirs(project_path, exist_ok=True)

# app.py بالكود الموحد
app_code = '''import streamlit as st
import requests
import pandas as pd
from bs4 import BeautifulSoup

# Telegram Bot Token
BOT_TOKEN = "7850779767:AAEt52D2I1OE38X-rNDRqC2ifah3OXefFDo"

# Telegram Scraper using Bot API
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

# Reddit Scraper using HTML parsing
def get_reddit_info(link):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(link, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            name_tag = soup.find("h1")
            bio_tag = soup.find("p", attrs={"data-testid": "profile-description"})

            account_name = name_tag.text.strip() if name_tag else "N/A"
            account_bio = bio_tag.text.strip() if bio_tag else "N/A"

            return {
                "Platform": "Reddit",
                "Account Name": account_name,
                "Account Bio": account_bio,
                "Status": "Active",
                "Link": link
            }
        elif response.status_code == 404:
            return {
                "Platform": "Reddit",
                "Account Name": "N/A",
                "Account Bio": "N/A",
                "Status": "Not Found",
                "Link": link
            }
    except Exception:
        return {
            "Platform": "Reddit",
            "Account Name": "N/A",
            "Account Bio": "N/A",
            "Status": "Error",
            "Link": link
        }

# Streamlit UI
st.set_page_config(page_title="Social Account Scraper", layout="centered")
st.title("🔍 Social Account Scraper")

platform = st.selectbox("اختر المنصة:", ["Telegram", "Reddit"])
user_input = st.text_area("أدخل روابط الحسابات (كل رابط في سطر):")

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

# requirements.txt
requirements = '''streamlit
requests
pandas
beautifulsoup4
'''

# حفظ الملفات
with open(f"{project_path}/app.py", "w", encoding="utf-8") as f:
    f.write(app_code)

with open(f"{project_path}/requirements.txt", "w", encoding="utf-8") as f:
    f.write(requirements)

# ضغط الملفات إلى ZIP
zip_path = "/mnt/data/reddit_telegram_scraper_final.zip"
with zipfile.ZipFile(zip_path, "w") as zipf:
    zipf.write(f"{project_path}/app.py", arcname="app.py")
    zipf.write(f"{project_path}/requirements.txt", arcname="requirements.txt")

zip_path
