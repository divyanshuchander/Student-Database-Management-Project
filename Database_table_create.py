# for sql table creation & table related constants
import mysql.connector as sql
fh = open('global_variable.py', 'w+')
input('Welcome! To create your database: (Press ENTER)')

while True:
    try:
        host = input("Please Enter host name:\t")
        fh.write("host = '{}'\n".format(host))
        user = input('Enter User_Name:\t')
        fh.write("user = '{}'\n".format(user))
        passwd = input('Enter password:\t\t')
        fh.write("passwd = '{}'\n".format(passwd))
        print('Please Wait...')
        connection = sql.connect(host=host, user=user, passwd=passwd)
        if connection.is_connected():
            print('Your Database system is connected!!!')
            cursor = connection.cursor()            
            break
    except:
        print('Try Again: y')
        print('Exit: n''')
        end = input("Your Choice:\t ").lower()
        if end == 'n':
            exit()
        continue
organisation_name = input(
    'Enter Name of Organisation(use underscore for space):\t')
fh.write("organisation_name = '{}'\n".format(organisation_name))
database_name = "{}_studentdata".format(organisation_name)
fh.write("database_name = '{}'\n".format(database_name))
admin_name = input("Enter Administrator's Name(can be changed later):\t")
fh.write("admin_name = '{}'".format(admin_name))
fh.close()
while True:
    try:
        query = 'create database {}'.format(database_name)
        cursor.execute(query)
        break
    except:
        print('''Database already exists''')
        exit()
print('Please Wait...')
query = 'use {}'.format(database_name)


#Table making queries
cursor.execute(query)
cursor.execute('''create table student_details_basic (Admission_No integer primary key,
	First_name varchar(30) not null, 
	Last_name varchar(30) not null,
	Class varchar(5),
	Rollno integer,
	Father_Name varchar(30),
	Mother_Name varchar(30),
	Phone_number bigint,
	Email_id varchar(30)) ''')
connection.commit()

cursor.execute('''create table Login_credentials (Admission_No int(11), foreign key (Admission_No) references student_details_basic (Admission_No) on delete cascade on update cascade,
	 Phone_number bigint, 
	passwd varchar(30) not null)''')
connection.commit()

cursor.execute('''create table student_grades (Admission_No int(11), foreign key (Admission_No) references student_details_basic (Admission_No)
				on delete cascade on update cascade,Physics varchar(3) default null,
				Maths varchar(3) default null, Chemistry varchar(3) default null,
				English varchar(3) default null, Computer_science varchar(3) default null,
				PHE varchar(3) default null)''')
connection.commit()
cursor.execute('''create table fee (Admission_No int(11),foreign key (Admission_No) references student_details_basic (Admission_No)
				on delete cascade on update cascade,
				fee_due integer, fee_total integer, fee_paid tinyint(1))''')  # boolean value to check if fee paid or not
connection.commit()

print('Your Tables are successfully created')

connection.close()

