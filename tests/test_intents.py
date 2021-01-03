import unittest
from pathlib import Path
import sys
sys.path.append(str(Path("lambda/py")))
sys.path.append(str(Path("../lambda/py/")))
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.intent_request import IntentRequest
from ask_sdk_model import RequestEnvelope
import request_handler
from olapi.OWLSchedule import OWLSchedule
from olapi.OWLStanding import OWLStanding
from olapi.OWLTeam import OWLTeam
from freezegun import freeze_time
from unittest import mock

class TestIntents(unittest.TestCase):
    def setUp(self):
        pass

    @freeze_time("2019-09-11")
    def test_GetNextMatchIntentTomorrow(self):
        owl_schedule = OWLSchedule(str(Path('tests/mock_responses/schedule.json').absolute()))
        intent_handler = request_handler.GetNextMatchIntentHandler(owl_schedule)
        response = intent_handler.handle(HandlerInput(request_envelope=None))
        self.assertIn("Atlanta Reign",response.output_speech.ssml)
        self.assertIn("Hangzhou Spark",response.output_speech.ssml)
        self.assertIn("tomorrow",response.output_speech.ssml)
        self.assertIn("at 11PM",response.output_speech.ssml)

    @freeze_time("2019-09-12")
    def test_GetNextMatchIntentToday(self):
        owl_schedule = OWLSchedule(str(Path('tests/mock_responses/schedule.json').absolute()))
        intent_handler = request_handler.GetNextMatchIntentHandler(owl_schedule)
        response = intent_handler.handle(HandlerInput(request_envelope=None))
        self.assertIn("Atlanta Reign",response.output_speech.ssml)
        self.assertIn("Hangzhou Spark",response.output_speech.ssml)
        self.assertIn("today",response.output_speech.ssml)
        self.assertIn("at 11PM",response.output_speech.ssml)

    @freeze_time("2019-09-10")
    def test_GetNextMatchIntentOnThursday(self):
        owl_schedule = OWLSchedule(str(Path('tests/mock_responses/schedule.json').absolute()))
        intent_handler = request_handler.GetNextMatchIntentHandler(owl_schedule)
        response = intent_handler.handle(HandlerInput(request_envelope=None))
        self.assertIn("Atlanta Reign",response.output_speech.ssml)
        self.assertIn("Hangzhou Spark",response.output_speech.ssml)
        self.assertIn("on Thursday",response.output_speech.ssml)
        self.assertIn("at 11PM",response.output_speech.ssml)

    @freeze_time("2019-09-10")
    def test_getNextTeamMatchIntent(self):
        owl_schedule = OWLSchedule(str(Path('tests/mock_responses/schedule.json').absolute()))
        intent_handler = request_handler.GetNextTeamMatchIntentHandler(owl_schedule)
        request_envelope = mock.MagicMock(spec=RequestEnvelope)
        request_envelope.request = mock.MagicMock(spec=IntentRequest)
        request_envelope.request.intent = mock.MagicMock()
        request_envelope.request.intent.slots = dict()
        request_envelope.request.intent.slots['teamName'] = mock.MagicMock()
        request_envelope.request.intent.slots['teamName'].value = "Atlanta Reign"
        response = intent_handler.handle(HandlerInput(request_envelope=request_envelope))
        self.assertIn("Atlanta Reign",response.output_speech.ssml)
        self.assertIn("Hangzhou Spark",response.output_speech.ssml)
        self.assertIn("on Thursday",response.output_speech.ssml)
        self.assertIn("at 11PM",response.output_speech.ssml)

    @freeze_time("2020-01-03")
    def test_getCurrentStandingsIntent(self):
        owl_standing = OWLStanding(str(Path('tests/mock_responses/standings.json').absolute()))
        intent_handler = request_handler.GetStandingsIntentHandler(owl_standing)
        request_envelope = mock.MagicMock(spec=RequestEnvelope)
        request_envelope.request = mock.MagicMock(spec=IntentRequest)
        request_envelope.request.intent = mock.MagicMock()
        request_envelope.request.intent.slots = dict()
        request_envelope.request.intent.slots['numRankings'] = mock.MagicMock()
        request_envelope.request.intent.slots['numRankings'].value = 3
        response = intent_handler.handle(HandlerInput(request_envelope=request_envelope))
        self.assertIn("The top 3 teams are", response.output_speech.ssml)
        self.assertIn("Vancouver Titans", response.output_speech.ssml)
        self.assertIn("San Francisco Shock", response.output_speech.ssml)
        self.assertIn("New York Excelsior", response.output_speech.ssml)

    @freeze_time("2021-01-03")
    def test_getTeamRecordIntent(self):
        owl_team = OWLTeam(teamId=4523, datafile=str(Path('tests/mock_responses/4523.json').absolute()))
        intent_handler = request_handler.GetTeamRecordIntentHandler(owl_team)
        request_envelope = mock.MagicMock(spec=RequestEnvelope)
        request_envelope.request = mock.MagicMock(spec=IntentRequest)
        request_envelope.request.intent = mock.MagicMock()
        request_envelope.request.intent.slots = dict()
        request_envelope.request.intent.slots['teamName'] = mock.MagicMock()
        request_envelope.request.intent.slots['teamName'].value = "Dallas Fuel"
        request_envelope.request.intent.slots['teamName'].resolution.values[0].id = 4523
        response = intent_handler.handle(HandlerInput(request_envelope=request_envelope))
        self.assertIn("Dallas Fuel", response.output_speech.ssml)
        self.assertIn("10 wins", response.output_speech.ssml)
        self.assertIn("18 losses", response.output_speech.ssml)
        self.assertIn("0 draws", response.output_speech.ssml)
        
        

        
if __name__ == '__main__':
    unittest.main()