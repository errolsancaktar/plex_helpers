#!/usr/bin/python3
    
import sys
import getopt
import sqlite3
import logging
from datetime import datetime, timedelta


def main(argv):
  
    ##Defaults 
    plexfolder = '/mnt/plex_ramdisk/Databases/'
    backupfolder = '/mnt/plex_ramdisk/Backups/'
    plexdb = 'com.plexapp.plugins.library.db'
    verbose = False
    dryRun = True
    
    
    
    
    if(dryRun == True):
        print("Dry Run. No Database Actions Taken")
    try:
        opts, args = getopt.getopt(argv, "fdbhv", ["plexfolder=","plexdb=", "backupfolder="])
    except getopt.GetoptError:
        print('PlexDB Backup -f <db folder> -d <DB>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('PlexDB Backup -f <Plex Database Folder> -d <Database Filename> -b <Backup Folder> -v (Verbose Output)')
            sys.exit()
        elif opt in ("-f", "--plexfolder"):
            plexfolder = arg
        elif opt in ("-d", "--plexdbdb"):
            plexdb = arg
        elif opt in ("-b", "--backupfolder"):
            plexdb = arg
        elif opt in ("-v"):
            verbose = True
    print('Plex Folder: ', plexfolder)
    print('Plex Database: ', plexdb)
    print('Backup Folder: ', backupfolder)

    
    ## Get current date and time 
    today = datetime.datetime.now()
    date_time = today.strftime("%m%d%Y-%H:%M:%S") #Set string
    print("Date: ",date_time)
    
    
    def progress(status, remaining, total):
        print(f'Copied {total - remaining} of {total} pages...')
    
    try:
        if(dryRun == False):
            # existing DB
            sqliteCon = sqlite3.connect(plexfolder + plexdb)
            # copy into this DB
            backupCon = sqlite3.connect(backupfolder + plexdb + '.' + date_time + '.bak') 
            with backupCon:
                if(verbose == True):
                    sqliteCon.backup(backupCon, pages=3, progress=progress)
                else:
                    sqliteCon.backup(backupCon, pages=3)
        else:
            print("Debugging")
                    
        print("backup successful")
        
    except sqlite3.Error as error:
        print("Error while taking backup: ", error)
    finally:
        if(dryRun == False):
            if backupCon:
                backupCon.close()
                sqliteCon.close()
        
if __name__ == "__main__":
       main(sys.argv[1:])
