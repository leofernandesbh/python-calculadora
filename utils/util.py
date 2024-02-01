import re

NUM_OR_DOT_REGEX = re.compile(r'^[0-9.]$')

def isNumOrDot(text: str):
  return bool(NUM_OR_DOT_REGEX.search(text)) 

def isEmpty(text: str):
  return len(text) == 0

def isValidNumber(text: str):
  formatedNumber = None
  
  if text.isdigit():
    formatedNumber = text.lstrip('0')    
  else:  
    try:
      float(text)
      formatedNumber = text
    except ValueError:
      return False, None
  
  if not formatedNumber is None:
    formatedNumber = text.lstrip('0')
    if formatedNumber == '':
      formatedNumber = '0'
    return True, formatedNumber

  return False, None

def formatNumber(text: str):
  if text.isdigit():
    return int(text)
  return float(text)