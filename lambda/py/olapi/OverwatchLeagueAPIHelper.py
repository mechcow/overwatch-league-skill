import requests
from olapi.exceptions import *
import simplejson as json

doc = """
Interact with the OWLeague API
"""

BASEURL = 'http://api.overwatchleague.com'
ENDPOINTS = {
    'TeamsRequest': '/teams',
    #'TeamsV2Request': '/v2/teams', putting this here for reference
    'TeamByIdRequest': '/team/{}',
    'TeamByIdV2Request': '/v2/team/{}',
    'ScheduleRequest': '/schedule',
    'MatchByIdRequest': '/match/{}',
    'RankingsRequest': '/ranking'
}

class OverwatchLeagueAPIHelper:
    def __init__(self):
        pass

    def makeRequest(self,endpoint):
        if endpoint not in ENDPOINTS:
            raise InvalidEndpointException("Couldn't find endpoint {}".format(endpoint))
        r = requests.get("{}{}".format(BASEURL,ENDPOINTS[endpoint]))
        if r.status_code != 200:
            raise APIException("Expected status code 200, got {}".format(r.status_code))
        d = json.loads(r.content)
        return d