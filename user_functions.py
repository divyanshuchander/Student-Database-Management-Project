# Various framework functions


def sqlconnect():  # To connect sql with a cursor
    import mysql.connector as sql
    import global_variable as gv
    c = sql.connect(host=gv.host, user=gv.user,
                    passwd=gv.passwd, database=gv.database_name)
    return c

def adminmenu():  # Administrator menu
    print('-'*65)
    print('Welcome! Administrator')
    print('''	1. Add Student
	2. Delete Student
	3. Show Student full details
	4. Update Student Info
	5. Search Student
	6. Main Menu
    7. Change Admin Name
    8. Full System Delete
	9. Exit''')

    while True:
        n=int(input("Choice:\t"))
        if n == 1:
            adminadd()
        elif n == 2:
            print("Caution: It will delete student records")
            no=input("Enter admission no:\t ")
            admindelete(no)
        elif n == 3:
            admiss=input('Enter Admission Number:\t')
            fulldetails(admiss)
        elif n == 4:
            adminupdate()
        elif n == 5:
            adminsearch()
        elif n == 6:
            print()
            print()
            print('-'*60)
            break
        elif n == 7:
            changeadmin()
        elif n == 8:
            killall()
        elif n == 9:
            end()
        else:
            print('invalid choice')
    return





def end():  # program exit statement
    print('-'*65)
    print('Have a nice Day! BYE')
    exit()


def showdatabases():
    sql=sqlconnect()
    cursor=sql.cursor()
    cursor.execute('show databases')
    print(cursor.fetchall())
    sql.close()
    return


def adminadd():
    print('-'*65)
    sql=sqlconnect()
    cursor=sql.cursor()
    print('Enter the following details:')
    while True:

        admin=input('Enter admissionno:\t')
        fname=input('Enter first name:\t')
        lname=input('Enter last name:\t')
        Class=input('Enter class Assigned(like VIII,XI,etc):\t')
        Class.upper()
        roll=int(input('Enter Roll No:\t'))
        pfname=input("Enter Father's name:\t")
        pmname=input("Enter Mother's name:\t")
        phno=input("Enter Phone No.(mandatory):\t")
        email=input('Enter your Email-id:\t')
        a=(admin, fname, lname, Class, roll, pfname, pmname, phno, email)
        query="insert into student_details_basic values(%s,'%s','%s','%s',%s,'%s','%s',%s,'%s')" % a
        cursor.execute(query)
        query="insert into student_grades(Admission_No) values({})".format(
            admin)
        cursor.execute(query)
        query="insert into fee values({},0,0,1)".format(admin)
        cursor.execute(query)
        print('Student Added')
        sql.commit()

        print()
        loop=input('''	1.Add Again
	2.Main menu
	3.Exit 		:\t''')
        if loop == '1':
            continue
        elif loop == '2':
            break
        elif loop == '3':
            end()
    sql.commit()
    sql.close()


def admindelete(admiss):
    while True:
        sql=sqlconnect()
        cursor=sql.cursor()
        cursor.execute(
            "select First_name,Last_name from student_details_basic where Admission_No = {}".format(admiss))
        a=cursor.fetchone()
        cursor.execute(
            "delete from student_details_basic where Admission_No ={}".format(admiss))
        sql.commit()
        print("AdmissionNo", admiss, "successfully deleted whose details are\n", a)
        print()
        loop=input('''	1.Remove Again
	2.Main menu
	3.Exit 		:\t''')
        if loop == '1':
            continue
        elif loop == '2':
            break
        elif loop == '3':
            end()
    sql.commit()
    sql.close()


def adminupdate():
    sql=sqlconnect()
    cursor=sql.cursor()
    print('-'*65)
    choice=input('''Select option to update:
		1.Student information
		2.New fee update

			Choice:\t''')
    if choice == '1':
        print('-'*65)
        print("STUDENT INFORMATION UPDATE")
        admno=input("Enter Student's Admission No:\t")

        print('Select From the following options to update:')
        opt=input('''1.Update Phone number
2. Update E-mail ID
3. Update Student's Grades''')
        if opt == '1':
            phno=input("Enter New Phone number:\t")
            cursor.execute(
                "update student_details_basic set Phone_number = {} where Admission_No ={}".format(phno, admno))
            print('Phone number updated')
        elif opt == '2':
            email=input("Enter New Email-ID:\t")
            cursor.execute(
                "update student_details_basic set Email_id = '{}' where Admission_No ={}".format(email, admno))
            print('Email-ID updated')
        elif opt == '3':
            x=input('''Do you have
				1.Computer Science
				2.Physical Education\n:\t''')
            if x == '1':
                subjects=['Physics', 'Maths', 'Chemistry',
                            'English', 'Computer_science']
            elif x == '2':
                subjects= ['Physics', 'Maths', 'Chemistry', 'English', 'PHE']
            for a in subjects:
                marks= input('Enter {} Grades/%:\t'.format(a))
                cursor.execute(
                    "Update student_grades set {} = '{}' where Admission_No = {}".format(a, marks, admno))
            print("GRADES UPDATED!")
            sql.commit()

    elif choice == '2':
        newamount = input("Enter monthly amount to update fee database:\t")
        cursor.execute(
            "update fee set fee_due = fee_due+{} where fee_paid = 0".format(newamount))
        sql.commit()
        cursor.execute(
            "update fee set fee_due = {} where fee_paid = 1".format(newamount))
        sql.commit()
        cursor.execute("update fee set fee_paid = 0 where fee_paid = 1")
        sql.commit()

    else:
        print('Invalid Choice')
        print('-'*65)
    sql.commit()
    sql.close()


def mysqlrun():
    sql = sqlconnect()
    cursor = sql.cursor()
    cursor.execute('show tables')
    t = cursor.fetchall()
    print('''Tables are:
		''', t)
    sql.commit()
    sql.close()
    while True:
        sql = sqlconnect()
        cursor = sql.cursor()
        query = input('MysqlQuery>\t')
        try:
            cursor.execute(query)
            sql.commit()
            print('Query executed')
        except:
            print('Syntax Error!')

        if 'select' in query or 'desc' in query or 'show' in query:
            q = cursor.fetchall()
            print(q)
        elif query == 'exit':
            break

    sql.close()


def newoldcheck(admiss):

    sql = sqlconnect()
    cursor = sql.cursor()

    cursor.execute(
        'select*from Login_credentials where Admission_No = {}'.format(admiss))
    cursor.fetchone()
    present = cursor.rowcount
    if present == 0:
        return False
    elif present == 1:
        return True


def oldstulog(admiss):

    sql = sqlconnect()
    cursor = sql.cursor()
    cursor.execute(
        'Select passwd from Login_credentials where Admission_No = {}'.format(admiss))
    a = cursor.fetchone()
    for i in a:
        p = i
    cursor.execute(
        'Select First_name from student_details_basic where Admission_No = {}'.format(admiss))
    n = cursor.fetchone()
    sql.close()
    for i in n:
        name = i
    while True:
        passwd = input('Please Enter your Password:')

        if p == passwd:
            print('Hi!', name)
            return True

        else:
            print('Wrong password. TRY AGAIN')


def newstulog(admiss):
    sql = sqlconnect()
    cursor = sql.cursor()
    cursor.execute(
        'select Phone_number from student_details_basic where Admission_No ={}'.format(admiss))
    ph = cursor.fetchall()
    a = ph[0][0]
    print('Temporary OTP sent to phone number:\t', a)
    passwd = input('Set your account passwd:\t')
    cursor.execute(
        "insert into Login_credentials values({},{},'{}')".format(admiss, a, passwd))
    print('Please Wait... ')
    sql.commit()
    sql.close()
    print()


def gradecheck(admiss):
    sql = sqlconnect()
    cursor = sql.cursor()
    cursor.execute(
        'select * from student_grades where Admission_No = {}'.format(admiss))
    a = cursor.fetchall()
    print('''+-------+-------+-----------+---------+------------------+------+-----------+
	| Physics | Maths | Chemistry | English | Computer_science | PHE  |
	+---------+-------+-----------+---------+------------------+------+
	|  {}     | {}    |     {}    |   {}    |        {}        |  {} |
 +---------+-------+-----------+---------+------------------+------+'''.format(a[0][1], a[0][2], a[0][3], a[0][4], a[0][5], a[0][6]))
    print('')
    sql.close()


def feecheck(admiss):
    sql = sqlconnect()
    cursor = sql.cursor()
    cursor.execute('select*from fee where Admission_No = {}'.format(admiss))
    a = cursor.fetchall()
    a = a[0]
    fdue = a[1]
    ftotal = a[2]
    fpaid = a[3]
    if fpaid == 0:
        print("				YOU HAVE NOT PAID THE FEE")
        print("Total Due Amount:\t", fdue)
        pay = input('1.To pay fee(else skip):\t')
        if pay == '1':
            print('Please Wait... Processing Payment')
            cursor.execute(
                'update fee set fee_due = 0 where Admission_No = {}'.format(admiss))
            sql.commit()
            cursor.execute(
                'update fee set fee_paid = 1 where Admission_No = {}'.format(admiss))
            sql.commit()
            print('Fee of', fdue, 'has been paid.\n ThankYou!')

    elif fpaid == 1:
        print('Fee has been paid')
    sql.close()
    print()


def basicinfo(admiss):
    sql = sqlconnect()
    cursor = sql.cursor()
    cursor.execute(
        'select * from student_details_basic where Admission_No = {}'.format(admiss))
    a = cursor.fetchall()
    print(a)
    ph = input('''1. Want to Update Phone number
		2. Want to update Email(else skip):\t''')
    if ph == '1':
        newnumber = input('Please Enter your new Phone number:\t')
        cursor.execute('update student_details_basic set Phone_number ={} where Admission_No ={}'.format(
            newnumber, admiss))
        sql.commit()
        cursor.execute('update Login_credentials set Phone_number ={} where Admission_No ={}'.format(
            newnumber, admiss))
        sql.commit()
        print('Information updated!!!')
        print()
    elif ph == '2':
        newmail = input('Please Enter your new Email:\t')
        cursor.execute(
            "update student_details_basic set Email_id ='{}' where Admission_No ={}".format(newmail, admiss))
        print('Information updated!!!')
        print()
        sql.commit()
    sql.close()
    print()


def passupdate(admiss):
    sql = sqlconnect()
    cursor = sql.cursor()
    print('Password Update:')
    newpass = input('Please Enter your new Password:\t')
    cursor.execute(
        "update Login_credentials set passwd ='{}' where Admission_No ={}".format(newpass, admiss))
    print('New Password Updated')
    sql.commit()
    sql.close()
    print()


def student(admiss):
    while True:
        print('		---------------------------------------------------')
        i = input('''\t\t\t1.Check your Grades
			2.FEE
			3.Your basic info
			4.Update Password
			5.Main Menu
			6.Exit
			Your Choice:\t''')
        if i == '1':
            gradecheck(admiss)
        elif i == '2':
            feecheck(admiss)
        elif i == '3':
            basicinfo(admiss)
        elif i == '4':
            passupdate(admiss)
        elif i == '5':
            print()
            print()
            print()
            break
        elif i == '6':
            end()
        else:
            print('Invalid Option')
            print()
            print()


def adminsearch():
    sql = sqlconnect()
    cursor = sql.cursor()
    searchdomain_intial = {'Admission_No': '', 'First_name': '',
                           'Father_name': '', 'Mother_name': '', 'Phone_number': '', 'Email': ''}
    searchdomain_final = {}
    for d in searchdomain_intial:
        a = input("Enter {} (Else skip):\t".format(d))
        if a == '':
            continue
        else:
            searchdomain_final[d] = a
    result = []
    rowcount = 0
    res = []

    for n in searchdomain_final:
        cursor.execute(
            "select*from student_details_basic where {} Like '%{}%' ".format(n, searchdomain_final[n]))
        a = cursor.fetchall()
        result.extend(a)
    for x in result:
        if x not in res:
            res.append(x)
    result = res

    print(searchdomain_final.keys())
    for s in result:
        print(s)
    print('-' * 65)
    sql.close()
    return


def fulldetails(admiss):
    sql = sqlconnect()
    cursor = sql.cursor()
    cursor.execute(
        'select*from student_details_basic where Admission_No = {}'.format(admiss))
    a = cursor.fetchall()
    print(a)
    cursor.execute('select*from fee where Admission_No = {}'.format(admiss))
    a = cursor.fetchall()
    a = a[0]
    fdue = a[1]
    ftotal = a[2]
    fpaid = a[3]
    if fpaid == 0:
        print("	Fee has not been paid!!!")
        print("Total Due Amount:\t", fdue)
    elif fpaid == 1:
        print('Fee has been paid')
        cursor.execute(
            'select * from student_grades where Admission_No = {}'.format(admiss))
    a = cursor.fetchall()
    print('Grades are:')
    print('''			+-------+-------+-----------+---------+------------------+------+-----------+
			 | Physics | Maths | Chemistry | English | Computer_science | PHE  |
			 +---------+-------+-----------+---------+------------------+------+
			 |  {}     | {}    |     {}    |   {}    |        {}        |  {} |
			 +---------+-------+-----------+---------+------------------+------+
	'''.format(a[0][1], a[0][2], a[0][3], a[0][4], a[0][5], a[0][6]))
    print()
    print()
    sql.close()
    return

def changeadmin():
    print("Caution changing admin name:\t")
    newadmin = input("Enter new admins name:\t")
    import global_variable as gv
    gv.admin_name = newadmin
    print("Admin name has been successfully changed to",newadmin)
    return


def killall():
    import global_variable as gv
    print("Are you really serious?")
    while True:
        print('1.Yes')
        print('2.No')
        c = int(input("-->\t"))
        if c == 2:
            print("Full deletion of database cancelled!")
            return
        elif c == 1:
            print("!!!Caution you are going to delete all of your stored data!!!")
            print("To finally delete your Data type below your organisation_name:")
            while True:
                dname = str(input("-->:\t")).lower()
                rdname = gv.organisation_name
                if dname == rdname:
                    c = sqlconnect()
                    cursor = c.cursor()
                    print('Deleting database...')
                    print("Please Wait...")
                    query = "drop database {}".format(gv.database_name)
                    cursor.execute(query)
                    print("Sorry to see you go!")
                    end()   
                else:
                    print("Wrong name entered!")
                    print('1.Try again')
                    print('2.Cancel')
                    c = int(input(":\t"))
                    if c == 1:
                        continue
                    elif c == 2:
                        print("Deletion cancelled!")
                        return
        else:
            print("invalid choice")
   