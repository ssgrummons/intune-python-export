# Export Intune Data using Python
 This python app can be used to export Intune data using the Export API for data analysis purposes.  

## Overview
Microsoft has built the Intune Export API in order to better download large amounts of MDM data quickly.  This method is significantly faster and more efficient than paging though Graph; using this method I was able to download over 400,000 records in less than a minute.

I used Python due to the data analysis tools python supports, such as pandas, numpy and other machine learning tools.  

## Repository Structure

| File | Function |
| ----------- | ----------- |
| `app.py` | This is the main python app that performs the data export |
| `config.py` | Configuration File. This can be modified with the desired export query |
| `intune_graph.py` | Reusable modules for authenticating to and performing operations in Microsoft Graph |
| `requirements.txt` | Dependencies to be installed using `pip install -r requirements.txt` into your python environment|
| `.env_template` | Contains accounts and secrets used to connect.  Edit and save as `.env` in the same directory |
| `deploy/cron.yaml`| An example CronJob file to deploy this application in Kubernetes as a job |


## Export API Resources

Microsoft has [documentation on using the export API](https://docs.microsoft.com/en-us/mem/intune/fundamentals/reports-export-graph-apis).  There is thorough documentation on [how to create your export job request](https://docs.microsoft.com/en-us/mem/intune/fundamentals/reports-export-graph-available-reports) in Intune.