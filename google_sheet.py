import gspread # pip install gspread
import sys

class GoogleSheet:
    # Get Google Sheet Object/Client
    def worksheet(self, sheet_id, sheet_title):    
        try:    
            gc = gspread.service_account(filename='cred_gs.json')
            sh = gc.open_by_key(sheet_id)
            worksheet = sh.worksheet(sheet_title)
            return worksheet
        except Exception as error:
            print("ERROR WHILE CREATING WORKSHEET CLIENT! ", error)
            sys.exit()
            
    # Get All Record From Google Sheet
    def get(self, worksheet):
        try:
            # Skip Columns Names
            records = worksheet.get_all_records()
            return records
        except Exception as error:
            print("ERROR WHILE RETREIVING RECORD FROM GOOGLE SHEET! ", error)
            sys.exit()

    # Check New Record Exist in Google Sheet
    def isExist(self, worksheet, new_data):
        try:
            url_exist = False
            googleSheet_data = self.get(worksheet)

            for row in googleSheet_data:
                if row["Job URL"] == new_data["Job URL"]:
                    url_exist = True

            if url_exist:
                return True
            else:
                return False
        
        except Exception as error:
            print("ERROR WHILE CHECKING NEW RECORD EXIST!", error)
            sys.exit()

    # Add Record to Google Sheet
    def add(self, worksheet, new_data):
        try:
            worksheet.append_row(new_data)
            print("\nSUCCESSFULLY ADDED NEW RECORD: ", new_data[0])
        except Exception as error:
            print("ERROR WHILE ADDING NEW RECORD!", error)
            sys.exit()