from flask import Flask,render_template,url_for,session,redirect,request
import re,sendgrid
from sendgrid.helpers.mail import *
import db
from db import ibm_db
app = Flask(__name__)
app.secret_key="1123"
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=55fbc997-9266-4331-afd3-888b05e734c0.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT= 31929;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=hdr83116;PWD=Tbz8J811msiJ4U38",'','')
# index page starts-----------------------------
@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/log_in")
def login():
    return render_template("log_in.html")
#index page ends---------------------------------

# sendgrid integration
#donor registration starts----------------------------------------
def mailtest_registration(to_email):
    sg = sendgrid.SendGridAPIClient(api_key= '' )
    from_email = Email("itaswinic@gmail.com")
    subject = "Registered Successfull as a DONOR!"
    content = Content("text/plain", "You have successfully registered as donor. Please Login using your Username and Password to donate Plasma.")
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)

#donor registration ends----------------------------------------

#hospital registration starts----------------------------------------
def mailtest_hosp_registration(to_email):
    sg = sendgrid.SendGridAPIClient(api_key= '' )
    from_email = Email("itaswinic@gmail.com")
    subject = "Registered Successfull as a Hospital!"
    content = Content("text/plain", "You have successfully registered as recipient. Please Login using your Username and Password to request Plasma.")
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)

#hospital registration ends----------------------------------------

#request plasma confirmation mail starts-----------------------------------
def mailtest_request_plasma(to_email):
    sg = sendgrid.SendGridAPIClient(api_key= '' )
    from_email = Email("itaswinic@gmail.com")
    subject = "Successfully registered to request plasma!"
    content = Content("text/plain", "You have successfully registered to request plasma. our admin will connect you shortly with donor details")
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)

#request plasma confirmation mail ends-----------------------------------
