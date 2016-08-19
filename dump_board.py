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

    # http://click.pocoo.org/5/utils/#printing-to-stdout
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
@click.option('--name', default="board_dump.yaml", help="Filename to dump contents if not default")
def dump_board(name):
    #click.echo(click.format_filename(name))

    #test_file = click.open_file('test.txt', 'w')
    #with click.open_file(filename, 'w') as f:
    #        f.write('Hello World!\n')

    board_lists = trello.boards.get_list( config['BOARD_ID'] )

    for l in board_lists:
        print "##", l['name'].encode('utf8')
        dump_list_cards(l)

def abort_if_false(ctx, param, value):
    if not value: ctx.abort()

@cli.command()
@click.option('--erase', is_flag=True, default=False, callback=abort_if_false,
              expose_value=False, prompt="Are you sure you want to delete everything?")
def erase_board():
    click.echo("erasing the board")

config, trello = setup_trello()
if __name__ == "__main__":
    cli()
