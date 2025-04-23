from zipfile import ZipFile
import os

# إنشاء مجلد مؤقت لتجميع الملفات
project_dir = "/mnt/data/reddit_telegram_scraper_final_v2"
os.makedirs(project_dir, exist_ok=True)

# ملف app.py
app_code = '''
import streamlit as st
from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import pandas as pd
import time

def setup_driver():
    options = EdgeOptions()
    options.use_chromium = True
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)
    return driver

def scrape_reddit(url, driver):
    platform = "Reddit"
    account_name = "N/A"
    account_bio = "N/A"
    status = "Failed or Not Found"

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 15)

        try:
            name_element = wait.until(EC.presence_of_element_located((By.XPATH, "//h1")))
            account_name = name_element.text.strip()
        except:
            pass

        try:
            bio_element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'ProfileSidebar__description')]")))
            account_bio = bio_element.text.strip()
        except:
            pass

        if account_name != "N/A":
            status = "Active"

    except Exception as e:
        print("❌ Reddit Error:", e)

    return {
        "Platform": platform,
        "Account Name": account_name,
        "Account Bio": account_bio,
        "Status": status,
        "Link": url
    }

def scrape_telegram(url, driver):
    platform = "Telegram"
    account_name = "N/A"
    account_bio = "N/A"
    status = "Active"

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 15)

        try:
            name_element = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@dir='auto']")))
            account_name = name_element.text.strip()
        except:
            account_name = "N/A"

        try:
            bio_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "tgme_page_description")))
            account_bio = bio_element.text.strip()
        except:
            account_bio = "N/A"

        if "unavailable" in driver.page_source:
            status = "Suspended"

    except Exception as e:
        print("❌ Telegram Error:", e)
        status = "Failed"

    return {
        "Platform": platform,
        "Account Name": account_name,
        "Account Bio": account_bio,
        "Status": status,
        "Link": url
    }

# Streamlit UI
st.title("🔍 Social Account Scraper")

platform = st.selectbox("اختر المنصة:", ["Reddit", "Telegram"])
urls_input = st.text_area("أدخل روابط الحسابات (كل رابط في سطر):")

if st.button("ابدأ"):
    urls = [u.strip() for u in urls_input.split("\\n") if u.strip()]
    results = []

    driver = setup_driver()
    for url in urls:
        if "reddit.com" in url:
            results.append(scrape_reddit(url, driver))
        elif "t.me" in url:
            results.append(scrape_telegram(url, driver))
    driver.quit()

    df = pd.DataFrame(results)
    st.markdown("### 📊 النتائج:")
    st.dataframe(df)
    st.download_button("📥 تحميل النتائج CSV", df.to_csv(index=False).encode("utf-8"), "results.csv", "text/csv")
'''

with open(f"{project_dir}/app.py", "w", encoding="utf-8") as f:
    f.write(app_code)

# عمل ملف requirements.txt
with open(f"{project_dir}/requirements.txt", "w") as f:
    f.write("streamlit\nselenium\nwebdriver-manager\npandas")

# ضغط المجلد
zip_path = "/mnt/data/reddit_telegram_scraper_final_v2.zip"
with ZipFile(zip_path, 'w') as zipf:
    for root, dirs, files in os.walk(project_dir):
        for file in files:
            filepath = os.path.join(root, file)
            zipf.write(filepath, arcname=os.path.relpath(filepath, project_dir))

zip_path
