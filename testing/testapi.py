#!/usr/bin/env python

import sys
import requests
import simplejson as json
import pprint

baseurl = 'http://api.overwatchleague.com'
endpoints = {
    'TeamsRequest': '/teams',
    #'TeamsV2Request': '/v2/teams', putting this here for reference
    'TeamByIdRequest': '/team/{}',
    'TeamByIdV2Request': '/v2/team/{}',
    'ScheduleRequest': '/schedule',
    'MatchByIdRequest': '/match/{}',
    'RankingsRequest': '/ranking'
}

r = requests.get(baseurl+endpoints['ScheduleRequest'])
if r.status_code != 200:
    print ("Error getting request from server")
    sys.exit(1)

d = json.loads(r.content)
with open('schedule-sample.json','w') as f:
    json.dump(d,f)