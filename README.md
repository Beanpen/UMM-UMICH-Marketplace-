# UMM (University of Michigan Marketplace)

## Description

UMM (University of Michigan Marketplace) is an online platform designed for students, faculty, and staff at the University of Michigan to buy, sell, and trade goods within the campus community. Whether you're looking to declutter your dorm room, find textbooks for your next semester, or discover unique items from fellow Wolverines, UMM provides a convenient and secure way to connect with your peers and engage in sustainable consumption.

## Requirements

To run UMM locally or deploy it on a server, you'll need the following:

- **Python**: Python is a high-level, general-purpose programming language.

- **Django**: Django is a free and open-source, Python-based web framework that runs on a web server.

- **Database**: local uses [MySQL](https://dev.mysql.com/downloads/shell/), on cloud uses RDS (still MySQL)

- **Other Dependencies**: pytz allows accurate and cross platform timezone calculations using Python 2.4 or higher. 

- **Environment Variables**: Set up environment variables for sensitive information such as timezone information, RDS database setups in settings.py.

- **Static and Media Files**: Configure Django to serve static files (CSS, JavaScript) and media files (images, documents) correctly. This may involve setting up static and media root directories in your Django settings.

- **Deployment**: If you're deploying UMM on a server, ensure you have a suitable hosting environment (e.g., Heroku, AWS) and follow best practices for security, scalability, and performance. I used EC2 from AWS in this project.

For detailed instructions on setting up and running UMM, please refer to the documentation or contact me.

## Environment Setup
### Tips:
You can replace python3 with python if not found.
For steps with (*), you need to download MySQL, and then run
```
mysql -u root -p
```
so that your terminal looks like 
```
mysql>
```
Now, you can run codes in those steps.
Similarly, I used RDS (mysql) as the cloud database and EC2 from AWS to deploy it so,
```
mysql -h YOUR_RDS_Database.rds.amazonaws.com -P 3306 -u YOUR_USER_NAME -p
```
### Steps:
1. Database setup (*)
```
CREATE DATABASE platform CHARACTER SET UTF8;

CREATE USER DBprojectUser@localhost IDENTIFIED BY 'password';

GRANT ALL PRIVILEGES ON platform.* TO DBprojectUser@localhost;

FLUSH PRIVILEGES;
```
2.1 If you are not using virtual environment:
```
# Install required packages
pip install -r requirements.txt

# Django basic setup
python3 manage.py makemigrations
python3 manage.py migrate

# Create a superuser
python3 manage.py createsuperuser

# Load DB schema (* run in mysql)
source [project dir]/DB-SecondHand.sql

# Run server
python3 manage.py runserver #add a port here if you would like to specify
```
2.2 If you are using virtual environment (recommended for most cases):
```
pip install virtualenv

# For MAC/Unix users,
python3 -m venv .venv

# Activate the virtual environment (change the path if different)
source env/bin/activate

# Install required packages
pip install -r requirements.txt

# Django basic setup
python3 manage.py makemigrations
python3 manage.py migrate

# Create a superuser
python3 manage.py createsuperuser

# Load DB schema (*)
source [project dir]/DB-SecondHand.sql

# Run server
python3 manage.py runserver #add a port here if you would like to specify
```
Read more about makemigrations and migrate [here](https://www.geeksforgeeks.org/django-basic-app-model-makemigrations-and-migrate/).

## Disclaimer

This project is based on code originally created as part of a school project by [Huang Jiahui] and [Joji James Anaghan, Su Qiulin, Wu Lingyun, Zhang Jiaxuan], which was made available on [GitHub] (https://github.com/Gabriel-Huang/SUTD_SecondHandGoods_Platform). After contacting the original creators, they have granted permission for the use and modification of their code for the development of this project.

While efforts have been made to ensure that the code is used responsibly and ethically, it is important to note the following:

- This project is provided as-is, without any warranty or guarantee of fitness for any particular purpose.
- The original creators and contributors are not liable for any damages or liabilities arising from the use of this project.
- Users of this project are responsible for ensuring compliance with all applicable laws, regulations, and ethical guidelines.
- Any modifications or enhancements made to the original code are the sole responsibility of the current project maintainers.

By using this project, you agree to abide by the terms and conditions outlined in this disclaimer. Additionally, it is acknowledged that I retain ownership rights over any modifications or enhancements made to the original code, including the right to commercialize the project in the future.

If you have any questions or concerns regarding the use of this project, please contact [cassiez@umich.edu].
