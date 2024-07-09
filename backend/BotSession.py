"""
last change: 24.06.2024
author: Tjorven Burdorf

description: logic of the chatbot
"""
import json
import random


# generator for the unique session ids
def _sid_generator():
    sid = 0
    while True:
        sid += 1
        yield sid


# iterator of the session ids
_sid_iterator = _sid_generator()

# store json data
question_data: dict = json.loads(open('questions.json').read())
general_data: dict = json.loads(open('generals.json').read())
answer_data: dict = json.loads(open('answers.json').read())
drone_data: dict = json.loads(open('drones.json').read())
weight_data: dict = json.loads(open('weight.json').read())


# generator for the questions
def _question_generator():
    for question in question_data.keys():
        yield question


# class representing a session of the bot
class BotSession:
    sid: int  # session id of the session
    state: str  # state in which the bot currently is
    last: str  # last state the bot was in
    question: str  # current question that is asked
    knowledge: dict  # storage of the already answered questions
    evaluation: list  # storage of evaluated data

    def __init__(self) -> None:
        # initialisation of the variables
        self.sid = next(_sid_iterator)
        self.state = "greet"
        self.last = "greet"
        self.question_iterator = _question_generator()
        self.question = next(self.question_iterator)
        self.knowledge = {}
        self.evaluation = []

    # returns first chat message
    @staticmethod
    def greet() -> str:
        return general_data['greeting']["action"]

    # state action automat for answer generation
    def generate_answer(self, text: str) -> str:
        text = text.lower()
        match self.state:
            # first state which introduces the conversation
            case "greet":
                self.last = self.state

                # just check for capability check
                if self._check_for_general(text) == "capabilities":
                    self.state = "capabilities"
                    return general_data["capabilities"]["action"]

                # else wise entering into the asking state
                self.state = "asking"
                return question_data[self.question]["question"]

            # asking state which is the main part of the bot
            case "asking":
                self.last = self.state

                # check for general actions in the answer (update, exit, info, restart)
                general = self._check_for_general(text)

                if general:
                    self.state = general
                    return general_data[general]["action"]

                # compute and log result from answer
                result = self._get_result(text)
                print(f'{self.sid}: {self.question} --> {result}')

                # answer with changing fallback if no result was achieved
                if not result:
                    return random.choice(question_data[self.question]["fallback"])

                # update knowledge storage
                self.knowledge[self.question] = result

                # continue with the next question or change to evaluation
                try:
                    self.question = next(self.question_iterator)
                except StopIteration:
                    self.state = "evaluation"
                    return general_data["recommendation"]["action"]

                # return next question
                return question_data[self.question]["question"]

            # state where the last entry can be changed
            case "change":
                self.last = self.state

                # if change was confirmed change to last question
                if self._confirmed(text):
                    # reset question_iterator
                    self.question_iterator = _question_generator()
                    for i in range([str(x) for x in question_data.keys()].index(self.question) - 1):
                        next(self.question_iterator)

                    # update state and return question to change
                    self.state = "asking"
                    self.question = next(self.question_iterator)
                    return question_data[self.question]["question"]

                # return question fallback because answer has been falsy categorized
                return question_data[self.question]["fallback"]

            # state which returns to normal after capability info
            case "capabilities":
                # give leading answer
                if self._check_for_general(text) == self.state:
                    return general_data["capabilities"]["fallback"]

                # go back to last state
                self.state = self.last
                self.last = "capabilities"
                return self.generate_answer(text)

            # computes state which computes start end exit sequence
            case "start" | "exit":
                self.last = self.state

                # sequence when action was confirmed
                if self._confirmed(text):
                    if self.state == "start":
                        # reset state system and question_iterator
                        self.state = "asking"
                        self.question_iterator = _question_generator()
                        self.question = next(self.question_iterator)
                        return question_data[self.question]["question"]

                    # provide evaluation sequence
                    self.state = "evaluation"
                    return general_data["recommendation"]["action"]

                # els wise return to previous question fallback
                self.state = "asking"
                return question_data[self.question]["fallback"]

            # evaluation state where the result is provided
            case "evaluation":
                self.last = self.state
                self.state = "finished"
                return self._create_advice()

            # last state where no questions are asked
            case "finished":
                self.last = self.state

                # check for general requests
                general = self._check_for_general(text)

                if general:
                    self.state = general
                    return general_data[general]["action"]

                # else return finished message
                return general_data["finish"]["action"]

        # default return if the state action machine should fail
        return f"session {self.sid} received message: {text}"

    # function that determines if a general request was made
    def _check_for_general(self, text: str) -> str:
        maximum = 0
        action = ""

        # count maximum keyword occurrence for all generals in the text
        for key in general_data.keys():
            current = 0

            # loops over all keyword of a general request
            for keyword in general_data[key]["keywords"]:
                if keyword in text:
                    current += 1

            # determines if current occurrence is the highest
            if current > maximum:
                maximum = current
                action = key

        # returns the general request or an empty string by default
        return action

    # computes the result to a question from the given input
    def _get_result(self, answer: str):
        question = question_data[self.question]
        results = []
        max_count = 0

        # catch the results with a relative scale
        if not question["result"]:
            result = ""

            # just consider digits and punctuation
            for char in answer:
                if char.isdigit() or char == "." or char == ",":
                    result += char

            # only return take the full amount
            result = result.split(",")[0].split(".")[0]
            if result == "":
                return False  # or false if no result could be found
            else:
                return result

        # other results are nominal and computed from now on
        for word in list(question["result"].keys()):
            spot_count = 0

            # iterate over all answer values and count the spotted keywords
            for spot in question["result"][word]:
                if spot in answer:
                    spot_count += 1

            # save all results with the highest keyword count
            if spot_count > max_count:
                max_count = spot_count
                results = [word]
            elif spot_count == max_count:
                results.append(word)

        # check for normal and negative results
        if not self._negated(answer) or results[0] == "none" or results[0] == "no":  # not negated -> normal

            # if the result is clear return it
            if len(results) == 1:
                return results[0]
            else:
                return False

        else:  # handle negation

            # generate the normal answer list (-> difference to the negated one)
            new_results = list(question["result"].keys())
            for result in results:
                new_results.remove(result)

            # decide over output
            if len(new_results) == 1:
                return new_results[0]  # return new clear result

            # return negative result if it is in the new options
            elif "none" in new_results:
                return "none"
            elif "no" in new_results:
                return "no"

            # else wise return the typical fallback return value
            else:
                return False

                # checks how often a text is negated

    def _negated(self, text: str) -> bool:
        spot_count = 0

        # counts negations
        for word in answer_data["negative"]:
            if word in text:
                spot_count += text.count(word)

        # returns rather the text is negated or not
        return bool(spot_count % 2)

    # check if the answer is confirmative
    def _confirmed(self, text: str) -> bool:
        confirm = False

        # checks if a keyword is in the text
        for keyword in answer_data["positive"]:
            confirm = confirm or keyword in text

        # returns the confirmation with negation check
        return confirm and not self._negated(text)

    # function that creates the evaluation
    def _create_advice(self):
        self.evaluation = []
        max_score = sum(weight_data.values()) * 2  # calculates the highest possible score

        # adds the margin onto the budget if both are given
        try:
            self.knowledge["budget"] = int(self.knowledge["budget"]) + int(self.knowledge["margin"])
        except KeyError:
            pass

        # calculate score for all drones
        for name, data in drone_data.items():
            score = max_score / 2  # default score

            # iterate over all criteria of the drone
            for key, val in data["characteristic"].items():

                # ignore criteria that are not given
                if key not in self.knowledge.keys():
                    continue

                # distinguish nominal and relative criteria
                if key == "budget":

                    # add or subtract point depending on accordance
                    if int(self.knowledge[key]) >= val:
                        score += weight_data[key]
                    else:
                        score -= weight_data[key]
                else:
                    # same for nominal values
                    if self.knowledge[key] == val:
                        score += weight_data[key]
                    else:
                        score -= weight_data[key]

            # append calculated data to the evaluation storage
            self.evaluation.append([round(score / max_score * 100, 1), name, data["image"], data["link"]])

        # sort the evaluation
        self.evaluation.sort()
        self.evaluation.reverse()

        # create the evaluation text and return it
        text = (drone_data[self.evaluation[0][1]]["text"]
                + f"This result has been found with {self.evaluation[0][0]}% certainty. Congratulations!")
        return text
