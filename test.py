import requests,json

url = requests.get('https://api.matsurihi.me/mltd/v1/events/251/rankings/logs/highScore/1,2,3,100,2000,5000,10000,20000,100000?prettyPrint=true')
content = json.loads(url.text)
text = ""
content = json.loads(url.text)
text += "======================\n"
for record in content:
    gap = record['data'][-1]['score']-record['data'][-2]['score']
    text += f"{record['rank']}位{record['data'][-1]['score']}pt(+{gap})\n"
text += "======================"

print(text)