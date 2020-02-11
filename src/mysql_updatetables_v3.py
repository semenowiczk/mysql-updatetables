#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

"""
A python script that UPGRADES DB with numbered SQL scripts stored
in a specified folder, named such as '045.createtable.sql'.
"""

import os
import argparse
import re
import pymysql

def parse_command_line_args():
    """ Command line argument """
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', '-f', required=True,
                        help='directory with sql scripts')
    parser.add_argument('--user', '-u', type=str, required=True,
                        help='username for the db')
    parser.add_argument('--host', '-c', type=str, required=True,
                        help='database host address')
    parser.add_argument('--database', '-d', type=str, required=True,
                        help='database name')
    parser.add_argument('--password', '-p', type=str, required=True,
                        help='database password')
    return vars(parser.parse_args())

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
        f"update ecs.versionTable SET ecs.versionTable.version='{version}' "
        f"where ecs.versionTable.version ='{lastversion}';")
    connection.commit()
    print(f"VersionTable updated. Current version is now: {version}")

def main():
    """ Do the work """
    args = parse_command_line_args()
    connection = pymysql.connect(host=args['host'],
                                 user=args['user'],
                                 passwd=args['password'],
                                 db=args['database'])

    directory = os.listdir(args['dir'])
    directory.sort(key=lambda x: int(''.join(filter(str.isdigit, x))))
    for file in directory:
        lastversion = int(sql_version(connection))
        version = int(get_version_filename(file))
        fullpath = os.path.join(args['dir'], file)
        if version > lastversion:
            print(f"running {fullpath} script")
            run_sql_file(fullpath, connection, version, lastversion)
        else:
            print(f"{fullpath} script will not be executed")

    connection.close()

if __name__ == "__main__":
    main()
