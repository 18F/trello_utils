#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys
import pprint

## API Reference: https://pythonhosted.org/trello/trello.html
##      Advanced: https://developers.trello.com/advanced-reference/
##        Python: https://pythonhosted.org/trello/
#  Trello API Info: https://trello.com/app-key
from trello import TrelloApi
# Get an AUTH_TOKEN Example: https://pythonhosted.org/trello/examples.html
#                          : To get an AUTH_TOKEN use "get_auth_token()"
# Help: http://www.trello.org/help.html

def del_all_cards(trello, board_id):
    for card in trello.boards.get_card(board_id):
        trello.cards.delete( card['id'] )

def get_auth_token(trello):
    print "Call this URL in your browser and write down the code in env.json"
    print trello.get_token_url('trello_utils', expires='never', write_access=True)

def move_all_cards(trello, board_id, from_name, to_name):
    print "Moving all cards from <%s> to <%s>" % (from_name, to_name)

    board_lists = trello.boards.get_list( board_id )

    from_list = filter(lambda l: l['name'] == from_name, board_lists)[0]
    to_list = filter(lambda l: l['name'] == to_name, board_lists)[0]

    print "\tFrom:", from_list['name'], from_list['id']
    print "\tTo:", to_list['name'], to_list['id']
    print

    list_cards = trello.lists.get(from_list['id'], cards="all")['cards']
    for c in list_cards:
        print "Moving:", c['name'], c['id']
        trello.cards.update_idList(c['id'], to_list['id']

def setup_trello():
    with open('env.json') as env:
        config = json.load(env)

    trello = TrelloApi( config['TRELLO_APP_KEY'] )
    trello.set_token( config['TRELLO_AUTH_TOKEN'] )

    return config, trello

if __name__ == "__main__":
    config, trello = setup_trello()

    from_name = sys.argv[1]
    to_name = sys.argv[2]

    # Auth Manual Step Required: Call the URL printed by below via your browser, while logged in
    #trello = TrelloApi( config["TRELLO_APP_KEY"] )
    #get_auth_token(trello)

    move_all_cards(trello, config['BOARD_ID'], from_name, to_name)
