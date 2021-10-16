import json

def read_file(PATH:str):
        params = json.loads(open(PATH + ".json").read())
        new_dict={}
        for param in params:
            key = param['name']
            value = param['subtopics']
            new_dict[key] = value
        return new_dict[PATH]

class RoadmapSet:

    def _init_(self,PATH:str):
        self.org_roadmap=[]
        self.cur_roadmap=[]
        self.t = 0
        self.index = 0
        self.n = 0

    def set(self,PATH):
        self.org_roadmap=read_file(PATH)
        self.cur_roadmap=self.org_roadmap.copy()
        self.n = len(self.org_roadmap)

    def done(self,idx):
        self.cur_roadmap.remove(self.org_roadmap[idx - 1])
        self.n -= 1
    
    def next(self):
        if(self.index == self.n):
            return ""
        else:
            d = self.cur_roadmap[self.index]
            return "\n" + d.name + "\n You need to finsih in " + round(d.weight*self.t) + "hours. Here are the resourses \n" + d.resources + "\n"


    def list_all(self):
        reply = ""
        b = ""
        sr = 0
        for i in self.cur_roadmap:
            if i['tag'] != b:
                b=i['tag']
                reply += "\n" + b + '\n'
            sr = sr + 1
            reply += str(sr) + "." + i['name'] + "\n"
        return reply

    def Estimate_Time(self,days):
        total_w = 0
        for i in self.cur_roadmap:
            total_w += self.i.weight
        self.t = 8*days / total_w
        