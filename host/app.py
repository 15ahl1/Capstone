from flask import Flask, render_template, url_for, flash, redirect, request
from flask_wtf import FlaskForm
from forms import *
from flask_mysqldb import MySQL
import yaml
import json
import os
import io
import datetime
import pandas


app = Flask(__name__)

# Configure db
db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['SECRET_KEY'] = os.urandom(24)
app.config['MYSQL_DB'] = db['mysql_db']
mysql = MySQL(app)

uploads_dir = os.path.join(app.instance_path, 'uploads')

# All routing
@app.route('/')
def index():
    return home()


@app.route('/home.html', methods=['GET', 'POST',  'PUT'])
def home():
    machines = []
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM machines")
    machines = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    return render_template("/home.html", machines=machines)


@app.route('/time.html', methods=['GET', 'POST',  'PUT'])
def timeFunction():
    # form = userTime()
    default_name = ''
    name = request.args.get('userName', default_name)
    default_date = ''
    date = request.args.get('date', default_date)
    default_machine = ''
    machine = request.args.get('machineNumber', default_machine)
    return timeHelper(name, date, machine)


def timeHelper(name, date, machine):
    value1 = 1
    value2 = 2
    value3 = 3
    value4 = 4
    value5 = 5
    value6 = 6
    value7 = 7
    units = "Number of Hours of Machine Use"
    if name != '':
        currentDate = datetime.date.today()
        yesterday = currentDate - datetime.timedelta(days=1)
        twoDays = currentDate - datetime.timedelta(days=2)
        threeDays = currentDate - datetime.timedelta(days=3)
        fourDays = currentDate - datetime.timedelta(days=4)
        fiveDays = currentDate - datetime.timedelta(days=5)
        sixDays = currentDate - datetime.timedelta(days=6)
        label1 = sixDays.strftime("%A") + " " + str(sixDays.day)
        label2 = fiveDays.strftime("%A") + " " + str(fiveDays.day)
        label3 = fourDays.strftime("%A") + " " + str(fourDays.day)
        label4 = threeDays.strftime("%A") + " " + str(threeDays.day)
        label5 = twoDays.strftime("%A") + " " + str(twoDays.day)
        label6 = yesterday.strftime("%A") + " " + str(yesterday.day)
        label7 = currentDate.strftime("%A") + " " + str(currentDate.day)
    elif date != '':
        label1 = "Machine 1"
        label2 = "Machine 2"
        label3 = "Machine 3"
        label4 = "Machine 4"
        label5 = "Machine 5"
        label6 = "Machine 6"
        label7 = "Machine 7"
    elif machine != '':
        currentDate = datetime.date.today()
        yesterday = currentDate - datetime.timedelta(days=1)
        twoDays = currentDate - datetime.timedelta(days=2)
        threeDays = currentDate - datetime.timedelta(days=3)
        fourDays = currentDate - datetime.timedelta(days=4)
        fiveDays = currentDate - datetime.timedelta(days=5)
        sixDays = currentDate - datetime.timedelta(days=6)
        label1 = sixDays.strftime("%A") + " " + str(sixDays.day)
        label2 = fiveDays.strftime("%A") + " " + str(fiveDays.day)
        label3 = fourDays.strftime("%A") + " " + str(fourDays.day)
        label4 = threeDays.strftime("%A") + " " + str(threeDays.day)
        label5 = twoDays.strftime("%A") + " " + str(twoDays.day)
        label6 = yesterday.strftime("%A") + " " + str(yesterday.day)
        label7 = currentDate.strftime("%A") + " " + str(currentDate.day)
    else:
        currentDate = datetime.date.today()
        yesterday = currentDate - datetime.timedelta(days=1)
        twoDays = currentDate - datetime.timedelta(days=2)
        threeDays = currentDate - datetime.timedelta(days=3)
        fourDays = currentDate - datetime.timedelta(days=4)
        fiveDays = currentDate - datetime.timedelta(days=5)
        sixDays = currentDate - datetime.timedelta(days=6)
        label1 = sixDays.strftime("%A") + " " + str(sixDays.day)
        label2 = fiveDays.strftime("%A") + " " + str(fiveDays.day)
        label3 = fourDays.strftime("%A") + " " + str(fourDays.day)
        label4 = threeDays.strftime("%A") + " " + str(threeDays.day)
        label5 = twoDays.strftime("%A") + " " + str(twoDays.day)
        label6 = yesterday.strftime("%A") + " " + str(yesterday.day)
        label7 = currentDate.strftime("%A") + " " + str(currentDate.day)

    return render_template('time.html', units=units, label1=label1,
    label2=label2, label3=label3, label4=label4, label5=label5, label6=label6,
    label7=label7, value1=value1, value2=value2, value3=value3, value4=value4,
    value5=value5, value6=value6, value7=value7)


@app.route('/addUser.html', methods=['GET', 'POST',  'PUT'])
def userFunction():
    form = makeNewUser()
    cur = mysql.connection.cursor()
    supers = cur.execute("SELECT superName, superName FROM supervisors")
    supers = cur.fetchall()
    dept = cur.execute("SELECT deptName, deptName FROM departments")
    dept = cur.fetchall()
    faculty = cur.execute("SELECT facultyName, facultyName FROM faculty")
    faculty = cur.fetchall()
    institution = cur.execute(
        "SELECT institutionName, institutionName FROM institution")
    institution = cur.fetchall()
    rate = cur.execute("SELECT rateAmount, rateName FROM rateType")
    rate = cur.fetchall()
    form.supervisor.choices = supers
    form.department.choices = dept
    form.faculty.choices = faculty
    form.institution.choices = institution
    form.rateType.choices = rate
    if request.method == "POST":
        permissionString = ""
        if(form.perMac1.data == True):
            permissionString += "1"
        else:
            permissionString += "0"

        if(form.perMac2.data == True):
            permissionString += "1"
        else:
            permissionString += "0"

        if(form.perMac3.data == True):
            permissionString += "1"
        else:
            permissionString += "0"

        if(form.perMac4.data == True):
            permissionString += "1"
        else:
            permissionString += "0"

        if(form.perMac5.data == True):
            permissionString += "1"
        else:
            permissionString += "0"

        if(form.perMac6.data == True):
            permissionString += "1"
        else:
            permissionString += "0"

        if(form.perMac7.data == True):
            permissionString += "1"
        else:
            permissionString += "0"
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(username, userPin, supervisor, department, faculty, institution, rateType, Permissions) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", ([form.userName.data, form.userPin.data, form.supervisor.data, form.department.data, form.faculty.data, form.institution.data, form.rateType.data, permissionString]))
        mysql.connection.commit()
        cur.close()
        return redirect('addUser.html')
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM users")
    userDetails = cur.fetchall()
    return render_template('addUser.html', form=form, userDetails=userDetails)


@app.route('/configure.html', methods=['GET', 'POST',  'PUT'])
def configure():
    superForm = newSupervisor()
    deptForm = newDepartment()
    facultyForm = newFaculty()
    institutionForm = newInstitution()
    rateForm = newRateType()
    if request.method == "POST":
        try:
            request.form['superName']
            cur = mysql.connection.cursor()
            superName = superForm.superName.data
            cur.execute(
                "INSERT INTO supervisors (superName) VALUES (%s)", ([superName]))
            mysql.connection.commit()
            cur.close()
            return redirect("/configure.html")
        except:
            pass
        try:
            request.form['deptName']
            cur = mysql.connection.cursor()
            deptName = deptForm.deptName.data
            cur.execute(
                "INSERT INTO departments (deptName) VALUES (%s)", ([deptName]))
            mysql.connection.commit()
            cur.close()
            return redirect("/configure.html")
        except:
            pass
        try:
            request.form['facultyName']
            cur = mysql.connection.cursor()
            facultyName = facultyForm.facultyName.data
            cur.execute(
                "INSERT INTO faculty (facultyName) VALUES (%s)", ([facultyName]))
            mysql.connection.commit()
            cur.close()
            return redirect("/configure.html")
        except:
            pass
        try:
            request.form['institutionName']
            cur = mysql.connection.cursor()
            institutionName = institutionForm.institutionName.data
            cur.execute(
                "INSERT INTO institution (institutionName) VALUES (%s)", ([institutionName]))
            mysql.connection.commit()
            cur.close()
            return redirect("/configure.html")
        except:
            pass
        try:
            request.form['rateTypeName']
            cur = mysql.connection.cursor()
            rateTypeName = rateForm.rateTypeName.data
            rateAmount = rateForm.rateAmount.data
            cur.execute("INSERT INTO rateType (rateName, rateAmount) VALUES (%s, %s)", ([
                        rateTypeName, rateAmount]))
            mysql.connection.commit()
            cur.close()
            return redirect("/configure.html")
        except:
            pass
    cur = mysql.connection.cursor()
    supers = cur.execute("SELECT * FROM supervisors")
    supers = cur.fetchall()
    dept = cur.execute("SELECT * FROM departments")
    dept = cur.fetchall()
    faculty = cur.execute("SELECT * FROM faculty")
    faculty = cur.fetchall()
    institution = cur.execute("SELECT * FROM institution")
    institution = cur.fetchall()
    rate = cur.execute("SELECT * FROM rateType")
    rate = cur.fetchall()
    return render_template("/configure.html",
    supers=supers, dept=dept, faculty=faculty, institution=institution,
    rate=rate,superForm=superForm, deptForm=deptForm, facultyForm=facultyForm,
    institutionForm=institutionForm, rateForm=rateForm)


@app.route('/reports.html', methods=['GET', 'POST',  'PUT'])
def reportFunction():
    cur = mysql.connection.cursor()
    supers = cur.execute("SELECT * FROM supervisors")
    supers = cur.fetchall()
    dept = cur.execute("SELECT * FROM departments")
    dept = cur.fetchall()
    faculty = cur.execute("SELECT * FROM faculty")
    faculty = cur.fetchall()
    institution = cur.execute("SELECT * FROM institution")
    institution = cur.fetchall()
    rate = cur.execute("SELECT * FROM rateType")
    rate = cur.fetchall()
    return render_template("/reports.html",
    supers=supers, dept=dept, faculty=faculty, institution=institution, rate=rate)


# All report upload to database files
@app.route("/uploadSuper", methods=["POST"])
def uploadSuper():
    file = request.files['uploadSuper']
    file.save('instance/uploads/Supervisors_file.xlsx')
    answers = pandas.read_excel(file)
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM supervisors")
    for item in answers['superName']:
        cur.execute(
            "INSERT INTO supervisors (superName) VALUES (%s)", ([item]))
    mysql.connection.commit()
    cur.close()
    return redirect("/reports.html")

@app.route("/uploadDepartments", methods=["POST"])
def uploadDepartments():
    file = request.files['uploadDepartments']
    file.save('instance/uploads/Departments_file.xlsx')
    answers = pandas.read_excel(file)
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM departments")
    for item in answers['deptName']:
        cur.execute(
            "INSERT INTO departments (deptName) VALUES (%s)", ([item]))
    mysql.connection.commit()
    cur.close()
    return redirect("/reports.html")

@app.route("/uploadFaculty", methods=["POST"])
def uploadFaculty():
    file = request.files['uploadFaculty']
    file.save('instance/uploads/Faculty_file.xlsx')
    answers = pandas.read_excel(file)
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM faculty")
    for item in answers['facultyName']:
        cur.execute(
            "INSERT INTO faculty (facultyName) VALUES (%s)", ([item]))
    mysql.connection.commit()
    cur.close()
    return redirect("/reports.html")

@app.route("/uploadInstitution", methods=["POST"])
def uploadInstitution():
    file = request.files['uploadInstitution']
    file.save('instance/uploads/Institution_file.xlsx')
    answers = pandas.read_excel(file)
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM institution")
    for item in answers['institutionName']:
        cur.execute(
            "INSERT INTO institution (institutionName) VALUES (%s)", ([item]))
    mysql.connection.commit()
    cur.close()
    return redirect("/reports.html")

@app.route("/uploadRateType", methods=["POST"])
def uploadRateType():
    file = request.files['uploadRateType']
    file.save('instance/uploads/RateType_file.xlsx')
    answers = pandas.read_excel(file)
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM rateType")
    names = answers['rateName']
    rates = answers['rateAmount']
    for x in range(0,names.size-1):
        cur.execute("INSERT INTO rateType (rateName, rateAmount) VALUES (%s, %s)", ([names[x], rates[x]]))
    mysql.connection.commit()
    cur.close()
    return redirect("/reports.html")


@app.route("/uploadUsers", methods=["POST"])
def uploadUsers():
    file = request.files['uploadUsers']
    file.save('instance/uploads/Users_file.xlsx')
    answers = pandas.read_excel(file)
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Users")
    for item1,item2 in answers['rateType']:
        cur.execute(
            "INSERT INTO rateType (rateName, rateAmount) VALUES (%s, %s)", ([item1, item2]))
    mysql.connection.commit()
    cur.close()
    return redirect("/reports.html")




# All report downloads to database files
@app.route("/downloadSuper", methods=["POST"])
def downloadSuper():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM supervisors')
    pandaDataFrame = pandas.DataFrame(cur.fetchall())
    pandaDataFrame.to_excel('instance/download.Supervisors_file.xlsx')
    mysql.connection.commit()
    cur.close()
    return redirect("/reports.html")


# All functions to delete things such as users, supers, institutions
@app.route('/deleteUser/<string:userIdentificationNumber>')
def deleteUser(userIdentificationNumber):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users where userID=" +
                str(userIdentificationNumber))
    mysql.connection.commit()
    cur.close()
    form = makeNewUser()
    return redirect("/addUser.html")


@app.route('/deleteSuper/<string:superIdentificationNumber>')
def deleteSuper(superIdentificationNumber):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM supervisors where superID=" +
                str(superIdentificationNumber))
    mysql.connection.commit()
    cur.close()
    return redirect("/configure.html")


@app.route('/deleteDepartment/<string:deptIdentificationNumber>')
def deleteDepartment(deptIdentificationNumber):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM departments where deptID=" +
                str(deptIdentificationNumber))
    mysql.connection.commit()
    cur.close()
    return redirect("/configure.html")


@app.route('/deleteFaculty/<string:facultyIdentificationNumber>')
def deleteFaculty(facultyIdentificationNumber):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM faculty where facultyID=" +
                str(facultyIdentificationNumber))
    mysql.connection.commit()
    cur.close()
    return redirect("/configure.html")


@app.route('/deleteInstitution/<string:institutionIdentificationNumber>')
def deleteInstitution(institutionIdentificationNumber):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM institution where institutionID=" +
                str(institutionIdentificationNumber))
    mysql.connection.commit()
    cur.close()
    return redirect("/configure.html")


@app.route('/deleteRate/<string:rateIdentificationNumber>')
def deleteRate(rateIdentificationNumber):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM rateType where rateID=" +
                str(rateIdentificationNumber))
    mysql.connection.commit()
    cur.close()
    return redirect("/configure.html")


def writeUsageRecord(machine, time, userID):
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO entries (machine,timeUsed, userID, inUse) VALUES (%s, %s, %s, %s);",
                    (machine, time, userID, str(1)))
        mysql.connection.commit()
        cur.close()


def machineStatus(machine):
    print("Updating machine status...")
    with app.app_context():
        cur = mysql.connection.cursor()
        select_stmt = "SELECT inUse FROM machines WHERE machine = %(machine)s"
        cur.execute(select_stmt, {'machine': machine})
        status = cur.fetchone()
        print(status)
        print("The machine status is " + str(status[0]))
        if status[0] == 0:
            update_stmt = "UPDATE machines SET inUse = '1' WHERE machine = %(machine)s"
            cur.execute(update_stmt, {'machine': machine})
        else:
            update_stmt = "UPDATE machines SET inUse = '0' WHERE machine = %(machine)s"
            cur.execute(update_stmt, {'machine': machine})
        mysql.connection.commit()
        cur.close()
