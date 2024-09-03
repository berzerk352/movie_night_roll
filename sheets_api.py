import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

def api_call(spreadsheet_id="1AI2EqC73Z87U1Y47Fl068xvQnQXsZ85Yll3G7UKa1ps", range="General!A:B"):
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    
    try:
        service = build("sheets", "v4", credentials = creds)

        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=spreadsheet_id, range=range)
            .execute()
        )
        values = result.get("values", [])

        if not values:
            print("No data found")
            return
        
        for row in values:
            if len(row) == 1:
                row.append("")
        return values

    except HttpError as err:
        print(err)

if __name__ == "__main__":
    movie_list = api_call()
    print(movie_list)