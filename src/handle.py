import json, requests

class ApiV1:
    def __init__(self, pattern, status) -> None:
        self.event_data = {}
        self.rank = []
        self.output_content = ""
        self.api_url = "https://api.matsurihi.me/mltd/v1/events"
        self.status = status
        self.pattern = pattern
        self.pattern_name = ""
        self.target_url = ""

    def get_data(self):
        event = requests.get(self.api_url)
        data = json.loads(event.text)
        self.event_data["id"] = data[-1]['id']
        self.event_data["name"] = data[-1]['name']
        self.event_data["begin_date"] = data[-1]['schedule']['beginDate']
        self.event_data["end_date"] = data[-1]['schedule']['endDate']

        self.url_preprocessing(self)
        self.crawler(self)
    
    def url_preprocessing(self):
        match self.pattern:
            case "pt":
                parmeter = "eventPoint"
                self.pattern_name =  "PT榜線"
                self.target_url = f"https://api.matsurihi.me/mltd/v1/events/{self.event_data["id"]}/rankings/logs/{parmeter}/1,2,3,100,2500,5000,10000,25000,50000,100000?prettyPrint=true"
            case "hs":
                parmeter = "highScore"
                self.pattern_name =  "高分榜線"
                self.target_url = f"https://api.matsurihi.me/mltd/v1/events/{self.event_data["id"]}/rankings/logs/{parmeter}/1,2,3,100,2000,5000,10000,20000,100000?prettyPrint=true"
            case "lp":
                parmeter = "loungePoint"
                self.pattern_name =  "寮榜線"
                self.target_url = f"https://api.matsurihi.me/mltd/v1/events/{self.event_data["id"]}/rankings/logs/{parmeter}/1,2,3,10,100,250,500,1000?prettyPrint=true"

    def crawler(self, data, eventOptions):
        target = requests.get(self.target_url)
        target_content = json.loads(target.text)
        output_content += f"{self.event_data['name']}\n開始時間:{self.event_data['begin_date']}\n結束時間:{self.event_data['end_date']}\n"
        output_content += f"{data[0]}  (名次/分數/半小時增加量)\n"
        for record in target_content:
            gap = record['data'][-1]['score']-record['data'][-2]['score']
            text += f"{record['rank']}位  {record['data'][-1]['score']}  pt(+{gap})\n"
            
        return output_content

# def singlePreprocessing(options,eventOptions):
#     if options[0:2] == "pt":
#         array = []
#         parmeter = "eventPoint"
#         titleParmeter = "PT榜線"
#         url = f"https://api.matsurihi.me/mltd/v1/events/{eventOptions[0]}/rankings/logs/{parmeter}/{options[3:]}?prettyPrint=true"
#         array.append(titleParmeter)
#         array.append(url)
#         return array
#     elif options[0:2] == "hs":
#         array = []
#         parmeter = "highScore"
#         titleParmeter = "高分榜線"
#         url = f"https://api.matsurihi.me/mltd/v1/events/{eventOptions[0]}/rankings/logs/{parmeter}/{options[3:]}?prettyPrint=true"
#         array.append(titleParmeter)
#         array.append(url)
#         return array
#     elif options[0:2] == "lp":
#         array = []
#         parmeter = "loungePoint"
#         titleParmeter = "寮榜線"
#         url = f"https://api.matsurihi.me/mltd/v1/events/{eventOptions[0]}/rankings/logs/{parmeter}/{options[3:]}?prettyPrint=true"
#         array.append(titleParmeter)
#         array.append(url)
#         return array