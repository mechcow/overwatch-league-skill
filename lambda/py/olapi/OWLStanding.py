import datetime
from dateutil import parser
import simplejson as json
from olapi.OverwatchLeagueAPIHelper import OverwatchLeagueAPIHelper

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class OWLStanding:
    def __init__(self, datafile=None):
        self.schedule_data = None

        if datafile:
            with open(datafile, 'r') as f:
                self.standing_data = json.loads(f.read())
        else:
            owapi = OverwatchLeagueAPIHelper()
            self.standing_data = owapi.makeRequest('StandingsRequest')

    def getCurrentStandings(self,numResults: int=3) -> list:
        """ Get current OWL Rankings a number of teams (default 3)"""
        standings = self.standing_data.get('ranks').get('content')
        res = list()
        for i in range(numResults):
            res.append(standings.get(str(i)))
        return res