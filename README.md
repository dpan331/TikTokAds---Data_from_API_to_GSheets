# TikTok Ads---Data_from_API_to_GSheets
A python script (that can be hosted in Google Cloud Run Functions) which gets data from TikTok Ads API and pushes them to a Google Sheets. 
The data fetched correspond to an ecommerce business thus certain dimensions and metrics have been selected.

How it works.
>>> It makes an API Call to TikTok Ads retrieving specific data for the last 28 days (to account for the longest aopplicable attribution window in case you have selected such one).
>>> It pushes the data to a Google Sheet merging them with the older data with the key column being the date.
>>> It runs automatically on a daily basis.

How it is set up.
>>> Grab the script from my github repository.
>>> Go to TikTok for Business Developers and create an App (Give it all "Reporting" permissions as well as the "Report Pixel Event" permission from the "Measurement" scope. Now you got your Secret. 
>>> Go to Google Cloud Platform, create a new project, attach your credit card (don’t worry, you’ll spend a very low amount).
>>> Go to Cloud Run Functions (fyi soon this will be migrated to the Cloud Run UI).
>>> Create a Cloud Run Function (heads up - my script and function setup is a bit old, although still functionable, so you may want to trial and error a bit in order to adjust it to a more updated/fresh setup). My configuration is using a 1st gen function, Python 3.10, Memory allocated 256 MB, Timeout 300 seconds, Minimum instances 0, Maximum instances 32.
>>> Obviously replace all relevant placeholders (your API Secret, your Spreadsheet ID, your ad account ID in the API call),
>>> Deploy your function and voila!
Btw:
>>> Beware to give the right Roles (i.e. Cloud Functions Invoker) to the right Principals in the Permissions tab of the Function.
>>> Beware to share your Google Sheet with the Service account used in the Function.
>>> Beware of small details like the Spreadsheet ID you replace in the body of the script or the Google Sheet tab specified in the relevant row of the script or the Entry Point you specify in the Function to match the def of the script initiation.
>>> Before deploying the Function do not forget to include all three files (main.py, requirements.txt, keys.json) in the Source tab.
>>> Schedule it to run daily.

Cool tips.
>>> You can schedule the Function to run via Cloud Scheduler (however this may increase the costs, so perform first some calculations to estimate the amount). Or you can use the Apps Scripts attached to your Google Sheet in order to invoke the Function via URL (you can find the URL in the Trigger tab of the Function) and schedule this Apps Script to run daily (this scheduler is totally free).
>>> You can connect the Google Sheet to Looker Studio and create an even nicer report.
>>> You can add more dimensions and metrics to be fetched.
>>> You can push the data to Google Big Query so that you store the data more robustly and keep the whole setup inside GCP.
>>> You can combine this Function with Google Cloud Repositories so that you have version control in hand.
>>> You can make use of the Variables tab in your Function in order to leverage the Secrets Manager and securely store API keys, passwords, and other sensitive information.  
>>> If you have trouble with errors when running the script, take a look at the Logs tab of the Function in order to effectively debug your setup.
