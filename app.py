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
            body = soup.find("div", {"class": "mw-parser-output"})
            ingredients = body.find_all("ul")

            # Create string with all ingredients seperated by a comma
            for row in ingredients:
                ingredients_list = ""
                if row.get_text():
                    ingredients_list += row.get_text()

            ingredients_list = ingredients_list.replace('\n', ',')

            # Turn string into list
            ingredients_list = ingredients_list.split(',')

            # return ingredient string
            return ingredients_list


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
    app.run(debug=True)