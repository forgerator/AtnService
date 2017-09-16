import unittest

from AtnScrape import AtnScrape


class AtnServiceTests(unittest.TestCase):

    def test_generate_player_list(self):
        scrape = AtnScrape()
        test_string = "<html><font color=\"#000000\" size=\"2\" face=\"Geneva, Arial, Helvetica, sans-serif\"> <A " \
                      "class=\"sidebar\" HREF=\"../ladder_players/player_information.php?player_lookup_number=4039" \
                      "\">\n              Andrea Summy              </A></font></html> "

        scrape.generate_player_list(test_string)

        self.assertTrue("Andrea Summy" in scrape.players, "Could not find the player in the list")
if __name__ == '__main__':
    unittest.main()
