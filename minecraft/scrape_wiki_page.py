from selenium.webdriver.common.by import By
from selenium import webdriver
#import undetected_chromedriver as uc
import time
import chromedriver_autoinstaller
from selenium.webdriver.chrome.options import Options
from playwright.sync_api import sync_playwright
import re
import pandas as pd
from tqdm import tqdm
import random
import requests


from bs4 import BeautifulSoup

FORBIDDEN_CHAR = ["\xa0+Matching", "Matching Overworld"]

URLS_TXT = "wiki_pages.txt"

crafting_recipes_url = "https://www.minecraft-crafting.net/"
url2 = "https://minecraft.tools/en/crafting.php"
url3 = "https://www.minecraftcrafting.info/"

def random_delay(min_seconds=2, max_seconds=5):
    time.sleep(random.uniform(min_seconds, max_seconds))

def scrape_page(driver, url):
    item = {}

    driver.get(url)
    time.sleep(3)

    html = driver.page_source

    soup = BeautifulSoup(html, "html.parser")

    item["name"] = soup.select_one("h2.pi-item.pi-item-spacing.pi-title.pi-secondary-background").text

    ingredients = soup.select_one("table.wikitable").select_one("td").text

    for char in FORBIDDEN_CHAR:
        ingredients = " ".join(ingredients.split(char))

    item["ingredients"] = ingredients.split()

    item["image"] = soup.select_one("img.pi-image-thumbnail")["src"]
    

    return item

def scrape_page2():
    minecraft_items = []
    url = "https://minecraft.tools/en/crafting.php"
    home = "https://minecraft.tools/en/"
    categories = ["Building Blocks", "Decoration Blocks", "Redstone", "Transportation", "Miscellaneous", "Food & Drinks", "Tools & Utilities", "Combat", "Brewing", "Others"]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(110, 120)}.0.0.0 Safari/537.36",
            viewport={"width": random.randint(1000, 1600), "height": random.randint(700, 1000)},
            locale='en-US',
            timezone_id="America/New_York",
            extra_http_headers={
                'Accept-Language': 'en-US,en;q=0.9'
            }
        )
        page = context.new_page()
        
        page.goto("https://minecraft.tools/en/crafting.php", wait_until="networkidle")
        page.wait_for_timeout(2000)

        sections = page.query_selector_all("div.categorie")

        for i, section in enumerate(sections):
            
            items = section.query_selector_all("img.block-small.tooltip")

            for item in tqdm(items):
                minecraft_item = {}
                minecraft_item["name"] = item.get_attribute("alt")[:-4]
                minecraft_item["name"] = "| ".join(minecraft_item["name"].split("<br><span class='potion_list'><span class='potion_positif'>"))
                minecraft_item["name"] = " ".join(minecraft_item["name"].split("</span><br/></span>"))
                minecraft_item["name"] = " | ".join(minecraft_item["name"].split("<br/><span class='potion_positif'>"))
                minecraft_item["name"] = " | ".join(minecraft_item["name"].split("<br><span class='potion_list'><span class='potion_negatif'>"))
                minecraft_item["name"] = " | ".join(minecraft_item["name"].split("<br><span class='potion_list'><span class='potion_base'>"))
                minecraft_item["name"] = " ".join(minecraft_item["name"].split("<span style='color: #55FFFF; '>"))
                minecraft_item["name"] = " ".join(minecraft_item["name"].split("br><span class='tooltip_attack_damage'>"))
                minecraft_item["name"] = " ".join(minecraft_item["name"].split("</span>"))
                minecraft_item["name"] = " ".join(minecraft_item["name"].split("<"))
                minecraft_item["image"] = f"{home}{item.get_attribute("src")}"
                minecraft_item["category"] = categories[i]

                # Random sleep to act like human
                random_delay(2, 5)

                # Scroll item into view
                item.scroll_into_view_if_needed()
                random_delay(0.5, 1.5)

                # Click a button by selector
                item.click(force=True)  # CSS selector (id)
                page.wait_for_load_state("load")

                elements = page.query_selector_all("div.case-crafting")

                ingredients = set()
                for element in elements:
                    img = element.query_selector("img.block-small.tooltip")
                    if img:
                        ingredient = img.get_attribute("alt")[:-4]
                        ingredient = "".join(ingredient.split("<span style='color: #FF55FF; '>"))
                        ingredient = "".join(ingredient.split("</span>"))
                        ingredient = " | ".join(ingredient.split("<br><span class='potion_list'><span class='potion_negatif'>"))
                        ingredient = " | ".join(ingredient.split("<br><span class='potion_list'><span class='potion_positif'>"))
                        ingredient = "".join(ingredient.split("<br/>"))
                        ingredients.add(ingredient)
                minecraft_item["ingredients"] = ingredients

                minecraft_items.append(minecraft_item)

        browser.close()
        print("finished scraping minecraft")
        return minecraft_items

def scrape_crafting_recipes():
    url = "https://www.minecraftcrafting.info/"

    response = requests.get(url)

    html = response.text

    dfs = pd.read_html(html)
    soup = BeautifulSoup(html, 'html.parser')

    tables = soup.find_all('table')

    # Extract all <h2> tags
    h2_tags = soup.find_all('h2')

    # Optional: get just the text content
    categories = [tag.get_text(strip=True) for tag in h2_tags]

    dfs = dfs[1:]
    tables = tables[1:]

    print(categories)

    print(f"number of categories: {len(categories)}")
    print(f"number of tables: {len(dfs)}")

    for i, df in enumerate(dfs):
        # removes the first row of the dataframe
        df = df.iloc[1:]

        # drops null column
        df = df.drop(columns=[2])

        df = df.rename(columns={
            0: 'Name',
            1: 'Ingredients',
            3: 'Description'
        })

        images = []
        image_tags = tables[i].find_all('img')
        for tag in image_tags:
            image = tag['src']
            images.append(f"{url}{image}")

        df["Image"] = images[:len(df)]  # Prevent image overflow

        # adds the category column
        df["Category"] = categories[i] if i < len(categories) else "Unknown"

        dfs[i] = df

        #print(df.head())

    minecraft_df = pd.concat(dfs, ignore_index=True)
    #print(minecraft_items)
    return minecraft_df

if __name__ == "__main__":

    items_df = scrape_crafting_recipes()

    print(items_df)

    with pd.ExcelWriter('minecraft_recipes.xlsx', engine='openpyxl') as writer:
        items_df.to_excel(writer, sheet_name='minecraft crafting recipes', index=False)
