from flask import Flask, jsonify
from blinkit import Blinkit_api
from time import sleep
import sys
import logging


app = Flask(__name__)

blinkit = Blinkit_api()


@app.route('/')
def myfun():
    return 'DSATM   Final year project'


@app.route('/blinkit/init/<string:pincode>')
def api1_init(pincode):
    blinkit.initialization()
    sleep(3)
    blinkit.set_location(pincode=pincode)
    return jsonify({"blinkit-result": "Initialized"})

@app.route('/blinkit/search/<string:product>')
def api1(product):
    mylist = blinkit.search_for_product(product=product)
    temp_list = []
    for item, packet_desc, price, url in mylist:
        temp_list.append({"item": item, "packet_description": packet_desc, "price": price, "url": url})
    return jsonify({"blinkit-result": "Success", "product": temp_list})

@app.route('/blinkit/quit')
def api1_quit():
    blinkit.exit()
    return jsonify({"blinkit-result": "Quit"})



if __name__ == '__main__':
    app.logger.addHandler(logging.StreamHandler(sys.stdout))
    app.logger.setLevel(logging.ERROR)
    app.run(debug=True)



