# the main framework for programming
import user_functions as func 
import global_variable as gv




print('		---------------------------------------------------')
print("				  '",gv.organisation_name.upper(), "'			",sep ='')
print('		---------------------------------------------------')
print('			   Student Database Management')
print('		---------------------------------------------------')
print('\t\t***Designed and Maintained By "{}"***'.format(gv.admin_name))
print('		---------------------------------------------------')
print()
while True:
	choice = ''
	while True:
		choice = input('''	1.Data Administrator
	2.Student Login
			Your Choice =\t''')
		if choice != '1' and choice!='2':
			print("invalid input- TRY AGAIN")
			print('-' * 65)
			continue
		break

	if choice == '1':
		print('!!Administrator!!')
		adminpass = input('Enter Admin Password:\t')
		if adminpass == gv.passwd:			
			func.adminmenu()					
		else:
			print('Invalid Password')
			print('*'* 65)
			print()
			continue




	elif choice =='2':

		print('!!Student Login!!')
		print("Welcome to Student Database!!!")
		admission = input('Enter your Admission Number:\t')
		a = func.newoldcheck(admission)
		
		if a is True:
			print('Welcome student')
			b = func.oldstulog(admission)
			if b is True:
				func.student(admission)


		elif a is False:
			print('New Student Registration')
			func.newstulog(admission)
			func.student(admission)



