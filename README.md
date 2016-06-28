# trello_utils

misc cli tools for trello functionality

This project utilizes the trello python library to streamline some trello actions:
    * **move_all_cards** from one list within a board to another

Currently, this will only function on a pre_defined (see below) board.

**NOTE IT WILL NOT FUNCTION AS IS**

In order to successfully execute, please:
    * create an env.json file

```
{
    "TRELLO_APP_KEY": "1",
    "TRELLO_AUTH_TOKEN": "2",
    "BOARD_ID": "3"
}
```

Complete the `env.json` file by:
# Add your application key from: https://trello.com/app-key
# Creating an AUTH_TOKEN through something similar to:
```
    # Auth Manual Step Required: Call the URL printed by below via your browser, while logged in
    #trello = TrelloApi( config["TRELLO_APP_KEY"] )
    #get_auth_token(trello)
```
# Grab the board id by navigating to your board and adding `.json` to the URL

Note: `env.json` is set in the `.gitignore` file.
