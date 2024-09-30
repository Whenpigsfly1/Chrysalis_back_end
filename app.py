import flask
from flask import Flask, render_template, request, session, redirect,url_for
from flask_mysqldb import MySQL
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


app.config['MYSQL_HOST'] = 'FILL-IN'
app.config['MYSQL_USER'] = 'FILL-IN'
app.config['MYSQL_PASSWORD'] = 'FILL-IN'
app.config['MYSQL_DB'] = 'FILL-IN'
 
mysql = MySQL(app)

 
@app.route('/')
def home():
	return render_template('home.html')
	#returns the homepage of the website

@app.route('/t_create', methods=['GET', 'POST'])
def t_create():
	if request.method == "POST":
		details = request.form
		school = details['school']
		username = details['username']
		print(school)
		print(username)
		password = details['password']
		cur = mysql.connection.cursor()
		cur.execute("SELECT t_username FROM schools WHERE school_name = %s AND t_username = %s", (school,username))
		Users = cur.fetchall()
		print(Users)
		if Users:
			print('duplicate username')
			return('Username already in use. Please choose a different username')
		cur.execute("INSERT INTO schools(school_name, t_username, t_password) VALUES (%s, %s, %s)", (school, username, password))
		mysql.connection.commit()
		cur.close()
		session["teacher_school"] = school
		return redirect("t_login")
	cur = mysql.connection.cursor()
	cur.execute("SELECT DISTINCT school_name FROM schools")
	schools = cur.fetchall()
	school_names =[]
	for school in schools:
		school_name = school[0]
		school_names.append(school_name)
	print('school_names')
	print(school_names)
	return render_template('t_create.html', schools=school_names)

@app.route('/t_select_school', methods=['GET', 'POST'])
def t_select_school():
	if request.method == "POST":
		details = request.form
		school = details['select_school']
		print('select school details')
		print(details)
		cur = mysql.connection.cursor()
		session["teacher_school"] = school
		print(session["teacher_school"])
		return redirect("/t_login")
	cur = mysql.connection.cursor()
	cur.execute("SELECT DISTINCT school_name FROM schools")
	schools = cur.fetchall()
	print('school_names')
	print(schools)
	return render_template('t_find_school.html', schools = schools)

@app.route('/t_login', methods=['GET', 'POST'])
def t_login():
	school = session["teacher_school"]
	if request.method == "POST":
		details = request.form
		username = details['username']
		password = details['password']
		school = session["teacher_school"]
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM schools WHERE school_name = %s AND t_username = %s AND t_password = %s", (school,username,password))
		User=cur.fetchone()
		cur.close()
		print(User)
		if User:
			session["teacher_name"] = request.form.get("username")
			return t_login_success()
		else:
			return render_template('t_loginfail.html', school = school)
	return render_template('t_login.html', school = school)

@app.route('/t_login_success', methods=['GET', 'POST'])
def t_login_success():
	teacher_username = session["teacher_name"]
	if teacher_username:
		return redirect("/t_home")
	else:
		return redirect("/")
@app.route('/t_home', methods=['GET', 'POST'])
def t_home():
	school = session["teacher_school"]
	teacher_username = session["teacher_name"]
	if request.method == "POST":
		details = request.form
		selected_student = details['student']
		#assigned = details['assigned_to_all']
		print(selected_student)
		if selected_student:
			session["selected_student"] = request.form.get("student")
			return redirect('/t_student_layout')
		#if assigned:
			#print(assigned)
			#cur = mysql.connection.cursor()
			#cur.execute("SELECT Student_username FROM teachers2 WHERE School_name =%s AND Teacher_username =%s", (school, teacher_username))
			#students = cur.fetchall()
			#print(students)
			#for student in students:
				#cur.execute("INSERT INTO videos2 (Student_school, Teacher_name, Student_username, Video_Name, Completed) VALUES (%s,%s,%s,%s,%s)", (school, teacher_username, student,assigned,0))
				#mysql.connection.commit()															
			#cur.close()
	cur = mysql.connection.cursor()
	cur.execute("SELECT Video_Number,Video_filename,Video_tag FROM video_filenames_test8")
	videos = cur.fetchall()
	cur.execute("SELECT Student_username FROM teachers2 WHERE School_name =%s AND Teacher_username =%s", (school, teacher_username))
	Students = cur.fetchall()
	mysql.connection.commit()															
	cur.close()
	return render_template('t_home.html', Students = Students, teacher_username = teacher_username,videos=videos)

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
	if request.method == "POST":
		details = request.form
		school = session["teacher_school"]
		teacher_username = session["teacher_name"]
		added_student_username = details['s_username']
		cur = mysql.connection.cursor()
		cur.execute("SELECT Student_username FROM teachers2 WHERE School_name =%s AND Teacher_username =%s", (school, teacher_username))
		Students = cur.fetchall()
		for student in Students:
			if student[0] == added_student_username:
				return('Cannot add duplicate usernames!')
		cur.execute("INSERT INTO teachers2(School_name, Teacher_username, Student_username) VALUES (%s, %s, %s)", (school, teacher_username, added_student_username))
		mysql.connection.commit()
		cur.close()
		return redirect("/t_login_success")
		#print(added_student_username)
		#cur = mysql.connection.cursor()
		#cur.execute("SELECT username FROM stest")
		#students = cur.fetchall()
		#print(students)
		#for student in students:
			#if added_student_username == student[0]:
				#cur.execute("SELECT Student_username FROM teachers")
				#Current_usernames = cur.fetchall()
				#print(Current_usernames)
				#for username in Current_usernames:
					#print(username)
					#if added_student_username == username[0]:
						#print('in list')
						#return 'Student already in list'
				#cur.execute("INSERT INTO teachers (Teacher_username, Student_username) VALUES (%s,%s)", (teacher_username,added_student_username,))
				#mysql.connection.commit()															
				#cur.close()
				#return redirect("/t_login_success")
		#return 'error - student not found'
	return render_template('add_student.html')

@app.route('/delete_student', methods=['GET', 'POST'])
def delete_student():
	school = session["teacher_school"]
	teacher_username = session["teacher_name"]
	cur = mysql.connection.cursor()
	cur.execute("SELECT Student_username FROM teachers2 WHERE School_name =%s AND Teacher_username =%s", (school, teacher_username))
	Students = cur.fetchall()
	if request.method == "POST":
		details = request.form
		school = session["teacher_school"]
		teacher_username = session["teacher_name"]
		deleted_student_username = details['student']
		cur = mysql.connection.cursor()
		cur.execute("SELECT Student_username FROM teachers2 WHERE School_name =%s AND Teacher_username =%s", (school, teacher_username))
		Students = cur.fetchall()
		for student in Students:
			if student[0] == deleted_student_username:
				cur.execute("DELETE FROM teachers2 WHERE Student_username=%s", (deleted_student_username,))
		mysql.connection.commit()
		cur.close()
		return redirect("/t_login_success")
	return render_template('delete_student.html', Students=Students)

@app.route('/assign_to_all', methods=['GET', 'POST'])
def assign_to_all():
	cur = mysql.connection.cursor()
	cur.execute("SELECT Video_Number,Video_filename,Video_tag FROM video_filenames_test8")
	videos = cur.fetchall()
	if request.method == "POST":
		print('posted')
		details = request.form
		assigned = details['assigned_to_all']
		print(assigned)
		school = session["teacher_school"]
		teacher = session["teacher_name"]
		cur = mysql.connection.cursor()
		cur.execute("SELECT Student_username FROM teachers2 WHERE School_name =%s AND Teacher_username =%s", (school, teacher))
		students = cur.fetchall()
		print(students)
		for student in students:
			cur.execute("INSERT INTO videos2 (Student_school, Teacher_name, Student_username, Video_Name, Completed) VALUES (%s,%s,%s,%s,%s)", (school, teacher, student,assigned,0))
			mysql.connection.commit()															
		cur.close()
		return redirect('/t_home')
	return render_template('assign_to_all.html', videos=videos)


@app.route("/t_student_layout")
def t_student_layout():
	school = session["teacher_school"]
	teacher = session["teacher_name"]
	student = session["selected_student"]
	print('student layout')
	print(school)
	print(teacher)
	print(student)
	cur = mysql.connection.cursor()
	cur.execute("SELECT Video_Name,Q1_answer,Q2_Answer,Q3_Answer,Notes FROM videos2 WHERE Student_school = %s AND Teacher_Name = %s AND Student_username = %s AND completed = 0", (school, teacher, student))
	unfinished_videos =cur.fetchall()
	print(unfinished_videos)
	cur.execute("SELECT Video_Name,Q1_answer,Q2_Answer,Q3_Answer,Notes,Timestamp FROM attempts WHERE Student_school = %s AND Teacher_Name = %s AND Student_username = %s", (school,teacher,student))
	finished_videos =cur.fetchall()
	print(finished_videos)
	return render_template('t_student_layout.html', student = student, unfinished_videos=unfinished_videos,finished_videos=finished_videos)

@app.route('/assign_video', methods=['GET', 'POST'])
def assign_video():
	cur = mysql.connection.cursor()
	cur.execute("SELECT Video_Number,Video_filename,Video_tag FROM video_filenames_test8")
	videos = cur.fetchall()
	if request.method == "POST":
		school = session["teacher_school"]
		teacher = session["teacher_name"]
		details = request.form
		student_username = session["selected_student"]
		assigned_video = details['assigned_video']
		print(assigned_video)
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO videos2 (Student_school, Teacher_name, Student_username, Video_Name, Completed) VALUES (%s,%s,%s,%s,%s)", (school, teacher, student_username,assigned_video,0))
		mysql.connection.commit()															
		cur.close()
		return redirect("/t_student_layout")
		#cur = mysql.connection.cursor()
		#cur.execute("SELECT Student_username FROM stest")
		#students = cur.fetchall()
		#print(students)
		#for student in students:
			#if student_username == student[0]:
				#cur.execute("INSERT INTO videos (Student_username, Video_NAME, Completed) VALUES (%s,%s,%s)", (student_username,assigned_video,0))
				#mysql.connection.commit()															
				#cur.close()
				#return redirect("/t_student_layout")
		#return 'error - student not found'
	return render_template('assign_video.html',videos = videos)

@app.route("/exit_student")
def exit_student():
	session["selected_student"] = None
	return redirect("/t_home")

@app.route('/s_find_school_create', methods=['GET', 'POST'])
def s_find_school_create():
	if request.method == "POST":
		details = request.form
		school = details['select_school']
		cur = mysql.connection.cursor()
		session["student_school"] = school
		return redirect("/s_create")
	cur = mysql.connection.cursor()
	cur.execute("SELECT DISTINCT school_name FROM schools")
	schools = cur.fetchall()
	return render_template('s_find_school_create.html', schools = schools)

@app.route('/s_create', methods=['GET', 'POST'])
def s_create():
	school = session["student_school"]
	cur = mysql.connection.cursor()
	cur.execute("SELECT t_username FROM schools WHERE school_name = %s",(school,))
	teachers = cur.fetchall()
	if request.method == "POST":
		details = request.form
		teacher_name = details['teacher']
		username = details['username']
		password = details['password']
		cur = mysql.connection.cursor()
		cur.execute("SELECT student_username FROM newstest WHERE school_name= %s AND teacher_name = %s", (school,teacher_name))
		accounts = cur.fetchall()
		print(accounts)
		for account in accounts:
			if account[0] == username:
				return('Username already exists')
		#check that student-inputted username matches an account
		cur.execute("SELECT Student_username FROM teachers2 WHERE Teacher_username =%s",(teacher_name,))
		students = cur.fetchall()
		print(students)
		for student in students:
			if student[0] == username:
				cur.execute("INSERT INTO newstest(school_name,teacher_name,student_username,password) VALUES (%s,%s,%s,%s)", (school, teacher_name, username, password))
				mysql.connection.commit() 
				cur.close()
				return redirect('/s_login')	
		return render_template('s_createfail.html', school = school)
	return render_template('s_create.html', school = school, teachers = teachers)

#Is the next one needed?
@app.route('/s_createfail')
def s_createfail():
	school = session["student_school"]
	return render_template('s_createfail.html', school = school)

@app.route('/s_find_school_login', methods=['GET', 'POST'])
def s_find_school_login():
	if request.method == "POST":
		details = request.form
		school = details['select_school']
		cur = mysql.connection.cursor()
		session["student_school"] = school
		return redirect("/s_login")
	cur = mysql.connection.cursor()
	cur.execute("SELECT DISTINCT school_name FROM schools")
	schools = cur.fetchall()
	return render_template('s_find_school_login.html', schools = schools)

@app.route('/s_login', methods=['GET', 'POST'])
def s_login():
	school = session["student_school"]
	cur = mysql.connection.cursor()
	cur.execute("SELECT t_username FROM schools WHERE school_name = %s",(school,))
	teachers = cur.fetchall()
	print(teachers)
	if request.method == "POST":
		details = request.form
		username = details['username']
		teacher = details['teacher']
		password = details['password']
		print(school)
		print(teacher)
		print(username)
		print(password)
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM newstest WHERE school_name = %s AND teacher_name=%s AND student_username = %s AND password = %s", (school,teacher,username,password))
		User=cur.fetchone()
		cur.close()
		print(User)
		if User:
			session["student_name"] = username
			session["s_teacher"] = teacher
			return s_login_success(username)
		else:
			return render_template('s_loginfail.html', school = school, teachers = teachers)
	return render_template('s_login.html', school = school, teachers=teachers)

@app.route('/s_login_success', methods=['GET', 'POST'])
def s_login_success(username):
	print(username)
	return redirect("/s_home")

@app.route('/s_home', methods=['GET', 'POST'])
def s_home():
	if request.method == "POST":
		details = request.form
		print('details:')
		print(details)
		video_number = details['selected_video']
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM video_filenames_test8 WHERE Video_Number = %s",(video_number))
		video_details = cur.fetchone()
		url=video_details[3]
		print(video_details)
		session["selected_video"] = video_number
		session["video_url"] = url
		return redirect ("/show_video")
	student = session["student_name"]
	teacher = session["s_teacher"] 
	school = session["student_school"]
	cur = mysql.connection.cursor()
	cur.execute("SELECT * FROM videos2")
	everything = cur.fetchall()
	print(everything)
	print(school)
	print(student)
	cur.execute("SELECT Video_Name FROM videos2 WHERE Student_school =%s AND Teacher_Name = %s AND Student_username = %s AND completed = 0", (school,teacher,student))
	unfinished_videos =cur.fetchall()
	print('unfinished_videos')
	print(unfinished_videos)
	if len(unfinished_videos) == 0:
		empty = True
		print(empty)
		return render_template('s_finished_home.html')
	cur.execute("SELECT v.Student_username, v.Video_Name, vf.Video_filename FROM videos2 v JOIN video_filenames_test8 vf on v.Video_Name = vf.Video_Number WHERE Student_school =%s AND Teacher_Name = %s AND Student_username = %s AND completed = 0",(school,teacher,student))
	unfinished_video_filenames =cur.fetchall()
	print('unfinished video filenames')
	print(unfinished_video_filenames)
	#unfinished_video_urls =[]
	#for item in unfinished_video_filenames:
		#url = item[2]
		#unfinished_video_urls.append(url)
	#print(unfinished_video_urls)
	#cur.execute("SELECT * FROM videos2 WHERE Student_school =%s AND Teacher_Name =%s AND Student_username = %s AND completed = 1", (school, teacher, student))
	#finished_videos =cur.fetchall()
	return render_template('s_home.html', student = student, unfinished_videos=unfinished_videos,unfinished_video_filenames=unfinished_video_filenames)

@app.route('/show_video',methods=['GET', 'POST'])
def show_video():
	student = session["student_name"]
	teacher = session["s_teacher"] 
	school = session["student_school"]
	video_number = session["selected_video"]
	print('current video:')
	print(video_number)
	url = session["video_url"]
	if request.method == "POST":
		details = request.form
		print(details)
		q1 = details['q1']
		q2 = details['q2']
		q3 = details['q3']
		notes = details['notes']
		video = details['video']
		cur = mysql.connection.cursor()
		#cur.execute("UPDATE videos2 SET Completed = 1, Q1_Answer = %s, Q2_Answer = %s, Q3_Answer = %s, Notes = %s WHERE Student_school =%s AND Teacher_Name = %s AND Student_Username = %s AND Video_name = %s", (q1,q2,q3,notes,school,teacher,student,video))
		cur.execute("UPDATE videos2 SET Completed = 1 WHERE Student_school =%s AND Teacher_Name = %s AND Student_Username = %s AND Video_name = %s", (school,teacher,student,video))
		cur.execute("INSERT INTO attempts (Student_school, Teacher_name, Student_username, Video_Name,Q1_Answer,Q2_Answer,Q3_Answer,Notes) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)", (school,teacher,student,video,q1,q2,q3,notes))
		print('succesfully committed')
		mysql.connection.commit() 
		cur.close()
		session["selected_video"] = None
		session["video_url"] = None
		return redirect("/s_home")
	cur = mysql.connection.cursor()
	cur.execute("SELECT q1,o1a,o1b,o1c,o1d,q2,o2a,o2b,o2c,o2d,q3,o3a,o3b,o3c,o3d FROM video_filenames_test8 WHERE Video_Number= %s",(video_number,))
	questions = cur.fetchone()
	print(questions)
	cur.close()
	return render_template('video.html', video_number=video_number,url=url, questions = questions)

@app.route('/video1',methods=['GET', 'POST'])
def video1():
	student = session["student_name"]
	teacher = session["s_teacher"] 
	school = session["student_school"]
	if request.method == "POST":
		details = request.form
		q1 = details['q1']
		q2 = details['q2']
		q3 = details['q3']
		notes = details['notes']
		video = details['video']
		cur = mysql.connection.cursor()
		cur.execute("UPDATE videos2 SET Completed = 1, Q1_Answer = %s, Q2_Answer = %s, Q3_Answer = %s, Notes = %s WHERE Student_school =%s AND Teacher_Name = %s AND Student_Username = %s AND Video_name = %s", (q1,q2,q3,notes,school,teacher,student,video))
		mysql.connection.commit() 
		cur.close()
		return redirect("/s_home")
	return render_template('video1.html')

@app.route('/video2',methods=['GET', 'POST'])
def video2():
	student = session["student_name"]
	teacher = session["s_teacher"] 
	school = session["student_school"]
	if request.method == "POST":
		details = request.form
		q1 = details['q1']
		q2 = details['q2']
		q3 = details['q3']
		notes = details['notes']
		video = details['video']
		cur = mysql.connection.cursor()
		cur.execute("UPDATE videos2 SET Completed = 1, Q1_Answer = %s, Q2_Answer = %s, Q3_Answer = %s, Notes = %s WHERE Student_school =%s AND Teacher_Name = %s AND Student_Username = %s AND Video_name = %s", (q1,q2,q3,notes,school,teacher,student,video))
		mysql.connection.commit() 
		cur.close()
		return redirect("/s_home")
	return render_template('video2.html')

@app.route('/video3',methods=['GET', 'POST'])
def video3():
	student = session["student_name"]
	teacher = session["s_teacher"] 
	school = session["student_school"]
	if request.method == "POST":
		details = request.form
		q1 = details['q1']
		q2 = details['q2']
		q3 = details['q3']
		notes = details['notes']
		video = details['video']
		cur = mysql.connection.cursor()
		cur.execute("UPDATE videos2 SET Completed = 1, Q1_Answer = %s, Q2_Answer = %s, Q3_Answer = %s, Notes = %s WHERE Student_school =%s AND Teacher_Name = %s AND Student_Username = %s AND Video_name = %s", (q1,q2,q3,notes,school,teacher,student,video))
		mysql.connection.commit() 
		cur.close()
		return redirect("/s_home")
	return render_template('video3.html')

@app.route('/video4',methods=['GET', 'POST'])
def video4():
	student = session["student_name"]
	teacher = session["s_teacher"] 
	school = session["student_school"]
	if request.method == "POST":
		details = request.form
		q1 = details['q1']
		q2 = details['q2']
		q3 = details['q3']
		notes = details['notes']
		video = details['video']
		cur = mysql.connection.cursor()
		cur.execute("UPDATE videos2 SET Completed = 1, Q1_Answer = %s, Q2_Answer = %s, Q3_Answer = %s, Notes = %s WHERE Student_school =%s AND Teacher_Name = %s AND Student_Username = %s AND Video_name = %s", (q1,q2,q3,notes,school,teacher,student,video))
		mysql.connection.commit() 
		cur.close()
		return redirect("/s_home")
	return render_template('video4.html')

@app.route('/s_videos', methods=['GET', 'POST'])
def s_videos():
	student = session["student_name"]
	teacher = session["s_teacher"] 
	school = session["student_school"]
	if request.method == "POST":
		details = request.form
		print(details)
		q1 = details['q1']
		q2 = details['q2']
		q3 = details['q3']
		notes = details['notes']
		video = details['video']
		print('answers')
		print(q1)
		print(q2)
		print(q3)
		print(notes)
		cur = mysql.connection.cursor()
		print(student)
		print(video)
		cur.execute("UPDATE videos2 SET Completed = 1, Q1_Answer = %s, Q2_Answer = %s, Q3_Answer = %s, Notes = %s WHERE Student_school =%s AND Teacher_Name = %s AND Student_Username = %s AND Video_name = %s", (q1,q2,q3,notes,school, teacher, student,video))
		mysql.connection.commit() 
		cur.close()
		print("cur closed!")
	#student = session["student_name"]
	cur = mysql.connection.cursor()
	#unfinished_videos =cur.fetchall()
	#print('unfinished_videos')
	#print(unfinished_videos)
	cur.execute("SELECT v.Student_username, v.Video_Name, vf.Video_filename FROM videos2 v JOIN video_filenames_test8 vf on v.Video_Name = vf.Video_Number WHERE Student_school =%s AND Teacher_Name = %s AND Student_username = %s AND completed = 0",(school, teacher, student,))
	unfinished_video_filenames =cur.fetchall()
	print('unfinished video filenames')
	print(unfinished_video_filenames)
	#unfinished_video_urls =[]
	#for item in unfinished_video_filenames:
		#url = item[2]
		#unfinished_video_urls.append(url)
	#print(unfinished_video_urls)
	cur.execute("SELECT * FROM videos2 WHERE Student_school =%s AND Teacher_Name = %s AND Student_username = %s AND completed = 1", (school, teacher, student))
	finished_videos =cur.fetchall()
	return render_template('s_videos.html', student = student,finished_videos=finished_videos, unfinished_video_filenames=unfinished_video_filenames)

@app.route("/s_all_videos")
def s_all_videos():
	cur = mysql.connection.cursor()
	cur.execute("SELECT Video_Number,Video_filename FROM video_filenames_test8 WHERE Video_tag='biology'")
	biology = cur.fetchall()
	cur.execute("SELECT Video_Number,Video_filename FROM video_filenames_test8 WHERE Video_tag='earth science'")
	earth_science = cur.fetchall()
	cur.execute("SELECT Video_Number,Video_filename FROM video_filenames_test8 WHERE Video_tag='technology'")
	technology = cur.fetchall()
	cur.execute("SELECT Video_Number,Video_filename FROM video_filenames_test8 WHERE Video_tag='Mathematics'")
	math = cur.fetchall()
	return render_template('s_all_videos.html', biology = biology, technology = technology, earth_science = earth_science, math=math, videos=videos)


@app.route("/t_all_videos",methods=['GET', 'POST'])
def t_all_videos():
	if request.method == "POST":
		print('posted')
		details = request.form
		assigned = details['assigned_to_all']
		print(assigned)
		school = session["teacher_school"]
		teacher = session["teacher_name"]
		cur = mysql.connection.cursor()
		cur.execute("SELECT Student_username FROM teachers2 WHERE School_name =%s AND Teacher_username =%s", (school, teacher))
		students = cur.fetchall()
		print(students)
		for student in students:
			cur.execute("INSERT INTO videos2 (Student_school, Teacher_name, Student_username, Video_Name, Completed) VALUES (%s,%s,%s,%s,%s)", (school, teacher, student,assigned,0))
			mysql.connection.commit()									
		cur.close()
	cur = mysql.connection.cursor()
	cur.execute("SELECT Video_Number,Video_filename,Video_tag FROM video_filenames_test8")
	videos = cur.fetchall()
	cur.execute("SELECT Video_Number,Video_filename FROM video_filenames_test8 WHERE Video_tag='biology'")
	biology = cur.fetchall()
	cur.execute("SELECT Video_Number,Video_filename FROM video_filenames_test8 WHERE Video_tag='earth science'")
	earth_science = cur.fetchall()
	cur.execute("SELECT Video_Number,Video_filename FROM video_filenames_test8 WHERE Video_tag='technology'")
	technology = cur.fetchall()
	cur.execute("SELECT Video_Number,Video_filename FROM video_filenames_test8 WHERE Video_tag='Mathematics'")
	math = cur.fetchall()

	return render_template('t_all_videos.html', biology = biology, technology = technology, earth_science = earth_science, math=math, videos=videos)


@app.route('/insert_video', methods=['GET', 'POST'])
def insert_video():
	if request.method == "POST":
		details = request.form
		url = details['url']
		name = details['name']
		tag = details['tag']
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO video_filenames_test8(Video_Number, Video_filename,Video_tag) VALUES (%s,%s,%s)", (name,url,tag))
		mysql.connection.commit() 
		cur.close()
		return redirect('/insert_video_success')	
	return render_template('insert_video.html')

@app.route('/insert_video_success')
def insert_video_success():	
	return render_template('insert_video_success.html')

@app.route('/insert_video_questions', methods=['GET', 'POST'])
def insert_video_questions():
	cur = mysql.connection.cursor()
	cur.execute("SELECT Video_Number FROM video_filenames_test8")
	videos = cur.fetchall()
	print(videos)
	if request.method == "POST":
		details = request.form
		video_number = details['video_number']
		print(video_number)
		q1=details['q1']
		o1a=details['o1a']
		o1b=details['o1b']
		o1c=details['o1c']
		o1d=details['o1d']
		q2=details['q2']
		o2a=details['o2a']
		o2b=details['o2b']
		o2c=details['o2c']
		o2d=details['o2d']
		q3=details['q3']
		o3a=details['o3a']
		o3b=details['o3b']
		o3c=details['o3c']
		o3d=details['o3d']
		worksheet=details['worksheet']
		print(details)
		cur = mysql.connection.cursor()
		cur.execute("UPDATE video_filenames_test8 SET q1=%s,o1a=%s,o1b=%s,o1c=%s,o1d=%s,q2=%s,o2a=%s,o2b=%s,o2c=%s,o2d=%s,q3=%s,o3a=%s,o3b=%s,o3c=%s,o3d=%s,worksheet_url=%s WHERE Video_Number =%s", (q1,o1a,o1b,o1c,o1d,q2,o2a,o2b,o2c,o2d,q3,o3a,o3b,o3c,o3d,worksheet,video_number))
		mysql.connection.commit() 
		cur.close()
		return redirect('/')	
	return render_template('insert_video_questions.html', videos = videos)

@app.route('/cells_wkst_1', methods=['GET', 'POST'])
def cells_wkst_1():	
	if request.method == "POST":
		print("posted")
		student = session["student_name"]
		teacher = session["teacher_name"]
		school = session["student_school"]
		details = request.form
		answer1=details['nucleus']
		answer2=details['Mitochondria']
		answer3=details['Rough Endoplasmic Reticulum']
		answer4=details['Peroxisomes & Lysosomes']
		answer5=details['Smooth Endoplasmic Reticulum']
		answer6=details['Golgi Apparatus']
		print(details)
		print(answer6)
		cur = mysql.connection.cursor()
		print("open")
		cur.execute("INSERT INTO cells_wkst_1(School_name,Teacher_name,Student_name,answer1,answer2,answer3,answer4,answer5,answer6) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (school,teacher,student,answer1,answer2,answer3,answer4,answer5,answer6))
		mysql.connection.commit()
		cur.close()
		print("cured")
	return render_template('cells_wkst_1.html')

@app.route('/cells_wkst_2', methods=['GET', 'POST'])
def cells_wkst_2():	
	if request.method == "POST":
		print("posted")
		student = session["student_name"]
		details = request.form
		print(details)
	return render_template('cells_wkst_2.html')

@app.route('/cells_wkst_3', methods=['GET', 'POST'])
def cells_wkst_3():	
	if request.method == "POST":
		print("posted")
		student = session["student_name"]
		details = request.form
		print(details)
	return render_template('cells_wkst_3.html')

@app.route('/life_wkst_1', methods=['GET', 'POST'])
def life_wkst_1():	
	if request.method == "POST":
		print("posted")
		student = session["student_name"]
		details = request.form
		print(details)
	return render_template('life_wkst_1.html')

@app.route('/life_wkst_2', methods=['GET', 'POST'])
def life_wkst_2():	
	if request.method == "POST":
		print("posted")
		student = session["student_name"]
		details = request.form
		print(details)
	return render_template('life_wkst_2.html')

@app.route('/life_wkst_3', methods=['GET', 'POST'])
def life_wkst_3():	
	if request.method == "POST":
		print("posted")
		student = session["student_name"]
		details = request.form
		print(details)
	return render_template('life_wkst_3.html')


@app.route('/gastropods_wkst_1', methods=['GET', 'POST'])
def gastropods_wkst_1():	
	if request.method == "POST":
		print("posted")
		student = session["student_name"]
		details = request.form
		print(details)
	return render_template('gastropods_wkst_1.html')

@app.route('/gastropods_wkst_2', methods=['GET', 'POST'])
def gastropods_wkst_2():	
	if request.method == "POST":
		print("posted")
		student = session["student_name"]
		details = request.form
		print(details)
	return render_template('gastropods_wkst_2.html')

@app.route('/gastropods_wkst_3', methods=['GET', 'POST'])
def gastropods_wkst_3():	
	if request.method == "POST":
		print("posted")
		student = session["student_name"]
		details = request.form
		print(details)
	return render_template('gastropods_wkst_3.html')

@app.route('/salamanders_wkst_1', methods=['GET', 'POST'])
def salamanders_wkst_1():	
	if request.method == "POST":
		print("posted")
		student = session["student_name"]
		details = request.form
		print(details)
	return render_template('salamanders_wkst_1.html')

@app.route('/salamanders_wkst_2', methods=['GET', 'POST'])
def salamanders_wkst_2():	
	if request.method == "POST":
		print("posted")
		student = session["student_name"]
		details = request.form
		print(details)
	return render_template('salamanders_wkst_2.html')

@app.route('/salamanders_wkst_3', methods=['GET', 'POST'])
def salamanders_wkst_3():	
	if request.method == "POST":
		print("posted")
		student = session["student_name"]
		details = request.form
		print(details)
	return render_template('salamanders_wkst_3.html')

@app.route('/garden_wkst_1', methods=['GET', 'POST'])
def garden_wkst_1():	
	if request.method == "POST":
		print("posted")
		student = session["student_name"]
		details = request.form
		print(details)
	return render_template('garden_wkst_1.html')

@app.route('/garden_wkst_2', methods=['GET', 'POST'])
def garden_wkst_2():	
	if request.method == "POST":
		print("posted")
		student = session["student_name"]
		details = request.form
		print(details)
	return render_template('garden_wkst_2.html')

@app.route('/garden_wkst_3', methods=['GET', 'POST'])
def garden_wkst_3():	
	if request.method == "POST":
		print("posted")
		student = session["student_name"]
		details = request.form
		print(details)
	return render_template('garden_wkst_3.html')

@app.route('/extraction_wkst_1', methods=['GET', 'POST'])
def extraction_wkst_1():	
	if request.method == "POST":
		print("posted")
		student = session["student_name"]
		details = request.form
		print(details)
	return render_template('extraction_wkst_1.html')

@app.route('/extraction_wkst_2', methods=['GET', 'POST'])
def extraction_wkst_2():	
	if request.method == "POST":
		print("posted")
		student = session["student_name"]
		details = request.form
		print(details)
	return render_template('extraction_wkst_2.html')

@app.route('/extraction_wkst_3', methods=['GET', 'POST'])
def extraction_wkst_3():	
	if request.method == "POST":
		print("posted")
		student = session["student_name"]
		details = request.form
		print(details)
	return render_template('extraction_wkst_3.html')

@app.route('/blissmeadows_wkst_1', methods=['GET', 'POST'])
def blissmeadows_wkst_1():	
	if request.method == "POST":
		print("posted")
		student = session["student_name"]
		details = request.form
		print(details)
	return render_template('blissmeadows_wkst_1.html')

@app.route('/blissmeadows_wkst_2', methods=['GET', 'POST'])
def blissmeadows_wkst_2():	
	if request.method == "POST":
		print("posted")
		student = session["student_name"]
		details = request.form
		print(details)
	return render_template('blissmeadows_wkst_2.html')

@app.route('/blissmeadows_wkst_3', methods=['GET', 'POST'])
def blissmeadows_wkst_3():	
	if request.method == "POST":
		print("posted")
		student = session["student_name"]
		details = request.form
		print(details)
	return render_template('blissmeadows_wkst_3.html')

@app.route("/logout")
def logout():
    session["teacher_name"] = None
    session["teacher_school"] = None
    session["selected_student"] = None
    session["student_name"] = None
    session["student_school"] = None
    session["s_teacher"] = None
    session["selected_video"] = None
    session["video_url"] = None
    return redirect("/")

@app.route('/videos')
def videos():
	return render_template('videos.html')

if __name__ == '__main__':
	app.run(debug=True)
