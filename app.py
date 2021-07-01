from flask import Flask, request, render_template, flash, redirect, url_for
from login_gengee import scrape_flask, installed_files, clear_lis, get_files_info, check_interruption, false_interruption
from sn_email import send_email
import multiprocessing
import psutil
import pickle
import time
import requests
import json
import os


SECRET_KEY = "I`q\x89|q\xf7\xb9\xd7\x17\xb8H\x94I\x82\xdc\x92\xcc~\xa5\xacPL\xaa"
app = Flask(__name__)
app.secret_key = SECRET_KEY



is_created = os.path.exists("Stats")
if is_created:
    pass
else:
    os.mkdir("Stats")


creds = []



all_users = {
    "Forward Football" : {
        "Password" : "admin123",
    }
}



curr = {
    "username" : {
        "curr_user" : "",
        "curr_auth" : False
    }
}


loaded_dates_match = pickle.load(open("MatchDates.sav", 'rb'))
loaded_dates_train = pickle.load(open("TrainDates.sav", 'rb'))



#REMOVE BEFORE FINAL DELIVERY ##########################################################################################
site_key = "6LcVf9sUAAAAAI6numLdLknFPLXFSPbYsCqZqHnY"
def is_human(captcha_response):
    secret = "6LcVf9sUAAAAACfP-vD3sAdQnRWBn_fFLEeCsjdX"
    payload = {'response':captcha_response, 'secret':secret}
    response = requests.post("https://www.google.com/recaptcha/api/siteverify", payload)
    response_text = json.loads(response.text)
    return response_text['success']
#REMOVE BEFORE FINAL DELIVERY ##########################################################################################




@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if curr["username"]["curr_auth"]:
        flash("You're already logged in!", "warning")
        return redirect(url_for("home"))
    else:
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            captcha_response = request.form['g-recaptcha-response']
            if is_human(captcha_response):
                if username in all_users:
                    if password == all_users[username]["Password"]:
                        flash("You've successfully logged in!", "success")

                        curr["username"]["curr_user"] = username
                        curr["username"]["curr_auth"] = True

                        return redirect(url_for('home'))
                    else:
                        flash("Incorrect password!", "warning")
                else:
                    flash("Incorrect username!", "warning")
            else:
                flash("Only humans allowed! Complete reCAPTCHA check!", "warning")


        
    return render_template("login.html", sitekey=site_key)



@app.route("/logout")
def logout():
    curr["username"]["curr_user"] = ""
    curr["username"]["curr_auth"] = False
    flash("You've successfully logged out!", "success")
    return redirect(url_for("login"))




@app.route("/home", methods=["GET", "POST"])
def home():
    if curr["username"]["curr_auth"]:
        if request.method == 'POST':
            if len(creds) == 0:

                username = curr["username"]["curr_user"]
                creds.append(username)

                password = all_users[username]["Password"]
                creds.append(password)

                teamname = request.form.get('teamname')
                creds.append(teamname)

                mat_trn = request.form.get('matr')
                creds.append(mat_trn)

                browser = request.form.get('browser')
                creds.append(browser)

                date = request.form.get('date')
                creds.append(date)

                date1 = request.form.get('date1')
                creds.append(date1)

                mode = request.form.get('mode')
                creds.append(mode)

            else:

                username = curr["username"]["curr_user"]
                creds[0] = username

                password = all_users[username]["Password"]
                creds[1] = password

                teamname = request.form.get('teamname')
                creds[2] = teamname

                mat_trn = request.form.get('matr')
                creds[3] = mat_trn

                browser = request.form.get('browser')
                creds[4] = browser

                date = request.form.get('date')
                creds[5] = date

                date1 = request.form.get('date1')
                creds[5] = date1

                mode = request.form.get('mode')
                creds[6] = mode
            

            scrape_flask(username, password, teamname, mat_trn, browser, date, date1, mode)
            if check_interruption():
                flash("Process was manually interrupted by user!", "warning")
                false_interruption()
            else:
                list_files = installed_files()
                nr = len(list_files)
                

                if nr == 0:
                    flash(str(nr) + " installed! Query returned empty or all files already installed!", "warning")
                else:
                    flash("Successfully installed " + str(nr) + " files", "success")
                    clear_lis()


            

    else:
        flash("Please login first!", 'warning')
        return redirect(url_for("login"))

    return render_template("index.html", date=loaded_dates_match, len=len(loaded_dates_match), date1=loaded_dates_train, len1=len(loaded_dates_train))




def countdown(set_time, credLis):
    while set_time:
        mins, secs = divmod(set_time, 60)
        hrs, mins = divmod(mins, 60)
        timer = '{:02d}:{:02d}:{:02d}'.format(hrs, mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        set_time -= 1
        if set_time == 0:
            break
    scrape_flask(credLis[0], credLis[1], credLis[2], credLis[3], credLis[4], credLis[5], credLis[6], credLis[7])



numOfProcesses = []


@app.route("/timer", methods=["GET", "POST"])
def timer():
    if curr["username"]["curr_auth"]:
        repBol = True
        if request.method == 'POST':
            period = int(request.form.get('period'))
            repeat = request.form.get('repeat')

            if (len(creds) != 0):

                if repeat == "yes":

                    if len(numOfProcesses) == 0:
                        start_count = multiprocessing.Process(target=countdown, args=(period, creds, ))
                        start_count.start()
                        numOfProcesses.append(str(start_count))
                        while repBol:
                            indexis = numOfProcesses[0][26:-1].index("=")
                            indexSpace = numOfProcesses[0][26:-1].index(" ")
                            pid = int(numOfProcesses[0][26:-1][indexis+1:indexSpace])
                            running_proc = psutil.pid_exists(pid)
                            if running_proc:
                                pass
                            else:
                                del numOfProcesses[0]
                                start_count = multiprocessing.Process(target=countdown, args=(period, creds, ))
                                start_count.start()
                                numOfProcesses.append(str(start_count))

                    else:
                        indexis = numOfProcesses[0][26:-1].index("=")
                        indexSpace = numOfProcesses[0][26:-1].index(" ")
                        pid = int(numOfProcesses[0][26:-1][indexis+1:indexSpace])

                        
                        try:
                            p = psutil.Process(pid)
                            p.terminate()
                            del numOfProcesses[0]
                        except psutil.NoSuchProcess:
                            del numOfProcesses[0]

                        start_count = multiprocessing.Process(target=countdown, args=(period, creds, ))
                        start_count.start()
                        numOfProcesses.append(str(start_count))
                        while repBol:
                            indexis = numOfProcesses[0][26:-1].index("=")
                            indexSpace = numOfProcesses[0][26:-1].index(" ")
                            pid = int(numOfProcesses[0][26:-1][indexis+1:indexSpace])
                            running_proc = psutil.pid_exists(pid)
                            if running_proc:
                                pass
                            else:
                                del numOfProcesses[0]
                                start_count = multiprocessing.Process(target=countdown, args=(period, creds, ))
                                start_count.start()
                                numOfProcesses.append(str(start_count))

                else:
                    if len(numOfProcesses) == 0:
                        start_count = multiprocessing.Process(target=countdown, args=(period, creds, ))
                        start_count.start()
                        numOfProcesses.append(str(start_count))

                    else:
                        indexis = numOfProcesses[0][26:-1].index("=")
                        indexSpace = numOfProcesses[0][26:-1].index(" ")
                        pid = int(numOfProcesses[0][26:-1][indexis+1:indexSpace])

                        try:
                            p = psutil.Process(pid)
                            p.terminate()
                            del numOfProcesses[0]
                        except psutil.NoSuchProcess:
                            del numOfProcesses[0]

                        start_count = multiprocessing.Process(target=countdown, args=(period, creds, ))
                        start_count.start()
                        numOfProcesses.append(str(start_count))


                if period == 5:
                    flash("Timer has been successfully set. Data will be fetched over 5 Seconds", "success")
                elif period == 120:
                    flash("Timer has been successfully set. Data will be fetched over 2 Minutes", "success")
                elif period == 18000:
                    flash("Timer has been successfully set. Data will be fetched over 5 Hours", "success")
                elif period == 36000:
                    flash("Timer has been successfully set. Data will be fetched over 10 Hours", "success")
                elif period == 54000:
                    flash("Timer has been successfully set. Data will be fetched over 15 Hours", "success")
                elif period == 72000:
                    flash("Timer has been successfully set. Data will be fetched over 20 Hours", "success")
                else:
                    flash("Timer has been successfully set. Data will be fetched over 24 Hours", "success")
            else:
                flash("Insert Team Name, Data type and browser", "warning")
    

    else:
        flash("Please login first!", 'warning')
        return redirect(url_for("login"))
    return render_template("timer.html")


@app.route("/terminate", methods=["GET", "POST"])
def terminator():
    if curr["username"]["curr_auth"]:
        if request.method == 'POST':
            if len(numOfProcesses) == 0:
                flash("There are no active timers!", 'warning')
            else:
                indexis = numOfProcesses[0][26:-1].index("=")
                indexSpace = numOfProcesses[0][26:-1].index(" ")
                pid = int(numOfProcesses[0][26:-1][indexis+1:indexSpace])
                try:
                    p = psutil.Process(pid)
                    p.terminate()
                    flash("Timer with PID " + str(pid) +" Has been successfully terminated!", "success")
                    del numOfProcesses[0]
                except psutil.NoSuchProcess:
                    flash("There are no active timers!", 'warning')
                    del numOfProcesses[0]
    else:
        flash("Please login first!", 'warning')
        return redirect(url_for("login"))
    return render_template("term.html")



@app.route("/contact", methods=["GET", "POST"])
def contact():
    if curr["username"]["curr_auth"]:
            if request.method == 'POST':
                name = request.form.get('name')
                email = request.form.get('email')
                subject = request.form.get('subject')
                msg = request.form.get('msg')
                try:
                    send_email(name, email, subject, msg)
                    flash("E-mail sent successfully", 'success')
                except:
                    flash("E-mail couldn't be sent! Try again..", 'warning')
    else:
        flash("Please login first!", 'warning')
        return redirect(url_for("login"))
    return render_template("contact.html")


@app.route("/downloads", methods=["GET"])
def downloads():
    if curr["username"]["curr_auth"]:
        downloaded_files_info = get_files_info()
        len_downloaded = len(downloaded_files_info)
        if len_downloaded == 0:
            return render_template("fils.html", len=len_downloaded)
        else:
            len_downloaded1 = len(downloaded_files_info[0])
            return render_template("fils.html", data=downloaded_files_info, len=len_downloaded, len1=len_downloaded1)
    else:
        flash("Please login first!", 'warning')
        return redirect(url_for("login"))



@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True, port=80, host="192.168.1.120"
    )