
import requests
import base64


def predict_new(url, image_path):
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read())

    # Setup separate json data
    payload = {
        "mime" : "image/png",
        "img_bytes": base64_image,
    }

    response = requests.post(url, data = payload)

    return response


if __name__ == '__main__':
    
    URL = 'http://localhost:8000/predict'


    # Create a POST request to send the image to the server
    #response = post_image(image, URL)
    res = predict_new(URL, './impuestos.jpeg')
    
    # Print the response
    print(res.text)