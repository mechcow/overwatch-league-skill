import unittest
from pathlib import Path
import sys
sys.path.append(str(Path("lambda/py")))
sys.path.append(str(Path("../lambda/py/")))
from ask_sdk_core.handler_input import HandlerInput
import request_handler
from olapi.OWLSchedule import OWLSchedule

class TestIntents(unittest.TestCase):
    def setUp(self):
        pass

    def test_GetNextMatchIntent(self):
        owl_schedule = OWLSchedule(str(Path('tests/mock_responses/schedule.json').absolute()))
        intent_handler = request_handler.GetNextMatchIntentHandler(owl_schedule)
        response = intent_handler.handle(HandlerInput(request_envelope=None))
        self.assertIn("Atlanta Reign",response.output_speech.ssml)
        self.assertIn("Hangzhou Spark",response.output_speech.ssml)


if __name__ == '__main__':
    unittest.main()