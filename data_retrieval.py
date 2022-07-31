from pyairtable import Api, Table
API_KEY = ""
BASE = "appB6hLip5pzTn9ps"
TABLE1 = "duty-personnel"

table = Table(API_KEY, BASE, 'blockout-dates')
print(table.all())
