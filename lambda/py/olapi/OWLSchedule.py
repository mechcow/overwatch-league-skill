import datetime
from dateutil import parser
import simplejson as json
from olapi.OverwatchLeagueAPIHelper import OverwatchLeagueAPIHelper

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class OWLSchedule:
    def __init__(self, datafile=None):
        self.schedule_data = None

        if datafile:
            with open(datafile, 'r') as f:
                self.schedule_data = json.loads(f.read())
        else:
            owapi = OverwatchLeagueAPIHelper()
            self.schedule_data = owapi.makeRequest('ScheduleRequest')

    def _nextMatchHelper(self, team=None):
        stages = self.schedule_data['data']['stages']
        for stage in stages:
            for match in stage.get('matches', []):
                if match.get('state', '') != 'CONCLUDED':
                    if team == None:
                        return match
                    logger.info(match)
                    for competitor in match.get('competitors', []):
                        if competitor != None and competitor.get('name', '') == team:
                            return match
        return None

    def getNextMatch(self):
        return self._nextMatchHelper()

    def getNextTeamMatch(self, team):
        return self._nextMatchHelper(team)

    def convertDatetime(self, datestring):
        return parser.parse(datestring)
