from flask import Flask, json
from flask_restful import Api
from flask_restful_swagger import swagger
from AtnScrape import AtnScrape

app = Flask(__name__)


###################################
# Wrap the Api with swagger.docs. It is a thin wrapper around the Api class that adds some swagger smarts
api = swagger.docs(Api(app), apiVersion='0.1')
###################################


@app.route('/players', methods=['GET'])
def get_all_players():
    """Gets a list of all players within the ATN Site.
        This is done by scraping the site and parsing out the html to obtain
        a complete list of player information.
    """
    # scrape = AtnScrape()
    # scrape.parse()
    # players_list = scrape.players
    players_list = ["Roger Federer", "Rafael Nadal", "Novak Djokovic"]
    return json.dumps({'success': True, 'data': players_list})

if __name__ == '__main__':
    app.run(debug=True)
