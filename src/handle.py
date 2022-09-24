from asyncio.windows_events import NULL
import requests,json

def spider(options,eventOptions):
    if options == "pt":
        parmeter = "eventPoint"
        titleParmeter = "PT榜線"
        url = requests.get(f"https://api.matsurihi.me/mltd/v1/events/{eventOptions[0]}/rankings/logs/{parmeter}/1,2,3,100,2500,5000,10000,25000,50000,100000?prettyPrint=true")
    elif options == "hs":
        parmeter = "highScore"
        titleParmeter = "高分榜線"
        url = requests.get(f"https://api.matsurihi.me/mltd/v1/events/{eventOptions[0]}/rankings/logs/{parmeter}/1,2,3,100,2000,5000,10000,20000,100000?prettyPrint=true")
    elif options == "lp":  
        parmeter = "loungePoint"
        titleParmeter = "寮榜線"
        url = requests.get(f"https://api.matsurihi.me/mltd/v1/events/{eventOptions[0]}/rankings/logs/{parmeter}/1,2,3,10,100,250,500,1000?prettyPrint=true")
    else:
        return NULL

    text = ""
    content = json.loads(url.text)

    return 

def event_data():
    eventData = []
    url = requests.get("https://api.matsurihi.me/mltd/v1/events")
    eventContent = json.loads(url.text)
    id = eventContent[-1]['id']
    name = eventContent[-1]['name']
    beginDate = eventContent[-1]['schedule']['beginDate']
    endDate = eventContent[-1]['schedule']['endDate']
    eventData.append(id)
    eventData.append(name)
    eventData.append(beginDate)
    eventData.append(endDate)
    return eventData