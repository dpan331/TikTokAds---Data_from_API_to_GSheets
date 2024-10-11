def hello_tiktok(request):

  import requests
  import json
  import pandas as pd
  from googleapiclient.discovery import build
  from google.oauth2 import service_account
  from datetime import date, timedelta

  # Define the last 28 days dates and keep them in a list
  datesRemove = []
  for i in range(1,29):
    dayBack = date.today() - timedelta(days=i)
    datesRemove.append(dayBack.strftime("%Y-%m-%d"))
  dayYesterday = date.today() - timedelta(days=1)


  ######## TIKTOK API CALL, RESPONSE & TRANSFORMATION #########

  url = "https://business-api.tiktok.com/open_api/v1.3/report/integrated/get/?advertiser_id=XXXXXXXXXXXXXXXXXXX&data_level=AUCTION_CAMPAIGN&report_type=BASIC&dimensions=[\"stat_time_day\",\"campaign_id\"]&metrics=[\"campaign_name\",\"objective_type\",\"spend\",\"impressions\",\"clicks\",\"total_pageview\",\"product_details_page_browse\",\"web_event_add_to_cart\",\"complete_payment\",\"total_complete_payment_rate\",\"profile_visits\",\"likes\",\"comments\",\"shares\",\"follows\",\"conversion\"]&start_date=" + dayBack.strftime("%Y-%m-%d") + "&end_date=" + dayYesterday.strftime("%Y-%m-%d") + "&page_size=60"

  payload={}
  headers = {
    'Access-Token': 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
  }

  response = requests.request("GET", url, headers=headers, data=payload)

  # Parse the API response
  json_obj = json.loads(response.text)
  df = pd.json_normalize(json_obj['data']['list'])

  df.rename(columns = {'dimensions.stat_time_day':'date'}, inplace = True)
  df['date'] = df['date'].map(lambda x: x.replace(" 00:00:00",""))
  df.sort_values(by='date',ascending=True, inplace = True)
  df.rename(columns = {'dimensions.campaign_id':'campaign_id'}, inplace = True)
  df.rename(columns = {'metrics.campaign_name':'campaign_name'}, inplace = True)
  df.rename(columns = {'metrics.objective_type':'objective_type'}, inplace = True)
  df.rename(columns = {'metrics.spend':'cost'}, inplace = True)
  df.rename(columns = {'metrics.impressions':'impressions'}, inplace = True)
  df.rename(columns = {'metrics.clicks':'clicks'}, inplace = True)
  df.rename(columns = {'metrics.conversion':'conversion'}, inplace = True)
  df.rename(columns = {'metrics.profile_visits':'profile_visits'}, inplace = True)
  df.rename(columns = {'metrics.follows':'paid_followers'}, inplace = True)
  df.rename(columns = {'metrics.likes':'paid_likes'}, inplace = True)
  df.rename(columns = {'metrics.comments':'paid_comments'}, inplace = True)
  df.rename(columns = {'metrics.shares':'paid_shares'}, inplace = True)
  df.rename(columns = {'metrics.complete_payment':'complete_payment'}, inplace = True)
  df.rename(columns = {'metrics.total_complete_payment_rate':'total_complete_payment_rate'}, inplace = True)
  df.rename(columns = {'metrics.total_pageview':'total_pageview'}, inplace = True)
  df.rename(columns = {'metrics.product_details_page_browse':'product_details_page_browse'}, inplace = True)
  df.rename(columns = {'metrics.web_event_add_to_cart':'web_event_add_to_cart'}, inplace = True)
  df.drop(df.columns[1],axis = 1)
  df = df[df['campaign_name'].str.contains('CW_')]
  df = df[df['impressions']!="0"]


  # Create an empty list
  row_list = []

  # Iterate over each row
  for index, rows in df.iterrows():
      # Create list for the current row
      my_list = [rows.date, rows.campaign_id, rows.campaign_name, rows.objective_type,
                rows.cost, rows.impressions,
                rows.clicks, rows.conversion, rows.paid_followers,
                rows.paid_likes, rows.paid_comments, rows.paid_shares,
                rows.profile_visits, rows.complete_payment, rows.total_complete_payment_rate,
                rows.total_pageview, rows.product_details_page_browse, rows.web_event_add_to_cart]

      # append the list to the final list
      row_list.append(my_list)



  ######## GOOGLE SHEETS API CALL, RESPONSE & TRANSFORMATION #########

  # Make sure to provide read & write permissions
  SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
  SERVICE_ACCOUNT_FILE = 'keys.json'

  # Service account authentication. Make sure to share Editor access
  # in the GSheet with the service account email which is located in GCP
  creds = None
  creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)


  # The ID and range of the spreadsheet.
  SPREADSHEET_ID = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
  READ_RANGE_NAME = 'log!A1:R'


  service = build('sheets', 'v4', credentials=creds)

  # Call the Sheets API to read all data in the "log" tab
  sheet = service.spreadsheets()
  result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                              range=READ_RANGE_NAME).execute()
  values = result.get('values', [])

  # Search for the row numbers that correspond to the last 28 days
  ls = []
  n = 1
  for i in values:
    for days in datesRemove:
      if days in i:
        ls.append(n)
    n = n + 1


  # Clear the rows that correspond to the last 28 days
  clearRange = "log!A" + str(ls[0]) + ":R" + str(ls[-1])
  request = sheet.values().clear(spreadsheetId=SPREADSHEET_ID,range=clearRange).execute()


  # Append rows with last 28 days data (fetched from TikTok API)
  request = sheet.values().append(spreadsheetId=SPREADSHEET_ID,
                                  range="log!A1:R",
                                  valueInputOption="USER_ENTERED",
                                  insertDataOption="INSERT_ROWS",
                                  body={"values":row_list}).execute()
  return 'null'
