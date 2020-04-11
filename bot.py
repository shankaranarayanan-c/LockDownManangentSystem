"""
Reference links:
https://www.twilio.com/blog/build-a-whatsapp-chatbot-with-python-flask-and-twilio
"""
import sqlite3
from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)


@app.route('/bot', methods=['POST'])
def bot():
    # print("AccountSid: "+request.values.get('AccountSid', ''))
    print("From: "+request.values.get('From', ''))
    # print("Date: "+request.values.get('dateCreated', ''))
    # print("AccountSid: "+request.values.get('Sid', ''))
    # print("ErrorMessage: "+request.values.get('ErrorMessage', ''))
    # print("Content: "+request.values.get('Body', ''))

    customermobno = request.values.get('From', '')
    start_index = customermobno.index('+')
    end_index = len(customermobno)
    # print("Incoming From : Start: {0} End: {1} ".format(start_index, end_index))

    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    greetings = """===============================================================
*வணக்கம் மதுரை மக்களே*
இது ஒரு தானியங்கி ஊடாடும் சேவை
*_முக்கிய அறிவிப்பு_*: 
மருத்துவம், தீ மற்றும் கொரோனா அவசர தேவைகளுக்கு
அரசு எண்களை தொடர்பு கொள்ளவும்.

மற்ற இதர சேவைகளுக்கு பின் வரும் பட்டியலில் இருந்து தேர்வு செய்க,

*Welcome people of Madurai*
This is an automated whatsapp chat bot
*_Warning_*: 
Please call government helpline numbers if you have
Medical, Fire or Corona related Emergency.

For other support kindly select from below choice,
===============================================================
*1* உணவு, காய்கறி, பழங்கள், மளிகை தேவைகள் / Food, Groceries
*2* மருத்துவ தேவைகள் [ இரத்தம், மருந்துகள் ] / Medical Supplies
*3* குடி நீர் தேவைகள் / Drinking Water Requirements
*4* மின் புகார் / Electricity Complaints
*5* சுகாதார குறைகள் / Sanitation Needs
*6* அவசர பயண கோரிக்கை / Emergency Travel Requests
*7* தங்கள் கோரிக்கையின் நிலை / Status of the Requests
*8* தன்னார்வலர்களாக பணியாற்ற விருப்பம் / Volunteer Registration
*9* எங்களை தொடர்புகொள்ள / Contact Us

தாங்கள் விரும்பும் சேவைக்கு நிகரான எண்ணை உள்ளீடு செய்க.
_உதாரணத்திற்கு_ மின் புகாருக்கு எண் 4 அழுத்தவும்

Kindly enter the number which corresponds to the needed support
_Example_: Press 4 if you want support in Electricity Complaints
===============================================================
"""
    requestreceived = """தங்கள் கோரிக்கை பதியப்பட்டது 
Your request is received"""
    inprogress = """இந்த வசதி கட்டுமானத்தில் உள்ளத்து 
This feature is in progress"""
    volunteerregistration = """தங்கள் ஆர்வத்திற்கு நன்றி! விரைவில் உங்கைளை தொடர்பு கொள்வோம் 
Thank you for your interest! You will hear from us shortly"""
    aboutus = """மதுரை தன்னார்வு சேவைகள்
Madurai Voluntary Services
+91 8220287172 / +91 8758410258
மென்பொறியாளர் தொடர்பு  / Developer Contact: 
+91 9943634523"""
    if incoming_msg.strip().isdigit():
        if int(incoming_msg.strip()) >= 1 and int(incoming_msg.strip()) <= 6:
            msg.body(requestreceived)
            update_db(customermobno, int(incoming_msg.strip()))
        if int(incoming_msg.strip()) == 7:
	        msg.body(inprogress)
	        update_db(customermobno,7)
        if int(incoming_msg.strip()) == 8:
	        msg.body(volunteerregistration)
	        update_db(customermobno,8)
        if '9' == incoming_msg:
	        msg.body(aboutus)
        if int(incoming_msg.strip()) >= 10:
            msg.body(greetings)
    else:
        msg.body(greetings)

    return str(resp)


def update_db(customermobno, category):
    db_connection = sqlite3.connect('lds.db')
    print("Opened database successfully")
    db_connection.execute("INSERT INTO CUSTOMERREQUEST (MOBILENO, CATEGORY, STATUS, TIMESTAMP) \
      VALUES (?, ?, ?, datetime('now', 'localtime'))", (customermobno, category, 1))
    db_connection.commit()
    print("Records inserted successfully")
    db_connection.close()

if __name__ == '__main__':
    app.run()
