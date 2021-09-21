import psycopg2
from sshtunnel import SSHTunnelForwarder
import sys

def connect_to_database():
	global cur_main
	global conn_main
	conn_main = None

	info_testing = ['hF8$!nfshGAgxPch', 'localhost', 'disable']
	info_production = ['qF7gk3JFrE7Do49z6T', '23.239.24.84', 'require']

	# Change this to move fromt esting to production and vice versa
	info = info_testing

	# In PostgreSQL, default username is 'postgres' and password is 'postgres'.
	# And also there is a default database exist named as 'postgres'.
	# Default host is 'localhost' or '127.0.0.1'
	# And default port is '54322'.
	try:

		# server = SSHTunnelForwarder(('23.239.24.84', 22),
		#          ssh_username='guido',
		#          ssh_password='zajbQz7#7bfyke!B',
		#          remote_bind_address=('localhost', 5432),
		#          local_bind_address=('localhost', 5432))

		# server.start()


		conn_main = psycopg2.connect(
			dbname='postgres',
			user="postgres",
			password=info[0],
			host=info[1],
			port='5432',
			sslmode=info[2])
		conn_main.autocommit = True

		print('Default database connected.')
	except:
		print("Could not connect to default database")

	# If connected to default database
	if conn_main != None:
		cur_main = conn_main.cursor()

		cur_main.execute("SELECT datname FROM pg_database;")

		list_database = cur_main.fetchall()
		print(list_database)


		main_database_name = "bms_inventory"


		if (main_database_name,) in list_database:
			print("SUCCESS: '{}' database already exist".format(main_database_name))
			database_exists = True
		else:
			print("WARNING: '{}' Database not exist.".format(main_database_name))
			database_exists = False

		if database_exists == False:
			print("Creating inventory database...")

			cur_main.execute(f"CREATE DATABASE {main_database_name};")
			conn_main.commit()

			# Closes Cursor and Login from default database
			cur_main.close()
			conn_main.close()

			# Connects to main database
			conn_main = psycopg2.connect(
				dbname=main_database_name,
				user="postgres",
				password=info[0],
				host=info[1],
				port='5432',
				sslmode=info[2])
			conn_main.autocommit = False

			print("Connected to database.")

			# Creates cursor for main database
			cur_main = conn_main.cursor()

			cur_main.execute("""CREATE TABLE individual_category (
				id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
				category_name VARCHAR);""")

			cur_main.execute("""CREATE TABLE stacked_category (
				id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
				category_name VARCHAR);""")

			cur_main.execute("""CREATE TABLE inv_user (
				id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
				username VARCHAR,
				password VARCHAR);""")

			cur_main.execute("""CREATE TABLE individual_equipment (
				inv_num VARCHAR PRIMARY KEY,
				brand VARCHAR,
				model VARCHAR,
				country VARCHAR,
				serial_number VARCHAR,
				description VARCHAR,
				base_price REAL,
				price REAL,
				import_date TIMESTAMP,
				export_date TIMESTAMP,
				category_id INTEGER,
				import_user_id INTEGER,
				export_user_id INTEGER,
				CONSTRAINT fk_ind_category_id FOREIGN KEY(category_id) REFERENCES individual_category(id),
				CONSTRAINT fk_import_user_id FOREIGN KEY(import_user_id) REFERENCES inv_user(id),
				CONSTRAINT fk_export_user_id FOREIGN KEY(export_user_id) REFERENCES inv_user(id));""")

			cur_main.execute("""CREATE TABLE stacked_equipment (
				inv_num VARCHAR PRIMARY KEY,
				brand VARCHAR,
				model VARCHAR,
				country VARCHAR,
				serial_number VARCHAR,
				description VARCHAR,
				base_price REAL,
				price REAL,
				quantity INTEGER,
				category_id INTEGER,
				import_user_id INTEGER,
				export_user_id INTEGER,
				CONSTRAINT fk_stacked_category_id FOREIGN KEY(category_id) REFERENCES stacked_category(id),
				CONSTRAINT fk__import_user_id FOREIGN KEY(import_user_id) REFERENCES inv_user(id),
				CONSTRAINT fk_export_user_id FOREIGN KEY(export_user_id) REFERENCES inv_user(id));""")

			cur_main.execute("""CREATE TABLE stacked_import (
				quantity INTEGER,
				import_date TIMESTAMP,
				equipment_inv_num VARCHAR,
				CONSTRAINT fk_inv_num FOREIGN KEY(equipment_inv_num) REFERENCES stacked_equipment(inv_num));""")

			cur_main.execute("""CREATE TABLE stacked_export (
				quantity INTEGER,
				export_date TIMESTAMP,
				equipment_inv_num VARCHAR,
				CONSTRAINT fk_inv_num FOREIGN KEY(equipment_inv_num) REFERENCES stacked_equipment(inv_num));""")

			cur_main.execute("""CREATE TABLE master_password(
				id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
				name VARCHAR,
				password VARCHAR);""")

			conn_main.commit()
			add_master_password()

		else:
			print("Database already existed. None created")


def delete_database():

	info_testing = ['hF8$!nfshGAgxPch', 'localhost', 'disable']
	info_production = ['qF7gk3JFrE7Do49z6T', '23.239.24.84', 'require']

	# Change this to move fromt esting to production and vice versa
	info = info_testing

	try:

		# server = SSHTunnelForwarder(('23.239.24.84', 22),
		#          ssh_username='guido',
		#          ssh_password='zajbQz7#7bfyke!B',
		#          remote_bind_address=('localhost', 5432),
		#          local_bind_address=('localhost', 5432))

		# server.start()

		conn_main = psycopg2.connect(
			dbname='postgres',
			user="postgres",
			password=info[0],
			host=info[1],
			port='5432',
			sslmode=info[2])
		conn_main.autocommit = True

		print('Default database connected.')
	except:
		print("Could not connect to default database")

	# If connected to default database
	if conn_main != None:
		cur_main = conn_main.cursor()

		main_database_name = "bms_inventory"

		cur_main.execute("SELECT datname FROM pg_database;")

		list_database = cur_main.fetchall()
		print("BEFORE:")
		print(list_database)


		cur_main.execute(f"DROP DATABASE {main_database_name};")
		conn_main.commit()

		cur_main.execute("SELECT datname FROM pg_database;")

		list_database = cur_main.fetchall()
		print("AFTER")
		print(list_database)


def add_master_password():
	# connect_to_database2()
	query = "INSERT INTO master_password (name, password) VALUES (%s, %s)"
	query_data = ("guido", "cbcN3YP")

	cur_main.execute(query, query_data)
	conn_main.commit()
	print("Master Password Added")


delete_database()

connect_to_database()
