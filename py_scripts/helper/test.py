from datetime import datetime

datetime_object = datetime.strptime('10/16/14', ' %-m/%-d/%Y')

print(datetime_object)