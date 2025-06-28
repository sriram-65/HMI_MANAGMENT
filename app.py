from flask import Flask , redirect , flash , request , render_template , jsonify , url_for , session
from flask_cors import CORS
from flask_mail import Mail , Message
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime , timedelta
import cloudinary.uploader
import cloudinary
import random
import datetime



app = Flask(__name__)

app.secret_key = "HMI"
clint = MongoClient("mongodb+srv://sriram65raja:1324sriram@cluster0.dejys.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'sriram65raja@gmail.com'
app.config['MAIL_PASSWORD'] = 'akio rluw wwup kfbc'  

mail = Mail(app)
HMI = clint['ai']

EMPLOYEE_REGISTER = HMI["EMPLOYEE_REGISTER"]
CLINET_DATILS = HMI["CLINET_DATILS"]
ACCEPTED_LIST = HMI['ACCEPTED_LIST']
DEVELOPER_LIST = HMI["DEVELOPER_LIST"]
RE_REQUESTED = HMI["RE_REQUESTED"]
MEASSAGES = HMI["MEASSAGES"]

cloudinary.config(
    cloud_name="dbrmvywb0",
    api_key="799647841433247",
    api_secret="XLtCOYXxRTnjZqwaF2oFnQ0AK7k"
)

app.permanent_session_lifetime = timedelta(days=15)

@app.route("/")
def Home():
    if session.get("email"):
        role = session.get("role")
        return redirect(f"/dash/{role}")
    return render_template("index.html")



@app.route("/hmi-manage/employee" , methods=["GET" , "POST"])
def hmi():
    if (request.method == "POST"):
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        role = request.form.get("role")
        pic = request.files.get("pic")
        
        try:
            if(EMPLOYEE_REGISTER.find_one({"Employee_email":email})):
                return "Email with This Employee already Exits"
            
            img = cloudinary.uploader.upload(pic , resource_type="auto")
            url = img["secure_url"]
            
            data = {
                "Employee_name":name,
                "Employee_email":email,
                "Employee_phone_no":phone,
                "Employee_Role":role,
                "Employee_Pic":url
            }
            
            EMPLOYEE_REGISTER.insert_one(data)
            return redirect("/hmi-manage/employee")
        
        except Exception as e:
            print(e)
            return f"Error on Creating the Emplyee due to Server Heavy Load or Network Error , You can Also Try After Some Times.....! , {e}"
    
    Employee = EMPLOYEE_REGISTER.find({})
    
    return render_template("hmi.html" , E=Employee)


@app.route("/hmi-manage/home")
def hmi_home():
    Cleints = CLINET_DATILS.find({})
    return render_template("hmi-home.html" , c=Cleints)

@app.route("/del/employee/<id>"  , methods=['POST'])
def Delete_user(id):
    EMPLOYEE_REGISTER.find_one_and_delete({"_id":ObjectId(id)})
    return redirect('/hmi-manage/home')


@app.route("/login" , methods=["GET" , "POST"])
def login():
    if session.get("email"):
        role = session.get("role")
        return redirect(f"/dash/{role}")
    if(request.method == "POST"):
        phone_no = request.form.get('phone')
        try:
            User = EMPLOYEE_REGISTER.find_one({"Employee_phone_no":phone_no})
            if User:
                session["email"] = User["Employee_email"]
                session["role"] = User["Employee_Role"]
                session.permanent = True
                if session.get("role") == "ClinetEmployee":
                    return redirect(url_for('dash' , role="ClinetEmployee"))
                else:
                    return redirect(url_for('dash' , role="Developer"))
                
            else:
                return "User Not Found"
        except Exception as e:
            print(e)
            return "Server Error"
    
    return render_template("login.html")
            

@app.route("/dash/<role>")
def dash(role):
    email = session.get("email")
    if not session.get("email"):
        return redirect("/login")
    
    if role == "ClinetEmployee":
        if(session.get("Verifed")):
            
         User = EMPLOYEE_REGISTER.find_one({"Employee_email":email})
       
         return render_template("ce.html" , email= email , U=User)
     
        else:
            
            otp_code = str(random.randint(43270 , 93270))
            now = datetime.datetime.now()
            session["opt_time"] = now.strftime('%Y-%m-%d %H:%M:%S')
            session['otp'] = otp_code
            
            N = EMPLOYEE_REGISTER.find_one({"Employee_email":email})
            
            Name = N["Employee_name"]
            
            msg = Message(
            subject=f"Your OTP CODE - HMI , {Name} ",
            recipients=[email],
            sender="sriram65raja@gmail.com",
            body=f"Here is Your OTP code : {otp_code} Don't Share this To anyone \n \n Developed By SRIRAM")
            
            mail.send(msg)
            
            return redirect(url_for("verify")) 
            
    elif role == "Developer":
        if (session.get("Verifed")):
              D = DEVELOPER_LIST.find({}).sort("_id" , -1)
              return render_template("dev.html" , email = email , d=D  )
          
        otp_code = str(random.randint(43270 , 93270))
        now = datetime.datetime.now()
        session["opt_time"] = now.strftime('%Y-%m-%d %H:%M:%S')
        session['otp'] = otp_code
                
        N = EMPLOYEE_REGISTER.find_one({"Employee_email":email})
                
        Name = N["Employee_name"]
                
        msg = Message(
        subject=f"Your OTP CODE - HMI , {Name} ",
        recipients=[email],
        sender="sriram65raja@gmail.com",
        body=f"Here is Your OTP code : {otp_code} Don't Share this To anyone \n \n Developed By SRIRAM")
                
        mail.send(msg)
                
        return redirect(url_for("verify")) 
        
      
    else:
        return "404 Page Not Found"
   


@app.route("/auth/verify" , methods=["GET" , "POST"])
def verify():
    if(request.method == "POST"):
            otp_user = request.form.get("otp_user")
            otp = session.get("otp")
            otp_time_str = session.get("opt_time")
            
            now = datetime.datetime.now()
            
            otp_time = datetime.datetime.strptime(otp_time_str, '%Y-%m-%d %H:%M:%S')
            
            if(now>otp_time+timedelta(minutes=2)):
                return render_template("Verify.html" , err="Otp is Experid")
            else:
                if(otp == otp_user):
                    session["Verifed"] = "verifyed"
                    return redirect("/login")
                else:
                    return render_template("Verify.html" , err="Invalid Otp")
                
    email = session.get("email")  
    return render_template("Verify.html"  , email=email)
    
    


@app.route("/get-clint-deatils" , methods=["POST"])
def GetClinet():
    cname = request.form.get("cname")
    cemail = request.form.get("cemail")
    cphone = request.form.get("cphone")
    csell = request.form.get("csell")
    
    email = session.get("email")
    
    User = EMPLOYEE_REGISTER.find_one({"Employee_email":email})
    
    if User:
        name_emp = User["Employee_name"]
    
    try:
        data={
            "cname":cname,
            "cemail":cemail,
            "cphone":cphone,
            "csell":csell,
            "Emplyee_name":name_emp,
            "Accepted":False,
            "for_Devloper_email":"",
            "sended_developer":False,
            "Developer_accepted":False,
            "Re_Request":False
        }    
        
        c = CLINET_DATILS.insert_one(data)
    
        session["Sumbited_id"] = str(c.inserted_id)
        return redirect("/qr-code")
    except:
        return "Server Error"


@app.route("/send-developer/<c_id>" , methods=["POST"])
def send_client(c_id):
    Client_deatils = ACCEPTED_LIST.find_one({"_id":ObjectId(c_id)})
    DEVELOPER_LIST.insert_one(Client_deatils)
    ACCEPTED_LIST.find_one_and_update({"_id":ObjectId(c_id)} , {"$set":{
        "sended_developer":True
    }})
    
    return redirect("/show-accpted")


@app.route("/show-admin-meassages")
def showAdmin():
    email = session.get("email")
    m = MEASSAGES.find({"Developer_mail":email})
    return render_template("admin-msg.html" , m=m , email=email)

@app.route("/send-msg-dev" , methods=["POST"])
def send_msg_dev():
    msg = request.form.get("msg")
    email_dev = request.form.get("email_dev")
    
    data={
        "From Admin":"Thirulingeshwar",
        "msg":msg,
        "Developer_mail":email_dev
    }
    
    MEASSAGES.insert_one(data)
    
    return jsonify({"Suecess":"Meassage Added"})
    
    

@app.route("/developer-accept/<d_id>", methods=["POST"])
def Devloper_accept(d_id):
    email = session.get("email")
    ACCEPTED_LIST.update_one({"_id": ObjectId(d_id)}, {"$set": {"Developer_accepted": True , "for_Devloper_email":email}})
    DEVELOPER_LIST.update_one({"_id": ObjectId(d_id)}, {"$set": {"Developer_accepted": True , "for_Devloper_email":email}})
    return redirect("/dash/Developer")

  
@app.route("/developer/reject/<d_id>" , methods=["POST"])
def Developer_reject(d_id):
     ACCEPTED_LIST.find_one_and_update({"_id":ObjectId(d_id)} , {"$set" : {
          "Developer_accepted":"Rejected"
      }})
     DEVELOPER_LIST.find_one_and_update({"_id":ObjectId(d_id)} , {"$set" : {
          "Developer_accepted":"Rejected"
      }})
     
     return redirect("/dash/Developer")
 

@app.route("/developer/re-request/<re_id>" , methods=["POST"]) 
def Re_Req(re_id):
    ACCEPTED_LIST.find_one_and_update({"_id":ObjectId(re_id)} , {"$set":{
        "Re_Request":True
    }})
    
    DEVELOPER_LIST.find_one_and_update({"_id":ObjectId(re_id)} , {"$set":{
        "Re_Request":True
    }})
    return redirect("/show-accpted")



@app.route("/get-dev-info/<email>")
def Get_info(email):
    return render_template("info.html" , email=email)


@app.route("/dev/re-req/accept/<d_id>" , methods=["POST"])
def dev_re_req(d_id):
    RE_REQUESTED.find_one_and_update({"_id":ObjectId(d_id)} , {"$set" : {
        "Re_Request":True
    }})
    
    ACCEPTED_LIST.find_one_and_update({"_id":ObjectId(d_id)} , {"$set" : {
        "Re_Request":True
    }})
    return redirect("/dash/Developer")


@app.route("/qr-code")
def qr_code():
    return render_template("qr.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@app.route("/show-accpted")
def show_accpted():
    show_acc = ACCEPTED_LIST.find({}).sort("_id" , -1)
    return render_template("show-ac.html" , s=show_acc)
   
@app.route("/accept/<id>" , methods=["POST"])
def Accept(id):
    CLINET_DATILS.find_one_and_update({"_id":ObjectId(id)} , {"$set" :{
        "Accepted":True
    }})
    
    Clint = CLINET_DATILS.find_one({"_id":ObjectId(id)})
    ACCEPTED_LIST.insert_one(Clint)
    
    CLINET_DATILS.delete_one({"_id":ObjectId(id)})
    
    return redirect("/hmi-manage/home")

@app.route("/reject/<id>" , methods=["POST"])
def Reject(id):
     CLINET_DATILS.find_one_and_update({"_id":ObjectId(id)} , {"$set" :{
        "Accepted":"Rejected"
    }})
     
     Clint = CLINET_DATILS.find_one({"_id":ObjectId(id)})
     ACCEPTED_LIST.insert_one(Clint)
     
     CLINET_DATILS.delete_one({"_id":ObjectId(id)})
     
     return redirect("/hmi-manage/home")
    


@app.route("/del/<id>")
def delete(id):
    ACCEPTED_LIST.find_one_and_delete({"_id":ObjectId(id)})
    return redirect("/show-accpted")

@app.route("/dev/delete/<id>")
def delete_dev(id):
    DEVELOPER_LIST.find_one_and_delete({"_id":ObjectId(id)})
    return redirect("/dash/Developer")

@app.route("/get-accepted-data")
def Get_Accepted():
    sumb_id = session.get("Sumbited_id")
    
    c = ACCEPTED_LIST.find_one({"_id": ObjectId(sumb_id)})
    
    if c:
        c["_id"] = str(c["_id"])
        return jsonify(c)
    else:
        return jsonify({"error": "No data found"}), 404



@app.route('/delete-all', methods=['GET'])
def delete_all_records():
    result = DEVELOPER_LIST.delete_many({})
    return jsonify({
        "message": "All records deleted",
        "deleted_count": result.deleted_count
    })
    
if __name__ == "__main__":
    app.run(debug=True , port=1212)
