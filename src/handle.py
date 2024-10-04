import json, requests

class ApiV1:
    def __init__(self, pattern, is_single: bool) -> None:
        self.event_data = {}
        self.output_content = ""
        self.api_url = "https://api.matsurihi.me/mltd/v1/events"
        self.is_single = is_single
        self.pattern = pattern
        self.pattern_name = ""
        self.target_url = ""
        self.defalut_format = {"pt": "1,2,3,100,2500,5000,10000,25000,50000,100000", 
                               "hs": "1,2,3,100,2000,5000,10000,20000,100000", 
                               "lp": "1,2,3,10,100,250,500,1000"}

    def get_data(self):
        event = requests.get(self.api_url)
        data = json.loads(event.text)
        self.event_data["id"] = data[-1]['id']
        self.event_data["name"] = data[-1]['name']
        self.event_data["begin_date"] = data[-1]['schedule']['beginDate']
        self.event_data["end_date"] = data[-1]['schedule']['endDate']

        self.url_preprocessing(self)
        return self.crawler(self)
    
    def url_preprocessing(self):
        if self.is_single:
            ranker = self.pattern[2:]
            self.pattern = self.pattern[0:2]
        match self.pattern:
            case "pt":
                parmeter = "eventPoint"
                self.pattern_name =  "PT榜線"
            case "hs":
                parmeter = "highScore"
                self.pattern_name =  "高分榜線"
            case "lp":
                parmeter = "loungePoint"
                self.pattern_name =  "寮榜線"
        if self.is_single:
            self.target_url = f"https://api.matsurihi.me/mltd/v1/events/{self.event_data['id']}/rankings/logs/{parmeter}/{ranker}?prettyPrint=true"
        else:
            self.target_url = f"https://api.matsurihi.me/mltd/v1/events/{self.event_data['id']}/rankings/logs/{parmeter}/{self.defalut_format[self.pattern]}?prettyPrint=true"

    def crawler(self):
        #get record data
        target = requests.get(self.target_url)
        target_content = json.loads(target.text)
        #output process
        output_content += f"{self.event_data['name']}\n開始時間:{self.event_data['begin_date']}\n結束時間:{self.event_data['end_date']}\n"
        output_content += "(名次/分數/半小時增加量)\n"
        for ranker_record in target_content:
            gap = ranker_record['data'][-1]['score']-ranker_record['data'][-2]['score']
            output_content += f"{ranker_record['rank']}位  {ranker_record['data'][-1]['score']}  pt(+{gap})\n"
            
        return output_content