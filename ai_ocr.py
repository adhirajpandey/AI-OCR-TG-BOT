from PIL import Image
import pytesseract
from dotenv import load_dotenv
import os
import openai

# Usage : python ai_ocr.py <path_to_image>

# get img path as argumernt of this script
import sys

# IMG_PATH = sys.argv[1]

# Load variables from .env into system's environment variables
load_dotenv()

PYTESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = PYTESSERACT_PATH

openai.api_type = "azure"
openai.api_version = "2023-05-15"
openai.api_base = os.getenv("BASE_URL")  # Your Azure OpenAI resource's endpoint value.
openai.api_key = os.getenv("API_KEY")


def extract_text_from_image(imagepath):
    # Open an image file
    image = Image.open(imagepath)

    # Use pytesseract to extract text
    text = pytesseract.image_to_string(image)

    return text


def gen_response(prompt):
    response = openai.ChatCompletion.create(
        engine="MyStatus",
        messages=[{"role": "system", "content": prompt}],
        temperature=0,
        max_tokens=350,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )
    response = response["choices"][0]["message"]["content"]

    return response


def correct_text(base_prompt, ocr_text):
    ai_corrected_text = gen_response(base_prompt + ocr_text)

    return ai_corrected_text


def get_base_prompt(textfile):
    with open(textfile, 'r') as f:
        base_prompt = f.read()
    return base_prompt


def AI_ocr(imgpath):
    # IMG_PATH = r'D:\Projects New\PLAYGROUND\OCR\j1.jpg'
    base_prompt = get_base_prompt('base_prompt.txt')

    # Extract text from image
    # ocr_text = extract_text_from_image(IMG_PATH)
    ocr_text = extract_text_from_image(imgpath)

    # Correct the text
    corrected_text = correct_text(base_prompt, ocr_text)

    return corrected_text