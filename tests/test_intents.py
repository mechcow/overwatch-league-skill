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
        
if __name__ == '__main__':
    unittest.main()