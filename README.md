## ECS Digital - Technical Assessment ##

The following use case might be a real-life example from one of our customers, please deliver your best possible solution. Please go through the described scenario and write a script, in one of the below languages, implementing a fix to the issue below. For the development of the scripts you have 4 hours and are allowed to use Google and any other material as long as the work submitted was written by you.

- Use Case:

1. A database upgrade requires the execution of numbered SQL scripts stored in a specified folder, named such as '045.createtable.sql'.
2. There may be gaps in the SQL file name numbering and there isn't always a . (dot) after the beginning number.
3. The database upgrade is based on looking up the current version in the database and comparing this number to the numbers in the script names.
4. If the version number from the db matches the highest number from the scripts then nothing is executed.
5. All scripts that contain a number higher than the current db version will be executed against the database in numerical order.
6. In addition, the database version table is updated after the script execution with the executed script's number.

- Requirements:
  - Supported Languages: Bash, Python2.7, PHP, Shell, Ruby, Powershell - No other languages will be accepted
  - You will have to use a MySQL 5.7 database
  - The scripts may contain any simple SQL statement(s) to any table of your choice, e.g. 'INSERT INTO testTable VALUES("045.createtable.sql");'
  - The table where the current db version is stored is called 'versionTable', with a single row for the version, called 'version'
  - Your script will be executed automatically via a program, and must satisfy these command line input parameters exactly in order to run:
    ```bash
    ./your-script.your-lang directory-with-sql-scripts username-for-the-db db-host db-name db-password
    ```

  ### Example Output: ###
  ```bash
  $ src/mysql_updatetables.py mysql-scripts root localhost ecs test
  mysql-scripts/01.createtable.sql script will not be executed
  mysql-scripts/2.createtable.sql script will not be executed
  mysql-scripts/03.createtable.sql script will not be executed
  mysql-scripts/004createtable.sql script will not be executed
  mysql-scripts/042.createtable.sql script will not be executed
  mysql-scripts/044.createtable.sql script will not be executed
  mysql-scripts/048.createtable.sql script will not be executed
  running mysql-scripts/052createtable.sql script
  VersionTable updated. Current version is now: 52
  running mysql-scripts/125.createtable.sql script
  /usr/local/lib/python2.7/site-packages/pymysql/cursors.py:170: Warning: (1007, "Can't create database 'myschema'; database exists")
    result = self._query(query)
  VersionTable updated. Current version is now: 125
  running mysql-scripts/127createtable.sql script
  VersionTable updated. Current version is now: 127
  running mysql-scripts/229createtable.sql script
  /usr/local/lib/python2.7/site-packages/pymysql/cursors.py:170: Warning: (1007, "Can't create database 'myschema2'; database exists")
    result = self._query(query)
  VersionTable updated. Current version is now: 229
  running mysql-scripts/731.createtable.sql script
  VersionTable updated. Current version is now: 731
  ```

### HOW TO RUN IT ###
* Download the repository
  ```bash
  git clone git@github.com:semenowiczk/mysql-updatetables.git ; cd mysql-updatetables
  ```
* Run mysql server with docker
  ```bash
  docker run --name ecs-mysql -e MYSQL_DATABASE=ecs -e MYSQL_ROOT_PASSWORD=test -p 3306:3306 mysql:5.7
  ```
* Make sure versionTable exists in ecs database
  ```bash
  mysql -h 127.0.0.1 -u root --password=test ecs < initdb.sql
  ```
* run the script: *./src/mysql_updatetables.py directory-with-sql-scripts username-for-the-db db-host db-name db-password* and check the output.
  ```bash
  ./src/mysql_updatetables.py mysql-scripts root localhost ecs test
  ```
* check what is the version of the versionTable
  ```bash
  mysql -h 127.0.0.1 -u root --password=test ecs -e "select version from versionTable;"
  ```
* set version value to '0'
  ```bash
  mysql -h 127.0.0.1 -u root --password=test ecs -e 'update versionTable SET version='0';'
  ```

### HOW TO RUN WITH DOCKER ###
Docker container was build from version 3 of the script

* Run mysql server with docker
```bash
docker run --name ecs-mysql -e MYSQL_DATABASE=ecs -e MYSQL_ROOT_PASSWORD=test -p 3306:3306 mysql:5.7
```
* Make sure versionTable exists in ecs database in docker container
```bash
docker run -i mysql:5.7 mysql -h 172.17.0.1 -u root --password=test ecs < initdb.sql
```
* run the script with docker
```bash
docker run -v $(pwd)/mysql-scripts:/mysql-scripts kskrisss/mysql_updatetables -f /mysql-scripts -u root --host 172.17.0.1 -p test -d ecs
```
* check what is the version of the versionTable
```bash
docker run -ti mysql:5.7 mysql -h 172.17.0.1 -u root --password=test ecs -e "select version from versionTable;"
```
* set version value to '0' wit docker
```bash
docker run -ti mysql:5.7 mysql -h 172.17.0.1 -u root --password=test ecs -e 'update versionTable SET version='0';'
```

### OTHER VERSIONS ###

- *./src/mysql_updatetables.py* - python2.7 as requested
- *./src/mysql_updatetables_v2.py* - python2.7 with argparse
- *./src/mysql_updatetables_v3.py* - python3 with argparse and fstring


