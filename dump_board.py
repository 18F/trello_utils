#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys
import click
import yaml

## API Reference: https://pythonhosted.org/trello/trello.html
##      Advanced: https://developers.trello.com/advanced-reference/
##        Python: https://pythonhosted.org/trello/
#  Trello API Info: https://trello.com/app-key
from trello import TrelloApi
# Get an AUTH_TOKEN Example: https://pythonhosted.org/trello/examples.html
#                          : To get an AUTH_TOKEN use "get_auth_token()"
# Help: http://www.trello.org/help.html

def setup_trello():
    with open('env.json') as env:
        config = json.load(env)

    trello = TrelloApi( config['TRELLO_APP_KEY'] )
    trello.set_token( config['TRELLO_AUTH_TOKEN'] )

    return config, trello

@click.group()
def cli():
    pass

def dump_list_cards(in_list):
    list_cards = trello.lists.get(in_list['id'], cards="all")['cards']

    for c in list_cards:

        print "\t* ###", c['name'].encode('utf8'), "###"
        if c['desc']: 
            print "\t--------------------------"
            print "\t", c['desc'].encode('utf8')
            print "\t--------------------------"

        text = []
        actions = trello.cards.get_field("actions", c['id'])
        for a in actions:
           if a.get('data', {}).get('text', None):
               text.append(a['data']['text'].encode('utf8'))
        if text:
            print "\t`"
            print "\t", "\n".join(text)
            print "\t`"

@cli.command()
def dump_board():
    board_lists = trello.boards.get_list( config['BOARD_ID'] )

    for l in board_lists:
        print "##", l['name'].encode('utf8')
        dump_list_cards(l)

config, trello = setup_trello()
if __name__ == "__main__":
    cli()
