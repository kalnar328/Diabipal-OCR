import requests
from flask_cors import CORS

from flask import Flask, request

from image_processing import process_image_less_noise, process_image_for_ocr, get_image_cv, get_image_pil
from data_extraction import process_ocr

app = Flask(__name__)
cors = CORS(app)


#  ?url=
@app.route('/url', methods=['POST', 'GET'])
def processURL():

    # load image from the url
    image_cv = get_image_cv(request)

    # image processing applied image
    processed_image = process_image_less_noise(image_cv)

    # extract text using ocr engine
    # returns an array of test name, result, unit, range
    result = process_ocr(processed_image)

    # word correction using knowledge graph
    if result:
        # response = requests.post(url="http://127.0.0.1:3000/corrections", data=result)
        response = requests.post(url="https://diabipal-knowledge-graph.herokuapp.com/corrections", data=result)
        # print(response.json())
        # returns a json object
        if response.json():
            print("Response", response.json())
            return response.json()
        else:
            return {'Error'}

    #  if the result array is empty apply more image processing techniques
    else:
        # image processing applied image
        out_image = process_image_for_ocr(get_image_pil(request))

        # extract text using ocr engine
        # returns an array of test name, result, unit, range
        out_array = process_ocr(out_image)

        if out_array:
            # response = requests.post(url="http://127.0.0.1:3000/corrections", data=result)
            response = requests.post(url="https://diabipal-knowledge-graph.herokuapp.com/corrections", data=out_array)
            if response.json():
                print("Response", response.json())
                return response.json()
            else:
                return {'Error'}
        else:
            return {'Error'}


if __name__ == '__main__':
    app.run(debug="true")
