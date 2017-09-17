import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from scrapy.http import FormRequest
from scrapy.crawler import CrawlerProcess

from AtnPlayer import AtnPlayer


class AtnScrape(scrapy.Spider):
    """This class scrapes the ATN site (https://austintennis.net.org) to gather player information """

    name = 'Austin Tennis Net'
    start_urls = ['https://www.austintennisnet.org/player_login.php']
    user = 'hbarlas'
    password = 'testing123'
    players = []

    def parse(self, response):
        return [FormRequest.from_response(
            response,
            formdata={'myusername': self.user, 'mypassword': self.password},
            callback=self.after_login)]

    def after_login(self, response):
        # check login succeed before going on
        if "Access Denied" in str(response.body):
            print("Login failed")
            return
        else:
            # continue scraping with authenticated session...
            return Request(
                url="https://www.austintennisnet.org/ladder_singles/singles_ladder.php?weekend_ladder=0",
                callback=self.parse_ladder_listing)

    def parse_ladder_listing(self, response):
        self.generate_player_list(str(response.body))

    def generate_player_list(self, response_str):
        """Generates a list of players using BeautifulSoup for parsing the html"""

        soup = BeautifulSoup(response_str)

        for anchor in soup.find_all('a', href=lambda x: x and 'player_information.php?player_lookup_number' in x):
            atn_id = str(anchor.attrs['href']).split("=")[1]
            player_name = str(anchor.contents[0]).replace("\\n", "").strip()
            atn_player = AtnPlayer(atn_id, player_name, 'n/a')
            self.players.append(atn_player)

if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(AtnScrape)
    process.start() # the script will block here until the crawling is finished
