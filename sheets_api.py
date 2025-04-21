import os.path
import pickle
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def api_call(
    spreadsheet_id="1AI2EqC73Z87U1Y47Fl068xvQnQXsZ85Yll3G7UKa1ps", range="General!A:B"
):
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            creds = service_account.Credentials.from_service_account_file(
                "credentials.json"
            )
            creds = creds.with_scopes(["https://www.googleapis.com/auth/spreadsheets"])
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    try:
        service = build("sheets", "v4", credentials=creds)

        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range).execute()
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
