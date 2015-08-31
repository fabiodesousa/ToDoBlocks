import trello
from slacker import Slacker
import datetime
import dateutil.parser
import pytz

# API keys:
trello_key = '704e6c320a6b289a96d1da11cf209e3a' # trello key
trello_token = 'bee447a36ea702188f84761692ed14d66954931b6df13268e870ebe8250f9e58' # trello token
slack_key = 'xoxp-2366742675-2366742677-9704170688-5d6984' # slack key
# trello things
trello_board_id = 'BjUnAzlo' #'Main' board
trello = trello.TrelloApi(trello_key, token=trello_token)

# function to post daily tasks to Slack
# takes list of tuples (task_string, task_time)
def slackPost(task_list):
  # Slack setup
  slack_channel = '@fabio'# Slack channel or message "#channel_name" or "@message_recipient"
  slack_bot_name = 'ToDoBot'# name of Slack bot (string)
  # create a Slack object
  slack = Slacker(slack_key)
  #print header
  slack.chat.post_message(slack_channel, 'Here are your tasks for today!', username=slack_bot_name)
  for task in task_list:
    slack.chat.post_message(slack_channel, format(task), username=slack_bot_name)

# function to format a list [task_string, task_time]
# ex: 00:00 AM/PM - Title of Task
def format(task):
  task_string = task[0]
  task_time = task[1]
  time_string = task_time.strftime('%I:%M %p')
  return time_string + ' -- ' + task_string

# borrowed function to round time to the nearest minute
def roundTime(dt_aware, dateDelta=datetime.timedelta(minutes=1)):
  """Round a datetime object to a multiple of a timedelta
  dt : datetime.datetime object, default now.
  dateDelta : timedelta object, we round to a multiple of this, default 1 minute.
  Author: Thierry Husson 2012 - Use it as you want but don't blame me.
          Stijn Nevens 2014 - Changed to use only datetime objects as variables
          Fabio DeSousa 2016 - Screwed with it a bunch
  """
  #make  naive
  dt = dt_aware.replace(tzinfo=None)
  #
  roundTo = dateDelta.total_seconds()
  #
  seconds = (dt - dt.min).seconds
  # // is a floor division, not a comment on following line:
  rounding = (seconds+roundTo/2) // roundTo * roundTo
  return dt + datetime.timedelta(0,rounding-seconds,-dt.microsecond)

# function for converting utc to local time zone
def convertTimeZoneFromUTC(timestampValue):
  # calculate time difference
  offset = datetime.datetime.now() - datetime.datetime.utcnow()
  # add offset to UTC time and return it
  return timestampValue + offset

# function to parse Trello dates
# takes a trello 'Due' string (UTC)
# returns a localized datetime object
def trelloDateParse(due):
  due_utc = dateutil.parser.parse(due)
  return convertTimeZoneFromUTC(due_utc)

# function to see if dates match
def isDueToday(due):
  # if None, return false:
  if due is None:
    return False
  else:
    # get today
    today = pytz.utc.localize(datetime.datetime.today()).date()
    # parse due
    due_local = trelloDateParse(due)
    # if today and due match, return True
    # else return False
    if due_local.date() == today:
      return True
    else:
      return False

# function that returns a list with all of the lists from Trello
def getTrelloLists(trello_board_id):
  lists = trello.boards.get_list(trello_board_id)
  lists_list = []
  for item in lists:
    lists_list.append(item)
  return lists_list

# function that returns a list with all of the cards on the board
def getTrelloCards(trello_board_id):
  cards = trello.boards.get_card(trello_board_id)
  card_list = []
  for card in cards:
    card_list.append(card)
  return card_list

# function that returns a list with all of the cards that are due today
def getCardsDueToday(cards):
  due_today = []
  for card in cards:
    # check if 'date' of card is today. If so, add it.
    if isDueToday(card['due']):
      due_today.append(card)
  return due_today

# function that returns dictionary of list names by ID
def getListNamesAndIds(lists):
  lists_dict = {}
  for item in lists:
    lists_dict[item['name']] = item['id']
  return lists_dict

# function that sets a card's list id to Today
def setCardListToday(card, lists_dict):
  # get listID of Today
  today_list_id = lists_dict['Today']
  trello.cards.update_idList(card['id'], today_list_id)

# function that archives cards in the "Done" list
def archiveDoneCards(lists_dict):
  # for every card in the Done board
  for card in trello.lists.get_card(lists_dict['Done']):
    # archive the card
    trello.cards.update_closed(card['id'], 'true')

# main

# instantiate slack_queue
slack_queue = []

# get lists_dict
lists_dict = getListNamesAndIds(getTrelloLists(trello_board_id))
# get all cards
cards = getTrelloCards(trello_board_id)
# archive cards that are in 'Done'
archiveDoneCards(lists_dict)

# AT SOME POINT:
# Change functions so that you do one loop and everything happens then?
# This would make it O(n)?

# for every card due today
for card in getCardsDueToday(cards):
  # set that card's list to Today
  setCardListToday(card, lists_dict)
  # send card name and due (rounded) to slack_queue
  slack_queue.append([card['name'], roundTime(trelloDateParse(card['due']))])

# post to Slack!
slackPost(slack_queue)


