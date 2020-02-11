#!/usr/bin/env python2.7
# -*- encoding: utf-8 -*-

"""
A python script that UPGRADES DB with numbered SQL scripts stored
in a specified folder, named such as '045.createtable.sql'.
"""

import os
import sys
import re
import pymysql

def sql_version(connection):
    """ Checks the last version in database """
    cursor = connection.cursor()
    cursor.execute("SELECT ecs.versionTable.version FROM ecs.versionTable;")
    for ver in cursor.fetchone():
        version = ver
    cursor.close()
    return version

def get_version_filename(filename):
    """ Checks the version of SQL file """
    return re.search(r'\d+', filename).group(0)

def run_sql_file(filename, connection, version, lastversion):
    """ Applyes SQL file content """
    cursor = connection.cursor()
    for line in open(filename):
        cursor.execute(line)
    connection.commit()
    cursor.execute(
        "update ecs.versionTable SET ecs.versionTable.version='{}' "
        "where ecs.versionTable.version ='{}';".format(version, lastversion))
    connection.commit()
    print("VersionTable updated. Current version is now: {}".format(version))

def main():
    """ Do the work """
    connection = pymysql.connect(host=sys.argv[3],
                                 user=sys.argv[2],
                                 passwd=sys.argv[5],
                                 db=sys.argv[4])

    directory = os.listdir(sys.argv[1])
    directory.sort(key=lambda f: int(filter(str.isdigit, f)))
    for file in directory:
        lastversion = int(sql_version(connection))
        version = int(get_version_filename(file))
        fullpath = os.path.join(sys.argv[1], file)
        if version > lastversion:
            print("running {} script".format(fullpath))
            run_sql_file(fullpath, connection, version, lastversion)
        else:
            print("{} script will not be executed".format(fullpath))

    connection.close()

if __name__ == "__main__":
    main()
