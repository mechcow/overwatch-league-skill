import datetime
from dateutil import parser
import simplejson as json
from olapi.OverwatchLeagueAPIHelper import OverwatchLeagueAPIHelper

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class OWLTeam:
    def __init__(self, teamId=None, datafile=None):
        self.team_data = None

        if datafile:
            with open(datafile, 'r') as f:
                self.team_data = json.loads(f.read())
        else:
            owapi = OverwatchLeagueAPIHelper()
            if not teamId:
                logger.error('Require teamId for OWLTeam')
                return None
            self.team_data = owapi.makeRequest('TeamsByIdV2Request' % teamId)

    def getTeamRecord(self):
        return self.team_data['data']['records']

    def getTeamName(self):
        return self.team_data['data']['name']