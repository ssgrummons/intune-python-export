import intune_graph
import config
import pandas as pd
#import requests
#import uuid
from datetime import datetime, timedelta
from dateutil import tz

utc_zone = tz.tzutc()
local_zone = tz.tzlocal()

def currentTimeStr():
    runTime = datetime.now() 
    timestr = runTime.strftime('%Y-%m-%d %H:%M:%S')
    return timestr

def main():
    # Start the logging
    print(currentTimeStr() + ' - Starting Script')
    start = datetime.now()
    token = getToken()
    # This leverages the new Export Job API to download >400K records in bulk.
    response = createExportJob(token)
    response = checkExportJob(response, token)

    print(currentTimeStr() + ' - Writing Intune data to disk')

    # Downloads the report from blob storage to a .zip file and unzips the file.
    file_path = saveReport(response, config.download_dir)
    csv_path = unZipReport(file_path)

    print(currentTimeStr() + ' - Ingesting Intune data from CSV file')

    df = pd.read_csv(csv_path)

    ### Continue to manipulate the data in Pandas

if __name__ == "__main__":
    main()