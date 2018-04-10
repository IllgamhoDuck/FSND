# Linux Server Configuration

Greeting Humans! I'm the duck from illgamho lake! QUARK!
![aily](https://github.com/IllgamhoDuck/FSDN-Project-6-Linux-Server-Configuration/blob/master/aily.png?raw=true)
This project will take a baseline installation of a Linux distribution on a virtual machine and prepare it to host your web applications, to include installing updates, securing it from a number of attack vectors and installing/configuring web and database servers.

1. **Create Server** - Using Lightsail create instance / Update package
2. **Securing Server** - Configure Firewall / Change SSH port
3. **Create User** - Add a user who has sudo privilege
4. **Key based authentication** - Add authentication and block password
5. **Apache & wsgi** - Install the apache server & wsgi
6. **PostgreSQL** - Install the PostgreSQL database
7. **UX** - Good User Experience

##### IP 52.193.203.176
##### SSH port 2200
##### Website URL  http://52.193.203.176/


## Summary of software installation and configuration changes made
___
### 1 - Get your server [**Amazon Lightsail**]
1. Made Ubuntu Instance
2. The instance is Named `illgamho-duck`
3. Login by the button Connect Using SSH that amazon provided

##### If your logout, login with below code 
`ssh ubuntu@52.193.203.176 -p 2200 -i LightsailDefaultPrivateKey-ap-northeast-1.pem`

### 2 - Update all currently installed packages
1. `sudo apt-get update`
2. `sudo apt-get upgrade`

### 3 - Change the SSH port from 22 to 2200
1. `sudo nano /etc/ssh/sshd_config`
2. Change **port 22** -> **port 2200**
3. `sudo service ssh restart`

### 4 - Make sure to configure the Lightsail firewall to allow it
1. Add 123 (NTP port) / 2200 (New SSH port)
![change the setting](https://github.com/IllgamhoDuck/FSDN-Project-6-Linux-Server-Configuration/blob/master/lightsail%20networking%20setting.png?raw=true)

### 5 - Configure the Uncomplicated Firewall (UFW)
1. `sudo ufw default deny incoming`
2. `sudo ufw default allow outgoing`
3. `sudo ufw allow 2200/tcp` - **SSH**
4. `sudo ufw allow 80/tcp` - **HTTP**
5. `sudo ufw allow 123/tcp` - **NTP**
6. `sudo ufw deny 22` - Disable the default SSH port
7. `sudo ufw enable`

### 6 - Create a new user account named grader
1. `sudo adduser grader`
2. Enter password

### 7 - Give grader the permission to sudo
1. `sudo touch /etc/sudoers.d/grader`
2. `sudo nano /etc/sudoers.d/grader`
3. Add `grader ALL=(ALL) NOPASSWD:ALL` - Never mistake here

### 8 - Create an SSH key pair for grader
[**This is done at Local Computer**]
1. Open git bash or terminal
2. `ssh-keygen`
3. Enter the path for the key - I named it `ducky`
4. We don't need to change /etc/ssh/sshd_config because it already set `PasswordAuthentication` to `no`

### 9 - Give public key to grader
[**Now done at remote server now**]
At here we will use `ubuntu` user because `grader` user cannot
login yet because there are no key provided.
1. `cd /home/grader`
2. `ls -al`
3. `sudo mkdir .ssh`
4. `sudo touch .ssh/authorized_keys`
5. `sudo nano .ssh/authorized_keys`
6. Copy & Paste the `~/.ssh/ducky.pub` to here 
7. `sudo chmod 700 .ssh`
8. `sudo chown grader .ssh`
9. `sudo chgrp grader .ssh`
10. `sudo chmod 644 .ssh/authorized_keys`
11. `sudo chown grader .ssh/authorized_keys`
12. `sudo chgrp grader .ssh/authorized_keys`

### 10 - Login as User grader
1. `ssh grader@52.193.203.176 -p 2200 -i [private key path]`
2. Logout `ubuntu` User - **[Ctrl-D]**

### 11 - Configure the local timezone to UTC
1. `sudo dpkg-reconfigure tzdata`
2. None above or etc
3. UTC

### 12 - Install Apache & mod wsgi
1. `sudo apt-get install apache2`
2. `sudo apt-get install libapache2-mod-wsgi`
3. `sudo service apache2 restart`
4. Check `52.193.203.176` if it is working.

### 13 - Add FlaskApp folder for using wsgi
1. `cd /var/www`
2. `sudo mkdir FlaskApp`
3. `cd FlaskApp/`

### 14 - Download the Item-Catalog Project
1. `sudo apt-get install git`
2. `sudo git clone https://github.com/IllgamhoDuck/catalog.git`
3. `sudo mv ./catalog ./FlaskApp`
4. `cd FlaskApp`
5. `sudo mv Ai.py __init__.py`

### 15 - Install PostgreSQL
1. `sudo apt-get install postgresql`
2. `sudo nano /etc/postgresql/9.5/main/pg_hba.conf`
3. PostgreSQL do not allow remote connections
4. `sudo su - postgres`
5. `psql`
6. `CREATE USER catalog WITH PASSWORD 'ducky';`
7. `CREATE DASTABASE ai;`
8. `GRANT ALL PRIVILEGES ON DATABASE ai TO catalog;`
9. \q
10. `exit` 

### 16 - Install python & library
1. `sudo apt-get install python-setuptools`
2. `sudo apt-get install python-pip`
3. `pip install --upgrade pip`
4. `sudo apt-get install python-sqlalchemy`
5. `sudo apt-get install python-flask`
6. `sudo apt-get install python-psycopg2`
7. `sudo apt-get install redis-server`
8. `sudo pip install passlib`
9. `sudo pip install httplib2`
10. `sudo pip install requests`
11. `sudo pip install oauth2client`
12. `sudo pip install redis`

### 17 - Populate the Database [**ai**]
1. `sudo python Aimodels.py`
2. `sudo python Aimodels_populating.py`

### 18 - Configure Apache & mod wsgi
1. `sudo nano /etc/apache2/sites-available/FlaskApp.conf`
2. Write the following
```
<VirtualHost *:80>
		ServerName  52.193.203.176
		ServerAdmin hyunbyung87@gmail.com
		WSGIScriptAlias / /var/www/FlaskApp/flaskapp.wsgi
		<Directory /var/www/FlaskApp/FlaskApp/>
			Order allow,deny
			Allow from all
		</Directory>
		Alias /static /var/www/FlaskApp/FlaskApp/static
		<Directory /var/www/FlaskApp/FlaskApp/static/>
			Order allow,deny
			Allow from all
		</Directory>
		ErrorLog ${APACHE_LOG_DIR}/error.log
		LogLevel warn
		CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```
3. `cd /var/www/FlaskApp`
4. `sudo a2ensite FlaskApp`
5. `sudo nano flaskapp.wsgi`
6. Write the following
```
#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/FlaskApp/")

from FlaskApp import app as application
application.secret_key = 'Super_secret_key'
```


### 19 - .git directory is not publicly accessible via a browser
1. `cd .git`
2. `sudo nano .htaccess`
3. Write the following
```
Order allow, deny
Allow from all
```

### 20 - Add google / facebook OAUTH 
Add google & facebook oauth Authorized **JavaScript Origins below**
1. http://52.193.203.176/

### 21 - Let the Service begin!!! QUARK!!!
1. `sudo service apache2 reload`
2. http://52.193.203.176/




