from bs4 import BeautifulSoup
import requests
import re
import xlwt

def writeExcel(x, keywords, sheet):
    keys = sorted(keywords)
    y = 1
    for word in keys:
        sheet.write(y, x, keywords[word])
        y+=1

def readFiles():
    wordlist = []
    urllist = []
    print("reading text files...")
    with open("keywords.txt") as f:
        for line in f:
            line = line.rstrip("\n").lower()
            wordlist.append(line)
    with open("urllist.txt") as f:
        for line in f:
            line = line.rstrip("\n")
            urllist.append(line)
    return wordlist, urllist

wordlist, urllist = readFiles()

wb = xlwt.Workbook()
sheet = wb.add_sheet("frequency_table")
y=1
for word in sorted(wordlist):
    sheet.write(y, 0, word)
    y+=1
x=1
for url in urllist:
    sheet.write(0, x, url)
    x+=1
count = 1
for url in urllist:
    print("reading url No.", count, "...")
    keywords = dict.fromkeys(wordlist, 0)
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36'}
    req = requests.get(url, headers=headers)
    html = req.text
    soup = BeautifulSoup(html, "html.parser")
    rawtext = soup.get_text()
    text = re.split(r'\W+', rawtext)
    for word in text:
        word = word.lower()
        if word in keywords:
            keywords[word] += 1
    writeExcel(count, keywords, sheet)
    count+=1
wb.save("frequency_table.xls")
print("All done! Output can be found in frequency_table.xls.")
