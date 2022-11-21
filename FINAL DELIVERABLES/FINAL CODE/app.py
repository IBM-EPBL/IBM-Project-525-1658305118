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

#donor login starts--------------------------------------

@app.route("/login_donor",methods=['GET','POST'])
def login_donor():
    global userid
    msg = ''
    if request.method == 'POST' :
        donor_name = request.form['donor_name']
        donor_password = request.form['donor_password']
        sql = "SELECT * FROM donors_details WHERE donor_name =? AND donor_password=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,donor_name)
        ibm_db.bind_param(stmt,2,donor_password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print (account)
        if account:
            session['loggedin'] = True
            session['id'] = account['DONOR_NAME']
            userid=  account['DONOR_NAME']
            session['donor_name'] = account['DONOR_NAME']
            msg = 'Logged in successfully as donor!'
            
            return render_template('homepage_donor.html', msg = msg)
        else:
            msg = 'Incorrect email / password !'
    return render_template("login_donor.html")

#donor login ends------------------------------------------


#sign up donor starts------------------------------------

@app.route("/signup_donor")
def signup_donor():
    return render_template("signup_donor.html")

@app.route("/donor_form", methods=['GET','POST'])
def donor_form():
    msg = ''
    if request.method == 'POST' :
        donor_name = request.form['donor_name']
        date_of_birth = request.form['date_of_birth']
        age = request.form['age']
        donor_gender = request.form['donor_gender']
        donor_blood_group = request.form['donor_blood_group']
        donor_address = request.form['donor_address']
        donor_city = request.form['donor_city']
        donor_state = request.form['donor_state']
        donor_email = request.form['donor_email']
        donor_password = request.form['donor_password']
        sql = "SELECT * FROM donors_details WHERE donor_name =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,donor_name)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', donor_email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', donor_name):
            msg = 'name must contain only characters and numbers !'
        else:
            mailtest_registration(donor_email)
            insert_sql = "INSERT INTO donors_details VALUES (?, ?, ?, ?,?,?,?,?,?,?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, donor_name)
            ibm_db.bind_param(prep_stmt, 2, date_of_birth)
            ibm_db.bind_param(prep_stmt, 3, age)
            ibm_db.bind_param(prep_stmt, 4, donor_gender)
            ibm_db.bind_param(prep_stmt, 5, donor_blood_group)
            ibm_db.bind_param(prep_stmt,6, donor_address)
            ibm_db.bind_param(prep_stmt, 7, donor_city)
            ibm_db.bind_param(prep_stmt, 8, donor_state)
            ibm_db.bind_param(prep_stmt, 9, donor_email)
            ibm_db.bind_param(prep_stmt, 10, donor_password)
           
            ibm_db.execute(prep_stmt)
            msg = 'You have successfully registered as donor!'
           
        return render_template('login_donor.html', msg = msg)
        
#sign up donor ends-----------------------------------------

# login hospital--------------------------------------------

@app.route("/login_hospital", methods=['GET','POST'] )
def login_hospital():
    msg = ''
    if request.method == 'POST' :
        hospital_name = request.form['hospital_name']
        hospital_password = request.form['hospital_password']
        sql = "SELECT * FROM hospitals_details WHERE hospital_name =? AND hospital_password=?"
        stmt = ibm_db.prepare(db.conn, sql)
        ibm_db.bind_param(stmt,1,hospital_name)
        ibm_db.bind_param(stmt,2,hospital_password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print (account)
        if account:
            session['loggedin'] = True
            session['id'] = account['HOSPITAL_NAME']
            userid=  account['HOSPITAL_NAME']
            session['hospital_name'] = account['HOSPITAL_NAME']
            msg = 'Logged in successfully as recipient!'
            return render_template('donors.html', msg = msg)
        else:
            msg = 'Incorrect email / password !'       
    return render_template('login_hospital.html', msg = msg)

#sign up hospital starts----------------------------------------------
        
@app.route("/signup_hospital",methods=['GET','POST'])
def signup_hospital():
    msg = ''
    if request.method == 'POST' :
        hospital_name = request.form['hospital_name']
        hospital_date = request.form['hospital_date']
        hospital_contact_number = request.form['hospital_contact_number']
        hospital_address = request.form['hospital_address']
        hospital_city = request.form['hospital_city']
        hospital_state = request.form['hospital_state']
        hospital_email = request.form['hospital_email']
        hospital_password = request.form['hospital_password']
        sql = "SELECT * FROM hospitals_details WHERE hospital_name =?"
        stmt = ibm_db.prepare(db.conn, sql)
        ibm_db.bind_param(stmt,1,hospital_name)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', hospital_email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', hospital_name):
            msg = 'name must contain only characters and numbers !'
        else:
            mailtest_hosp_registration(hospital_email)
            insert_sql = "INSERT INTO hospitals_details VALUES (?, ?, ?, ?,?,?,?,?)"
            prep_stmt = ibm_db.prepare(db.conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, hospital_name)
            ibm_db.bind_param(prep_stmt, 2, hospital_date)
            ibm_db.bind_param(prep_stmt, 3, hospital_contact_number)
            ibm_db.bind_param(prep_stmt, 4, hospital_address)
            ibm_db.bind_param(prep_stmt, 5, hospital_city)
            ibm_db.bind_param(prep_stmt, 6, hospital_state)
            ibm_db.bind_param(prep_stmt, 7, hospital_email)
            ibm_db.bind_param(prep_stmt, 8, hospital_password)
           
            ibm_db.execute(prep_stmt)
            msg = 'You have successfully registered as recipient!'
            # mailtest(usermail)
            return render_template('login_hospital.html', msg = msg)
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template("signup_hospital.html")

#sign up hospital ends-----------------------------------------------------


#donor list table starts------------------------------------------------------------
@app.route('/donorlist')
def donorlist():
    donors_details = []
    sql = "SELECT * FROM DONORS_DETAILS"
    stmt = ibm_db.exec_immediate(db.conn, sql)
    dictionary = ibm_db.fetch_both(stmt)
    while dictionary != False:
        donors_details.append(dictionary)
        dictionary = ibm_db.fetch_both(stmt)
    if donors_details:
        return render_template("homepage_hospital.html", donors_details = donors_details)

#donor list table endss------------------------------------------------------------


#request plasma-----------------------------------------------------------------

@app.route("/request_plasma",methods=['GET','POST'])
def request_plasma():
    msg = ''
    if request.method == 'POST' :
        hospital_name = request.form['hospital_name']
        hospital_contact_number = request.form['hospital_contact_number']
        patient_name = request.form['patient_name']
        patient_age = request.form['patient_age']
        patient_blood_group = request.form['patient_blood_group']
        cause_of_plasma = request.form['cause_of_plasma']
        hospital_address = request.form['hospital_address']
        hospital_city = request.form['hospital_city']
        hospital_state = request.form['hospital_state']
        hospital_email = request.form['hospital_email']
        sql = "SELECT * FROM request_hospital_details WHERE hospital_name =?"
        stmt = ibm_db.prepare(db.conn, sql)
        ibm_db.bind_param(stmt,1,hospital_name)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', hospital_email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', hospital_name):
            msg = 'name must contain only characters and numbers !'
        else:
            mailtest_request_plasma(hospital_email)
            insert_sql = "INSERT INTO request_hospital_details VALUES (?, ?, ?, ?,?,?,?,?,?,?)"
            prep_stmt = ibm_db.prepare(db.conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, hospital_name)
            ibm_db.bind_param(prep_stmt, 2, hospital_contact_number)
            ibm_db.bind_param(prep_stmt, 3, patient_name)
            ibm_db.bind_param(prep_stmt, 4, patient_age)
            ibm_db.bind_param(prep_stmt, 5, patient_blood_group)
            ibm_db.bind_param(prep_stmt, 6, cause_of_plasma)
            ibm_db.bind_param(prep_stmt, 7, hospital_address)
            ibm_db.bind_param(prep_stmt, 8, hospital_city)
            ibm_db.bind_param(prep_stmt, 9, hospital_state)
            ibm_db.bind_param(prep_stmt, 10, hospital_email)
            ibm_db.execute(prep_stmt)
            msg = 'You have successfully registered to request plasma. our admin will connect you shortly with donor details!'
            # mailtest(usermail)
            return render_template('success.html', msg = msg)
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template("request_plasma.html")


# sendgrid integration
#donor registration starts----------------------------------------
def mailtest_registration(to_email):
    sg = sendgrid.SendGridAPIClient(api_key='')
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

@app.route('/index')
def index():
    session.clear()
    return render_template("index.html")


if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000, debug=True)
