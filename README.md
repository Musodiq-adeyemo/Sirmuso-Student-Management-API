# ALTSCHOOL-BACKEND-Python-THIRD-SEMESTER-EXAMINATION-PROJECT.
## CONTENT
### Title
### Introduction 
### Project Environment
### Installation
### Authentication & Authorization
### Rules
### Usage
### What i learned
### Testing
### Challenges
### Acknowledgement
### Conclusion

# TITLE:
# SIRMUSO STUDENTS MANAGEMENT API

# INTRODUCTION :
Sirmuso Student Management API is built using Flask-RESTX and Flask-sqlalchemy.
This is a student management API that allows users to register their account with their preferred password and must specify the user status(Student, Teacher or Admin).
This student management API contains more than 50 routes which has been tested and all working fine.
Some routes are authorized for Admin only, some for Teachers only, some for Students only, some for Teacher and Admin only while others are for all registered users.


# BUILT WITH:
<p align="left"> <a href="https://www.python.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a>
<a href="https://flask.palletsprojects.com/" target="_blank" rel="noreferrer"> <br> <img src="https://www.vectorlogo.zone/logos/pocoo_flask/pocoo_flask-icon.svg"  alt="flask" width="40" height="40"/></a> </p>

# PROJECT ENVIRONMENT: 
This project requires a virtual environment for the proper functioning of the project. This section gives a short demonstration of how to create a virtual environment(windows users) which is as follows:
## Step 1:
Open your system command prompt from your window search bar "search command prompt".

## Step 2 :
Make a directory to your desktop or any preferable location.
### Command: cd Desktop
## Step 3:
Install virtual environment if not installed before.
### Command: pip install virtual environment
## Step 4:
Create your flask environment with any name you want. (i will be using flaskenv for demonstration)
### Command: virtualenv flaskenv
## Step 5:
Make a directory to your environment
### Command: cd flaskenv
## Step 6:
Make a directory to scripts
### Command: cd scripts
## Step 7:
Activate your environment
### Command: activate
Yes, your environment is ready for use.
### Note: The above illustrations are for windows users only.

# INSTALLATION:
This section contains all the packages to be installed for this project.
Before installation make sure your environment is activated and packages are installed in the terminal( e.g command prompt, PowerShell, Git Bash, etc) using  "pip install package".
## Packages to be installed:
### flask
### flask-login
### flask-sqlalchemy
### flask-migrate
### flask-jwt-extended
### flask-restx
### python-decouple
### python-dotenv

### The command for installation:
pip install " package name"

# AUTHENTICATION AND AUTHORIZATION
This student management API is fully authenticated using JWT tokens. The user will need an access token before they are allowed to get access to others routes. The users must first register their accounts and after registration, they are meant to log in to their accounts where an access token will be generated for every user. The access token is the gateway for every user to access other routes.
Sirmuso Student Management API is well-secured so that unauthorized users cannot access the unauthorized routes so it is advised that every users should follow the rules and guidelines stated below.
Users are allowed to log out when done.

 
# RULES
### All users must register their accounts with their preferred password.
### All users must set up their profiles in other to be registered with adequate information.
### Only Admin can register students and teachers and generate students' matriculation numbers and staff identification numbers.
### Students must retrieve their matric number before they can register for their courses.
### Staff must retrieve the staff identification number before they can register for their course.
### Only Teacher and Admin are allowed to input students score to the dashboard.
### Only Admin can generate the students GPA.

# USAGE
## Admin
### Step 1 :
Create an account with your email , username , password and specify your role(i.e designation= ADMIN).
### Step 2:
Login to your account using your email and password. An access token will be generated which you will use as your authorization key.
### Step 3:
Confirm users with designation as Students if they are bonafide students of the school and retrieve their profile to get their required data.
### Step 4:
Register Students using the information from their profiles. Also, you have the authority to update, delete and retrieve students' information.
### Step 5:
Generate a Matriculation Number for the registered students so that they can register for courses.
### Step 6:
Confirm users with designation as Teacher if they are real staff of the school and retrieve their profile to get their required data.
### Step 7:
Register Teachers using the information from their profiles. Also, you have the authority to update, delete and retrieve teachers' information.
### Step 8:
Generate staff identification number for all registered staff.
### Step 9:
Submit the student's score for grading and their scores can be retrieved, updated, and deleted in the database.



## Admin Authorized routes
### All routes in the Auth namespace.
### All routes in the Profile namespace.
### All routes in the Grade namespace.
### All routes except Get matric_no routes in the Student namespace.
### All routes except Get staff Id routes in the Teacher namespace.
### Get all courses route
### Get courses by course id route.
### Get all teacher courses route.
### Get teacher courses by course id route.
### All other routes are unauthorized for the admin.

## Teacher
### Step 1 :
Create an account with your email , username , password and specify your role(i.e designation= ADMIN).
### Step 2:
Login to your account using your email and password. An access token will be generated which you will use as your authorization key.
###  Step 3:
Get your staff identification number from the Get staff id route in the Teacher namespace.
### Step 4:
Register for the course you are to teach for the semester and you can also update, delete and retrieve the course.
### Step 5:
Submit the student's score for your course for grading you can as well retrieve, update and delete student scores.

## Teacher authorized routes
### All routes in the Auth namespace.
### All routes in the profile namespace.
### All routes in the TeacherCourse namespace.
### All routes in the Grade namespace.
### Get staff id route.
## Student
### Step 1 :
Create an account with your email , username , password and specify your role(i.e designation= ADMIN).
### Step 2:
Login to your account using your email and password. An access token will be generated which you will use as your authorization key.
### Step 3:
Get your matriculation number from the Get matrix_no  route in the Student namespace.
### Step 4:
Register for the courses you are to take for the semester and you can also update, delete and retrieve the courses.

## Student authorized routes
### All routes in the Auth namespace.
### All routes in the profile namespace.
### All routes in the StudentCourse namespace.
### All routes in the Grade namespace except the Submit result route.
### Get matric_no route.

# LESSON LEARNED 
### Unit testing using pytest and test environment variables.
### Using insomnia and postman for testing my route.
### Use of flask shell to create my database.
### Deployment using Pythonanywhere.
### Configuration of development, test and production.

#  TESTING
To test Sirmuso Student Management API you must follow the above rules and guidelines while working through the below site.
Click the deploy link musawdeeq.pythonanywhere.com 


# THE Challenges’
Getting  student by matriculation number which is a string. 

Getting  Teacher by identification number which is a string. 

Creating multiple course for same set of student.

Resetting lost password

Using uuid for my database



# ACKNOWLEDGEMENT
### Caleb Emenike
### Altschool Africa School of Software Engineering.


# CONCLUSION
This student management API " SIRMUSO STUDENT MANAGEMENT API" is an AltSchool python backend third-semester examination project which was built to suit the exam instructions.
This project is fully created by ADEYEMO MUSODIQ OLALEKAN an AltSchool Africa School of Engineering student.
This project is open for contribution.

<h1 align="left" font-weight="bold">Connect with me:</h1>
<p align="left">
<a href="https://twitter.com/sirmuso" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/twitter.svg" alt="sirmuso" height="30" width="40" /></a>
<a href="https://linkedin.com/in/musodiq-adeyemo" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/linked-in-alt.svg" alt="musodiq-adeyemo" height="30" width="40" /></a>
<a href="https://fb.com/https://www.facebook.com/adeyemo.musodiq" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/facebook.svg" alt="https://www.facebook.com/adeyemo.musodiq" height="30" width="40" /></a>
</p>

- 📫 How to reach me **adeyemomusodiq@gmail.com**

- ⚡ Fun fact **I'm currently studying at AltSchool Africa School of Software Engineering Class of 2022.**


You can contact me on WhatsApp at 08141171294

## GOD BLESS ALT SCHOOL  AFRICA






