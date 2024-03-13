# UMM (University of Michigan Marketplace)

## Description

UMM (University of Michigan Marketplace) is an online platform designed for students, faculty, and staff at the University of Michigan to buy, sell, and trade goods within the campus community. Whether you're looking to declutter your dorm room, find textbooks for your next semester, or discover unique items from fellow Wolverines, UMM provides a convenient and secure way to connect with your peers and engage in sustainable consumption.

## Requirements

To run UMM locally or deploy it on a server, you'll need the following:

- **Python**: UMM is built with Django, a Python web framework. Make sure you have Python installed on your system. You can download it from [python.org](https://www.python.org/).

- **Django**: Install Django using pip, the Python package manager. You can install Django by running `pip install Django`.

- **Database**: UMM uses a database to store user information, product listings, and transaction records. You can use SQLite for development purposes or choose a more robust database like PostgreSQL for production deployments.

- **Dependencies**: UMM relies on various Python packages and libraries. Install the dependencies listed in the `requirements.txt` file using `pip install -r requirements.txt`.

- **Environment Variables**: Set up environment variables for sensitive information such as secret keys, database credentials, and API keys. You can use a `.env` file to manage your environment variables.

- **Static and Media Files**: Configure Django to serve static files (CSS, JavaScript) and media files (images, documents) correctly. This may involve setting up static and media root directories in your Django settings.

- **Deployment**: If you're deploying UMM on a server, ensure you have a suitable hosting environment (e.g., Heroku, AWS) and follow best practices for security, scalability, and performance.

For detailed instructions on setting up and running UMM, please refer to the documentation or contact the repository owner.

## Environment Setup
### Tips:
You can replace python with python3 if not found.
For steps with (*), you need to download MySQL, and then run
```
mysql -u root -p
```
so that your terminal looks like 
```
mysql>
```
Now, you can run codes in those steps.
### Steps:
0. Database setup (*)
```
CREATE DATABASE platform CHARACTER SET UTF8;

CREATE USER DBprojectUser@localhost IDENTIFIED BY 'password';

GRANT ALL PRIVILEGES ON platform.* TO DBprojectUser@localhost;

FLUSH PRIVILEGES;
```
1. virtualenv
```
pip install virtualenv
```
2. mysql
```
sudo apt-get install mysql-server
sudo apt-get install libmysqlclient-dev
```
For MAC users, replace "sudo apt-get" with "brew".

3. create the virtual environment
```
virtualenv $environment_name
```
For MAC/Unix users,
```
python3 -m venv .venv
```
4. activate the virtual environment
```
source path/to/env/folder/bin/activate
# install required packages
pip install -r requirments.txt
```
5. Django basic setup
```
python manage.py makemigrations
python manage.py migrate
# create a superuser
python manage.py createsuperuser
```
6. Load DB schema (*)
```
source [project dir]/DB-SecondHand.sql
```
7. Run server
```
python manage.py runserver
```
## Disclaimer

This project is based on code originally created as part of a school project by [Huang Jiahui] and [Joji James Anaghan, Su Qiulin, Wu Lingyun, Zhang Jiaxuan], which was made available on GitHub [https://github.com/Gabriel-Huang/SUTD_SecondHandGoods_Platform]. After contacting the original creators, they have granted permission for the use and modification of their code for the development of this project.

While efforts have been made to ensure that the code is used responsibly and ethically, it is important to note the following:

- This project is provided as-is, without any warranty or guarantee of fitness for any particular purpose.
- The original creators and contributors are not liable for any damages or liabilities arising from the use of this project.
- Users of this project are responsible for ensuring compliance with all applicable laws, regulations, and ethical guidelines.
- Any modifications or enhancements made to the original code are the sole responsibility of the current project maintainers.

By using this project, you agree to abide by the terms and conditions outlined in this disclaimer. Additionally, it is acknowledged that I retain ownership rights over any modifications or enhancements made to the original code, including the right to commercialize the project in the future.

If you have any questions or concerns regarding the use of this project, please contact [cassiez@umich.edu].
