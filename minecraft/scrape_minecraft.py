from bs4 import BeautifulSoup
import requests

url = "https://minecraft.fandom.com/wiki/Item"
home_url = "https://minecraft.fandom.com"


def get_wiki_pages():
    wiki_pages = []

    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
    else:
        html = response.text

        soup = BeautifulSoup(html, "html.parser")

        partitions = soup.select("div.div-col.columns.column-width")

        # only gets the first 4 partitions (excluding education edition, removed items, and joke items)
        partitions = partitions[:4]

        # iterates through each partition
        for partition in partitions:
            
            # gets all the wiki_pages
            pages = partition.select("a.mw-redirect")

            for page in pages:
                wiki_pages.append(f"{home_url}{page['href']}")

        #print(f"Number of partitions scraped: {len(partitions)}")

        with open("wiki_pages.txt", "w") as f:
            for page in wiki_pages:
                f.write(page)
                f.write('\n')

if __name__ == "__main__":
    get_wiki_pages()