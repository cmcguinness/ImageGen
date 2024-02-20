from openai import OpenAI
import requests
from PIL import Image
from datetime import datetime as dt
import os

"""
# generate_image
Creates an image and places it in the outputs/ directory

## arguments
* description: the text to feed to DALL-# to generate the image
* quality: optional, one of `standard` or `hd`
* size: optional, one of  `1024x1024`, `1024x1792` or `1792x1024`

## returns
description_file_name, image_file_name
"""


def generate_image(description: str, quality='standard', size='1024x1024'):

    if not os.path.isdir('outputs'):
        os.mkdir('outputs')

    tstamp = dt.now().strftime("%Y-%m-%d-%H-%M-%S")
    description_name = f'outputs/{tstamp}-prompt.txt'
    with open(description_name, 'w') as f:
        f.write(description)

    client = OpenAI()

    response = client.images.generate(
        model="dall-e-3",
        prompt=description,
        size=size,
        quality=quality,
        n=1,
    )

    image_url = response.data[0].url

    generated_image = requests.get(image_url).content

    image_name = f'outputs/{tstamp}-image.png'

    with open(image_name, "wb") as image_file:
        image_file.write(generated_image)  # write the image to the file

    return description_name, image_name

if __name__ == "__main__":

    print('Image Generation Tool')

    description = input('Describe: ')

    desc_name, image_name = generate_image(description)

    Image.open(image_name).show()


