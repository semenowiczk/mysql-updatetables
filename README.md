The following use case might be a real-life example from one of our customers, please deliver your best possible solution. 

 

Please go through the described scenario and write a script, in one of the below languages, implementing a fix to the issue below. 

 

For the development of the scripts you have 4 hours and are allowed to use Google and any other material as long as the work submitted was written by you. 

 

Use Case: 

 

·   A database upgrade requires the execution of numbered SQL scripts stored in a specified folder, named such as '045.createtable.sql'

        - The scripts may contain any simple SQL statement(s) to any table of your choice, e.g. 'INSERT INTO testTable VALUES("045.createtable.sql");'

 

·   There may be gaps in the SQL file name numbering and there isn't always a . (dot) after the beginning number

 

·   The database upgrade is based on looking up the current version in the database and comparing this number to the numbers in the script names

        - The table where the current db version is stored is called 'versionTable', with a single row for the version, called 'version'

 

·   If the version number from the db matches the highest number from the scripts then nothing is executed

 

·   All scripts that contain a number higher than the current db version will be executed against the database in numerical order

 

·   In addition, the database version table is updated after the script execution with the executed script's number 

 

·   Your script will be executed automatically via a program, and must satisfy these command line input parameters exactly in order to run:

        - './your-script.your-lang directory-with-sql-scripts username-for-the-db db-host db-name db-password'

  

 

Requirements:

 

·   Supported Languages: Bash, Python2.7, PHP, Shell, Ruby, Powershell - No other languages will be accepted

 

·   You will have to use a MySQL 5.7 database

    

 

How would you implement this in order to create an automated solution to the above requirements? 

