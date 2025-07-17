import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pyttsx3
from PIL import Image, ImageDraw, ImageFont
from translate import Translator
from quotes import Quotes


def fetch_and_translate_quotes(language,count):
    translater = Translator(to_lang=language, from_lang='en')
    quotes = Quotes()
    translated_quote_list = []
    try:
        for _ in range(1,count+1):
            quote,author = quotes.get()
            if quote and author:
                if language != "en":
                    translated_quote = translater.translate(quote).title()
                else:
                    translated_quote = quote
                translated_quote_list.append((translated_quote,author))
    except Exception as e:
        print(e)
    return translated_quote_list

def save_quote_to_file(quote_list):
    try:
        with open("translated.txt", 'w', encoding="utf-8") as file:
            for q,a in quote_list:
                formatted_code = f"Quote : {q}, Author : {a}\n"
                file.write(formatted_code)
    except Exception as e:
        print(e)

def text_to_speech(quote_list):
    try:
        if len(quote_list) > 0:
            speech_obj = pyttsx3.init()
            for quote,_ in quote_list:
                speech_obj.say(quote)
                speech_obj.runAndWait()

    except Exception as e:
        print(e)

def save_as_image(quote_list):
    try:
        img_width = 700
        line_height  = 60
        padding = 50
        img_height = (padding * 2) + (line_height*len(quote_list))
        img = Image.new("RGB",(img_width,img_height), color=(255,255,255))
        obj = ImageDraw.Draw(img)
        font = ImageFont.load_default()
        y_cord = padding
        for q,a in quote_list:
            formatted_code = f"Quote : {q}, Author : {a}\n"
            obj.text((padding, y_cord), formatted_code,fill=(0,0,0),font=font)
            y_cord += line_height

        image_name = "translated_quotes.png"
        img.save(image_name)
        return image_name

    except Exception as e:
        print(e)

def send_email(quote_list,image_path,recipent_address):
    gmail = "controllerplayer68@gmail.com"
    password = "bldb jvbx gsje nhfw"
    msg = MIMEMultipart()
    msg["From"] = gmail
    msg["To"] = recipent_address
    msg["Subject"] = "Daily Translated Quotes!"
    body = "\n \n ".join([f"Quote : {q}, Author : {a}\n" for q,a in quote_list])
    msg.attach(MIMEText(body,"plain"))
    if image_path is not None:
        with open(image_path, "rb") as image_file:
            img = MIMEImage(image_file.read())
            img.add_header("Content-Disposition", "attachment", filename=image_path)
            msg.attach(img)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(gmail,password)
        server.sendmail(gmail, recipent_address, msg.as_string())
        server.quit()
    except Exception as e:
        print(e)

def main():
    need_translation = input("Do you want to translate into another language? (Yes/no): ")

    if need_translation == "yes":
        target_language = input("Enter target language (e.g., 'es' for Spanish, 'fr' for French): ").strip().lower()
    else:
        target_language = "en"

    quote_count = int(input("Enter the number of quotes you want to translate: "))
    result = fetch_and_translate_quotes(target_language, quote_count)
    print(result)

    save_file = input("Do you want to save the quotes to a file? (yes/no): ").lower()
    if save_file == "yes":
        save_quote_to_file(result)

    var = None
    save_img = input("Do you want to see an image of the quotes? (yes/no)").lower()
    if save_img == "yes":
        var = save_as_image(result)

    text_speech = input("Do you want the audio of the quotes? (yes/no)").lower()
    if text_speech == "yes":
        text_to_speech(result)

    want_email_address = input("Do you want an email copy? (yes/no)").lower()
    if want_email_address == "yes":
        email_address = input("Enter your email address here (vihaan.khullar@gmail.com) : ")
        send_email(result,var,email_address)

main()


