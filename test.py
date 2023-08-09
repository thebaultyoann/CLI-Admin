import datetime

def convert_string_to_date(date):
    try:
        year, month, day = date.split('/')
        new_date = datetime.date(int(year), int(month), int(day))
        return new_date
    except (ValueError, AttributeError):
        return
    except:
        return
    
print(convert_string_to_date("2023/05/08"))
print(datetime.date(int("2023"),int("05"),int("08")))