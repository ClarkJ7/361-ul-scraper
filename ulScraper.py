from flask import Flask
from flask_restful import Api, Resource, abort
from bs4 import BeautifulSoup
import requests



app = Flask(__name__)
api = Api(app)


# Function to check if page loaded
def check_link(page):
    if page.status_code > 200:
        abort(404, message="Bad Link")
    else:
        print("Page loaded successfully")


class ReturnIngredients(Resource):

    def get(self, URL):

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

        # return ingredient string
        return ingredients_list


class ReturnWorld(Resource):

    def get(self):
        return "Hello World"


api.add_resource(ReturnIngredients, "/<string:URL>")



if __name__ == "__main__":
    app.run(debug=True)