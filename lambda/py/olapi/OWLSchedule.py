import datetime
from dateutil import parser
import simplejson as json
from olapi.OverwatchLeagueAPIHelper import OverwatchLeagueAPIHelper

class OWLSchedule: 
    def __init__(self,datafile=None):
        self.schedule_data = None

        if datafile:
            with open(datafile,'r') as f:
                self.schedule_data = json.loads(f.read())
        else:
            owapi = OverwatchLeagueAPIHelper()
            self.schedule_data = owapi.makeRequest('ScheduleRequest')            

    def getNextMatch(self):
        stages = self.schedule_data['data']['stages']
        for stage in stages: 
            for match in stage['matches']:
                if match['state'] != 'CONCLUDED':
                    return match
    
    def convertDatetime(self,datestring):
        return parser.parse(datestring)