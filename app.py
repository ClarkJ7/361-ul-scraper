from flask import Flask
from flask_restful import Api, Resource, abort
from bs4 import BeautifulSoup
import requests
import pandas
import lxml


app = Flask(__name__)
api = Api(app)


# Function to check if page loaded
def check_link(page):
    if page.status_code > 200:
        abort(404, message="Bad Link")
    else:
        print("Page loaded successfully")


class ReturnTable(Resource):

    def get(self, URL, table_num):

            print("table scrape requested")
            # Obtain wikipedia URL and designate CSV output
            link = "https://en.wikipedia.org/wiki/" + URL

            # Verify wikipedia link works, abort if not
            page = requests.get(link)
            check_link(page)

            # Obtain tables into panda dataframe
            dfs = pandas.read_html(link)
            # Select specific table
            table = dfs[table_num]
            # Turn table into dictionary
            table_output = table.to_dict()

            return table_output


class ReturnUL(Resource):

    def get(self, URL):

            print("ul scrape requested")
            # create URL for Wikipedia page
            link = "https://en.wikibooks.org/wiki/Cookbook:" + URL

            # Verify wikipedia link works, abort if not
            page = requests.get(link)
            check_link(page)

            # Obtain ingredients UL
            soup = BeautifulSoup(page.content, 'html.parser')

            # Find Ingredients header on page
            element = soup.find("span", {"class": "mw-headline", "id": "Ingredients"}).parent

            ingredient_string = ""

            # Pull all <li> from Ingredient Section
            while element.next_sibling.name != 'h2':
                if element.name == 'ul':
                    for li in element.find_all('li'):
                        ingredient_string += li.get_text()
                        ingredient_string += ";"

                element = element.next_sibling

            ingredient_string = ingredient_string.replace('\n', ';')

            ingredient_list = ingredient_string.split(';')
            ingredient_list.pop(-1)

            return ingredient_list


@app.route('/')
def root():
    return """This is the Table/UL Scraper microservice
    To scrape a table use the input format of: /<string:URL>/<int:table_num>
    To scrape a UL use the input format of: /<string:URL>
    <string:URL> = end of wikipedia URL for desired page, ex: Kyle_Lewis for page on Seattle Mariner Kyle Lewis
    <int:table_num> = index of table on page, ex: to return the first table on Kyle Lewis's page enter /Kyle_Lewis/0"""


api.add_resource(ReturnTable, "/<string:URL>/<int:table_num>")
api.add_resource(ReturnUL, "/<string:URL>")


if __name__ == "__main__":
    app.run(debug=True, port=5001)