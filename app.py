import json
import logging
import random
import sys
import time
from datetime import datetime
from typing import Iterator

from flask import Flask, Response, render_template, request, stream_with_context

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

application = Flask(__name__)
random.seed()  # Initialize the random number generator


@application.route("/")
def index() -> str:
    return render_template("index.html")


def getdata() -> Iterator[str]:
    """
    Generates random value between 0 and 100
    :return: String containing current timestamp (YYYY-mm-dd HH:MM:SS) and randomly generated data.
    """
    if request.headers.getlist("X-Forwarded-For"):
        client_ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        client_ip = request.remote_addr or ""

    try:
        logger.info("Client %s connected", client_ip)
        while True:
            f = open('data.json')
  
            # returns JSON object as 
            # a dictionary
            file_data = json.load(f)
            json_data = json.dumps(
                {
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "tvalue": file_data[0],
                    "hvalue": file_data[1],
                    "pvalue": file_data[2],
                    "axvalue": file_data[3],
                    "ayvalue": file_data[4],
                    "azvalue": file_data[5],
                    "gxvalue": file_data[6],
                    "gyvalue": file_data[7],
                    "gzvalue": file_data[8],
                }
            )
            yield f"data:{json_data}\n\n"
            time.sleep(1)
    except GeneratorExit:
        logger.info("Client %s disconnected", client_ip)


@application.route("/chart-data")
def chart_data() -> Response:
    response = Response(stream_with_context(getdata()), mimetype="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    return response

@application.route('/on')
def on():
    obj = '"value":1'
    obj_json = json.dumps(obj)
    with open('./obj.json','w') as outfile:
        outfile.write(obj_json)
    print ("Encendido Padre")
    return('')
    
@application.route('/off')
def off():
    obj = '"value":0'
    obj_json = json.dumps(obj)
    with open('./obj.json','w') as outfile:
        outfile.write(obj_json)
    print ("Apagado Padre")
    return('')

if __name__ == "__main__":
    application.run(host="0.0.0.0", threaded=True)