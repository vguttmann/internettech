"""
last change: 24.06.2024
author: Vincent Guttmann

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
general_intent_data: dict = json.loads(open('generals.json').read())
answer_data: dict = json.loads(open('answers.json').read())
controller_data: dict = json.loads(open('mcus.json').read())
weight_data: dict = json.loads(open('weight.json').read())


# generator for the questions
def generate_question():
  for question in question_data.keys():
    yield question


class BotSession:
  """
  class representing a session of the bot
  """

  sid: int  # session id of the session
  intent: str  # state in which the bot currently is
  last: str  # last state the bot was in
  question: str  # current question that is asked
  knowledge: dict  # storage of the already answered questions
  evaluation: list  # storage of evaluated data

  def __init__(self) -> None:
    """
    initialization of the variables
    """

    self.sid = next(_sid_iterator)
    self.intent = "greet"
    self.last = "greet"
    self.question_iterator = generate_question()
    self.question = next(self.question_iterator)
    self.knowledge = {}
    self.evaluation = []

  @staticmethod
  def greet() -> str:
    """
    returns first chat message
    """

    return general_intent_data['greeting']["action"]

  def generate_answer(self, text: str) -> str:
    """
    state action automatically for answer generation
    """

    text = text.lower()
    match self.intent:
      # first state which introduces the conversation
      case "greet":
        self.last = self.intent

        # check if user would like to know more about the bot
        if self.check_for_general_intent(text) == "capabilities":
          self.intent = "capabilities"
          return general_intent_data["capabilities"]["action"]

        # otherwise, enter into the "asking" state
        self.intent = "asking"
        return question_data[self.question]["question"]

      # asking intent which is the main part of the bot
      case "asking":
        self.last = self.intent

        # check for general actions (update, exit, info, restart)
        general = self.check_for_general_intent(text)
        if general:
          self.intent = general
          return general_intent_data[general]["action"]

        result = self.get_result(text)
        print(f'{self.sid}: {self.question} --> {result}')

        # answer with changing fallback if no result was achieved
        if not result:
          return random.choice(question_data[self.question]["fallback"])

        self.knowledge[self.question] = result

        try:
          self.question = next(self.question_iterator)
          return question_data[self.question]["question"]
        except StopIteration:
          self.intent = "evaluation"
          return self.generate_answer(text)

      # intent to change the last entry
      case "change":
        self.last = self.intent

        # if change was confirmed change to last question
        if self.is_affirmative(text):
          # reset question_iterator
          self.question_iterator = generate_question()
          for _ in range([str(x) for x in question_data.keys()].index(self.question) - 1):
            next(self.question_iterator)

          # update state and return question to change
          self.intent = "asking"
          self.question = next(self.question_iterator)

          return question_data[self.question]["question"]

        # return question fallback because answer has been falsy categorized
        return question_data[self.question]["fallback"]

      # return capability info and then go back to last intent
      case "capabilities":
        if self.check_for_general_intent(text) == self.intent:
          return general_intent_data["capabilities"]["fallback"]

        # go back to last intent
        self.intent = self.last
        self.last = "capabilities"

        return self.generate_answer(text)

      # computes state which computes start end exit sequence
      case "start" | "exit":
        self.last = self.intent

        # sequence when action was confirmed
        if self.is_affirmative(text):
          if self.intent == "start":
            # reset intent and question_iterator
            self.intent = "asking"
            self.question_iterator = generate_question()
            self.question = next(self.question_iterator)
            return question_data[self.question]["question"]

          # provide evaluation sequence
          self.intent = "evaluation"
          return self.generate_answer(text)

        # otherwise return to previous question fallback
        self.intent = "asking"
        return question_data[self.question]["fallback"]

      # evaluation state where the result is provided
      case "evaluation":
        self.last = self.intent
        self.intent = "finished"
        return self.generate_advice()

      # last state where no questions are asked
      case "finished":
        self.last = self.intent

        # check for general requests
        general = self.check_for_general_intent(text)

        if general:
          self.intent = general
          return general_intent_data[general]["action"]

        # else return finished message
        return general_intent_data["finish"]["action"]

    # default return if the state machine should fail
    return f"session {self.sid} received message: {text}"

  def check_for_general_intent(self, text: str) -> str:
    """
    function that determines if a general request was made
    """

    maximum_weight = 0
    intent = ""

    # count maximum keyword occurrence for all generals in the text
    for general_intent_key in general_intent_data.keys():
      current_weight = 0

      # loops over all keyword of a general request
      for keyword in general_intent_data[general_intent_key]["keywords"]:
        if keyword in text:
          current_weight += 1

      # determines if current occurrence is the highest
      if current_weight > maximum_weight:
        maximum_weight = current_weight
        intent = general_intent_key

    # returns the general request or an empty string by default
    return intent

  def get_result(self, answer: str):
    """
    computes the result to a question from the given input
    """

    question = question_data[self.question]
    results = []
    max_keyword_count = 0

    # If the question requires a numerical answer
    if not question["result"]:
      result = ""

      # just consider digits and punctuation
      for char in answer:
        if char.isdigit() or char == "." or char == ",":
          result += char

      # only return the numerical amount
      result = result.split(",")[0].split(".")[0]
      if result == "":
        return False  # or false if no result could be found
      else:
        return result

    # other results are nominal and computed from now on
    for word in list(question["result"].keys()):
      spotted_keyword_count = 0

      # iterate over all answer values and count the spotted keywords
      for spot in question["result"][word]:
        if spot in answer:
          spotted_keyword_count += 1

      # save all results with the highest keyword count
      if spotted_keyword_count > max_keyword_count:
        max_keyword_count = spotted_keyword_count
        results = [word]
      elif spotted_keyword_count == max_keyword_count:
        results.append(word)

    # check for normal and negative results
    if not self.is_negative(answer) or results[0] == "none" or results[0] == "no":  # not negative == normal
      # if the result is clear return it
      if len(results) == 1:
        return results[0]
      else:
        return False
    # handle negation
    else:
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

  def is_negative(self, text: str) -> bool:
    """
    check if the answer is negative
    """

    spotted_keyword_count = 0

    # counts negations
    for word in answer_data["negative"]:
      if word in text:
        spotted_keyword_count += text.count(word)

    # returns rather the text is negated or not
    return bool(spotted_keyword_count % 2)

  def is_affirmative(self, text: str) -> bool:
    """
    check if the answer is affirmative
    """
    affirmative = False

    # checks if a keyword is in the text
    for keyword in answer_data["positive"]:
      affirmative = affirmative or keyword in text

    # returns the confirmation with negation check
    return affirmative and not self.is_negative(text)

  def generate_advice(self):
    """
    function that creates the evaluation
    """

    self.evaluation = []
    max_score = sum(weight_data.values()) * 2  # calculates the highest possible score

    # adds the margin onto the budget if both are given
    try:
      self.knowledge["budget"] = int(self.knowledge["budget"]) + int(self.knowledge["margin"])
    except KeyError:
      pass

    # calculate score for all drones
    for name, data in controller_data.items():
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
      self.evaluation.append({
        "certainty": round(score / max_score * 100, 1),
        "name": name,
        "image_name": data["image"],
        "link": data["link"]
      })

    self.evaluation = sorted(self.evaluation, key=lambda k: k['certainty'], reverse=True)

    aboutText = controller_data[self.evaluation[0]["name"]]["text"]
    certainty = self.evaluation[0]["certainty"]

    return f"{aboutText} This result has been found with {certainty}% certainty. Congratulations! <a routerLink=\"/evaluation\">You can see more on the evaluation page.</a>"
