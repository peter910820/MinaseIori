import requests,json

def spider(data,eventOptions):
    url = requests.get(data[-1])
    text = ""
    content = json.loads(url.text)
    text += f"{eventOptions[1]}\n開始時間:{eventOptions[2]}\n結束時間:{eventOptions[3]}\n"
    text += "======================\n"
    text += f"{data[0]}  (名次/分數/半小時增加量)\n"
    for record in content:
        gap = record['data'][-1]['score']-record['data'][-2]['score']
        text += f"{record['rank']}位  {record['data'][-1]['score']}  pt(+{gap})\n"
    text += "======================"
    return text

def preprocessing(options,eventOptions):
    if options == "pt":
        array = []
        parmeter = "eventPoint"
        titleParmeter = "PT榜線"
        url = f"https://api.matsurihi.me/mltd/v1/events/{eventOptions[0]}/rankings/logs/{parmeter}/1,2,3,100,2500,5000,10000,25000,50000,100000?prettyPrint=true"
        array.append(titleParmeter)
        array.append(url)
        return array
    elif options == "hs":
        array = []
        parmeter = "highScore"
        titleParmeter = "高分榜線"
        url = f"https://api.matsurihi.me/mltd/v1/events/{eventOptions[0]}/rankings/logs/{parmeter}/1,2,3,100,2000,5000,10000,20000,100000?prettyPrint=true"
        array.append(titleParmeter)
        array.append(url)
        return array
    elif options == "lp":
        array = []
        parmeter = "loungePoint"
        titleParmeter = "寮榜線"
        url = f"https://api.matsurihi.me/mltd/v1/events/{eventOptions[0]}/rankings/logs/{parmeter}/1,2,3,10,100,250,500,1000?prettyPrint=true"
        array.append(titleParmeter)
        array.append(url)
        return array

def singlePreprocessing(options,eventOptions):
    if options[0:2] == "pt":
        array = []
        parmeter = "eventPoint"
        titleParmeter = "PT榜線"
        url = f"https://api.matsurihi.me/mltd/v1/events/{eventOptions[0]}/rankings/logs/{parmeter}/{options[3:]}?prettyPrint=true"
        array.append(titleParmeter)
        array.append(url)
        return array
    elif options[0:2] == "hs":
        array = []
        parmeter = "highScore"
        titleParmeter = "高分榜線"
        url = f"https://api.matsurihi.me/mltd/v1/events/{eventOptions[0]}/rankings/logs/{parmeter}/{options[3:]}?prettyPrint=true"
        array.append(titleParmeter)
        array.append(url)
        return array
    elif options[0:2] == "lp":
        array = []
        parmeter = "loungePoint"
        titleParmeter = "寮榜線"
        url = f"https://api.matsurihi.me/mltd/v1/events/{eventOptions[0]}/rankings/logs/{parmeter}/{options[3:]}?prettyPrint=true"
        array.append(titleParmeter)
        array.append(url)
        return array

def event_data():
    eventData = []
    mainUrl = requests.get("https://api.matsurihi.me/mltd/v1/events")
    eventContent = json.loads(mainUrl.text)
    id = eventContent[-1]['id']
    name = eventContent[-1]['name']
    beginDate = eventContent[-1]['schedule']['beginDate']
    endDate = eventContent[-1]['schedule']['endDate']
    eventData.append(id)
    eventData.append(name)
    eventData.append(beginDate)
    eventData.append(endDate)
    return eventData