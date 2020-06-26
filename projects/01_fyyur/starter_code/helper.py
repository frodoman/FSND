from datetime import datetime
import dateutil.parser
import babel

def arrayToString(stringlist): 
    if len(stringlist) == 0:
        return ""

    result = ""
    for oneString in stringlist: 
        result += (oneString + ",")

    return result

def stringToArray(stringValue):
    if stringValue is None or len(stringValue) == 0:
        return [""]

    if "," in stringValue:
        return stringValue.split(",")
    else:
        return [stringValue]

def format_datetime(stringValue, format='medium'):
  date = dateutil.parser.parse(stringValue)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

def dateTimeToString(dateTime):
    format="%a %-d %b %Y 'at' %H:%M"
    return dateTime.strftime(format)