

from flask import Flask, request, render_template , flash, redirect, url_for
import tkinter
from tkinter.ttk import *
from tkinter.filedialog import asksaveasfile 
from tkinter.filedialog import askopenfile 
#from nlp import ocr,nlp
from mongo import insert , present_or_not , get_field , get_employer_view , get_post , get_collection , delete_post
from send_mail import send_mail
from nlp1 import pdf_text,nlp1

app = Flask(__name__)   




@app.route('/', methods =["GET", "POST"])
def home_page():
    if request.method == "POST":
        if request.form["submit_button"] == "sign_up":            
        
            return redirect(url_for('sign_up'))
        elif request.form["submit_button"] == "login":
            post = {}
            post['email'] = request.form.get('email')       
            post['password'] = request.form.get('password') 
            if present_or_not(post,'employee') == 1:
                user_name = get_field(post,'first_name','employee')
                _id = get_field(post,'_id','employee')
                email = get_field(post,'email','employee')
                return redirect(url_for('employee',user_name =user_name , _id = _id,email = email))
        elif request.form["submit_button"] == "employer":
            return redirect(url_for('employer'))

        
    return render_template("home.html")

@app.route('/sign_up', methods =["GET", "POST"])
def sign_up():
    if request.method == "POST":
        post = {}
        post['email'] = request.form.get('email')
        post['first_name'] = request.form.get('firstName')
        post['password'] = request.form.get('password')    

        if present_or_not({'email':post['email'],'first_name':post['first_name']},'employee')==0:
            insert(post,'employee')
            return redirect(url_for('home_page' ))

            
    return render_template("sign_up.html")    

@app.route('/employee', methods =["GET", "POST"])
def employee():
    user_name=request.args.get('user_name')
    emp_id=request.args.get('_id')
    email=request.args.get('email')
    print(emp_id)
    recom_jobs = []
    if request.method == 'POST':
        if request.form["submit_button"] == "upload_resume":
            return redirect(url_for('upload_resume',user_name =user_name , emp_id = emp_id,email = email))
        else:
            return redirect(url_for('apply_job',user_name =user_name , emp_id = emp_id,email = email))
    return render_template("employee.html",recom_jobs = recom_jobs)

def comma_to_list(text):
    op = []
    text = text+'*'
    word = ''
    for i in text:
        if i!=',' and i!='*':
            word+=i
        else:
            op.append(word)
            word = ''
    return op

@app.route('/apply_job', methods =["GET", "POST"])
def apply_job():
    user_name=request.args.get('user_name')
    emp_id=request.args.get('emp_id')
    email=request.args.get('email')
    print(emp_id)
    print(user_name)
    resume = get_post(emp_id,'resume')
    jobs = get_collection('job')
    recom_jobs = []
    emp_skills = str(resume['Skills'])
    for job in jobs:
        job_skills = comma_to_list(job['skills'])
        for job_skill in job_skills:
            if job_skill!=',' and job_skill.lower() in str(emp_skills).lower():
                recom_jobs.append(job['job_name'])
                break
    
    if request.method == 'POST':
        post = {}
        post['Name'] = user_name
        post['email'] = email 
        post['skills'] = resume['Skills']
        post['Job name'] = request.form["submit_button"]
        insert(post,'job_applied')
    return render_template("employee.html",recom_jobs = recom_jobs) 
    

@app.route('/upload_resume', methods =["GET", "POST"])
def upload_resume():
    user_name=request.args.get('user_name')
    emp_id=request.args.get('emp_id')
    email=request.args.get('email')
    output = {}
    if request.method == "POST":
        f = request.files['file']
        f.save(f.filename)
        print("Extracting text...")
        text = pdf_text(f.filename)
        print("Text extracted...")
        print("Applying NLP...")
        output = nlp1(text)
        print("NLP completed...")
        post = {}
        post['_id'] = emp_id
        post['emp_name'] = user_name
        post['emp_email'] = email
        if present_or_not(post,'resume') == 0:
            post.update(output)
            insert(post,"resume")
        else:
            delete_post(post,'resume')
            post.update(output)
            insert(post,"resume")
        # if request.form["submit_button"] == "upload":
        #     file_path = askopenfile(mode ='r', filetypes =[('PDF Files', '*.pdf')]) 
            
            # return render_template("employee.html",user_name = user_name )
        
            

        
    return render_template("upload_resume.html",user_name = user_name , output = output)

@app.route('/employer', methods =["GET", "POST"])
def employer():
    if request.method == 'POST':
        if request.form["submit_button"] == "create_job":
            return redirect(url_for('create_job'))
        else:
            return redirect(url_for('select_emp'))
    return render_template("employer.html")

@app.route('/create_job', methods =["GET", "POST"])
def create_job():
    if request.method == "POST":
        post = {}
        post['job_name'] = request.form.get('job_name')
        post['job_descrip'] = request.form.get('job_descrip')
        post['skills'] = request.form.get('skills')   
        insert(post,'job')
        return redirect(url_for('employer'))
    return render_template("create_job.html")

@app.route('/select_emp', methods =["GET", "POST"])
def select_emp():
    applied_emps = get_collection('job_applied')
    output = {}
    for emps in applied_emps:
        if emps['Job name'] in output.keys():
            output[emps['Job name']].append(emps)
        else:
            output[emps['Job name']] = [emps]

    if request.method == "POST":
        # if request.form["submit_button"].count("select")>0:
        post = {}
        post['email'] = request.form["submit_button"]
        print(post)
        name = get_field(post,"Name","job_applied")
        email_id = get_field(post,"email","job_applied")
        job_name = get_field(post,"Job name","job_applied")
        send_mail(email_id,name,job_name)
    print(output)
    return render_template("select_emp.html",emps = output)
  
if __name__=='__main__':
   app.run()