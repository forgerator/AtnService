import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from scrapy.http import FormRequest


class AtnScrape(scrapy.Spider):
    """This class scrapes the ATN site (https://austintennis.net.org) to gather player information """

    name = 'Austin Tennis Net'
    start_urls = ['https://www.austintennisnet.org/player_login.php']
    user = ''
    password = ''
    players = []

    def parse(self, response):
        return [FormRequest.from_response(
            response,
            formdata={'myusername': self.user, 'mypassword': self.password},
            callback=self.after_login)]

    def after_login(self, response):
        # check login succeed before going on
        if "Access Denied" in str(response.body):
            self.log("Login failed", level=log.ERROR)
            return
        else:
            # continue scraping with authenticated session...
            return Request(
                url="https://www.austintennisnet.org/ladder_singles/singles_ladder.php?weekend_ladder=0",
                callback=self.generate_player_list)

    def generate_player_list(self, response):
        """Generates a list of players using BeautifulSoup for parsing the html"""

        soup = BeautifulSoup(str(response.body))

        for anchor in soup.find_all('a', href=lambda x: x and 'player_information.php?player_lookup_number' in x):
            player_name = str(anchor.contents[0]).replace("\\n", "").strip()
            self.players.append(player_name)



