# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
from datetime import datetime, timezone
from os.path import join

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
import ask_sdk_core.utils as ask_utils
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response
from ask_sdk_model.slu.entityresolution import StatusCode

from olapi.OWLSchedule import OWLSchedule
from olapi.OWLStanding import OWLStanding
from olapi.OWLTeam import OWLTeam
import data

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = data.WELCOME_TEXT

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class IntentHelper:
    @staticmethod
    def _format_human_time(time):
        # type: (HandlerInput) -> time
        if time.minute == 0:
            return time.strftime("%-I%p")
        else:
            return time.strftime("$-I%m%p")

    @staticmethod
    def _match_to_speech(match, match_time):
        now = datetime.now(timezone.utc)
        tdelta = match_time - now

        day_str = ""

        if tdelta.days == 0: #today
            day_str = "today"
        elif tdelta.days == 1: #tomorrow
            day_str = "tomorrow"
        elif tdelta.days > 1: 
            day_str = "on {}".format(match_time.strftime("%A"))
        else:
            day_str = "unknown"

        matchtime_speak_output = "{} at {}".format(day_str, IntentHelper._format_human_time(match_time) )

        speak_output = data.NEXT_MATCH.format(
            match['competitors'][0]['name'],
            match['competitors'][1]['name'],
            matchtime_speak_output
        )
        
        return speak_output
    
class GetNextMatchIntentHandler(AbstractRequestHandler):
    def __init__(self,owl_schedule = None):
        if owl_schedule:
            #testing uses this to overwrite the default
            self.owl_schedule = owl_schedule
        else:
            self.owl_schedule = None #lazy-load later

    """Handler for Schedule Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("GetNextMatchIntent")(handler_input)


    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In GetNextMatchIntentHandler.handle")

        if not self.owl_schedule:
            self.owl_schedule = OWLSchedule()

        match = self.owl_schedule.getNextMatch()
        match_time = self.owl_schedule.convertDatetime(match.get('startDate'))
        speak_output = IntentHelper._match_to_speech(match, match_time)
        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )

class GetNextTeamMatchIntentHandler(AbstractRequestHandler):
    def __init__(self,owl_schedule = None):
        if owl_schedule:
            #testing uses this to overwrite the default
            self.owl_schedule = owl_schedule
        else:
            self.owl_schedule = None #lazy-load later

    """Handler for Schedule Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("GetNextTeamMatchIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In GetNextTeamMatchIntentHandler.handle")

        slots = handler_input.request_envelope.request.intent.slots
        if 'teamName' not in slots:
            logger.error("teamName not in slots")
            return None
        
        team_name = slots['teamName'].value
        logger.info(team_name)

        if not self.owl_schedule:
            self.owl_schedule = OWLSchedule()

        match = self.owl_schedule.getNextTeamMatch(team_name)
        match_time = self.owl_schedule.convertDatetime(match.get('startDate'))
        speak_output = IntentHelper._match_to_speech(match, match_time)
        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )

class GetStandingsIntentHandler(AbstractRequestHandler):
    def __init__(self, owl_standings):
        if owl_standings:
            #testing uses this to overwrite the default
            self.owl_standings = owl_standings
        else:
            self.owl_standings = None #lazy-load later

    """Handler for Schedule Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("GetStandingsIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In GetNextTeamMatchIntentHandler.handle")

        numRankings = 3 # default
        slots = handler_input.request_envelope.request.intent.slots
        if 'numRankings' in slots:
            numRankings = slots.get('numRankings').value

        if not self.owl_standings:
            self.owl_standings = OWLStanding()

        standings = self.owl_standings.getCurrentStandings(numRankings)
        speak_output = [ "The top {:d} teams are: ".format(numRankings) ]

        for team in standings:
            speak_output.append("{:d}, {} - ".format(
                team.get('placement'),
                team.get('competitor').get('name')
                ))

        return (
            handler_input.response_builder
                .speak("".join(speak_output))
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )

class GetTeamRecordIntentHandler(AbstractRequestHandler):
    def __init__(self, owl_team = None):
        if owl_team:
            self.owl_team = owl_team
        else:
            self.owl_team = None

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> Response
        return ask_utils.is_intent_name("GetTeamRecordIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In GetTeamRecordIntentHandler.handle")

        slots = handler_input.request_envelope.request.intent.slots
        if 'teamName' not in slots:
            logger.error("teamName not in slots")
            return None

        team_name = slots.get('teamName').value
        teamId = None
        resolution = slots.get('teamName').resolutions.resolutions_per_authority[0]
        if resolution.status.code == StatusCode.ER_SUCCESS_MATCH:
            resolutionValues = resolution.values[0]
            teamId = resolutionValues.value.id
            
        logger.info("Got teamName: {} teamId: {}".format(team_name, teamId))

        if not self.owl_team:
            self.owl_team = OWLTeam(teamId=teamId)
        
        record = self.owl_team.getTeamRecord()
        speak_output = "{} have {:d} wins, {:d} losses and {:d} draws".format(
            self.owl_team.getTeamName(),
            record['matchWin'],
            record['matchLoss'],
            record['matchDraw']
        )
        
        return (
            handler_input.response_builder
                .speak("".join(speak_output))
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response

class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.

sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(GetNextMatchIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

handler = sb.lambda_handler()
