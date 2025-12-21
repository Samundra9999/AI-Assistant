import re
def clean_text(text):
    text= re.sub(r'\\','',text)
    text = text.replace('"', "  ")
    text = text.replace("∞",' ')
    text = re.sub(r'\s+', ' ', text).strip()
    return text