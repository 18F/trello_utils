#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys

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

def get_labels(trello, board_id):
    b = trello.boards.get( board_id )

    return b['labelNames']

def label_all_cards(trello, board_id, list_name, label_name):
    print "Tagging all cards in <%s> with <%s>" % (list_name, label_name)

    board_lists = trello.boards.get_list( board_id )

    in_list = filter(lambda l: l['name'] == list_name, board_lists)[0]

    print "\tIn:", in_list['name'], in_list['id']
    print

    list_cards = trello.lists.get(in_list['id'], cards="all")['cards']

    for c in list_cards:
        print "Tagging:", c['name'], c['id']
        try:
            trello.cards.new_label( c['id'], label_name ) #throws HTTP 400 if label already exists
        except:
            pass

def unlabel_all_cards(trello, board_id, list_name, label_name):
    print "Tagging all cards in <%s> with <%s>" % (list_name, label_name)

    board_lists = trello.boards.get_list( board_id )

    in_list = filter(lambda l: l['name'] == list_name, board_lists)[0]

    print "\tIn:", in_list['name'], in_list['id']
    print

    list_cards = trello.lists.get(in_list['id'], cards="all")['cards']

    for c in list_cards:
        print "Tagging:", c['name'], c['id']
        try:
            trello.cards.delete_label_color( label_name, c['id'] )
        except:
            pass

def setup_trello():
    with open('env.json') as env:
        config = json.load(env)

    trello = TrelloApi( config['TRELLO_APP_KEY'] )
    trello.set_token( config['TRELLO_AUTH_TOKEN'] )

    return config, trello

if __name__ == "__main__":
    config, trello = setup_trello()

    list_name = sys.argv[1]
    
    try:
        tag_color = sys.argv[2]
    except:
        print json.dumps( get_labels(trello, config['BOARD_ID'] ), indent=4, sort_keys=True)
        sys.exit(-1)

    # Auth Manual Step Required: Call the URL printed by below via your browser, while logged in
    #trello = TrelloApi( config["TRELLO_APP_KEY"] )
    #get_auth_token(trello)

    label_all_cards(trello, config['BOARD_ID'], list_name, tag_color)
    #unlabel_all_cards(trello, config['BOARD_ID'], list_name, tag_color)
