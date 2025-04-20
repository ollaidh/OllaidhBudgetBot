# BUDGET BOT

This is a simple budget-tracking Discord bot written in Python
You send a message to the bot with the purchase information
(name, price, category), bot adds it to database. 
Bot can return you simple statistics like money spent for certain period,
product category, pie-chart of spent money etc.

Bot uses Google Cloud AppEngine and Firestore database.

## Example

![Alt text](pics/example.png?raw=true "Title")

## Commands

`!buy` - adds purchase to database. Example: `!buy coffee 4.5 takeaway`. 
First parameter is the name of the purchase, second parameter is its price,
third parameter is a purchase category. Category can be left empty, in this
case a predefined category will be set for this purchase or `uncategorized`
if there's no predefined category. 

Refer to `commands/command_buy` for the list of predefined categories.

Parameters can't contain spaces.

`!del` - Deletes the last purchase. Doesn't accept any parameters.

`!spent`- Shows statistics about amount of money spent. Example:
`!spent 2023-08 2023-12 takeaway` shows statistics from date 1 to date 2
(inclusive) for the given category. If you don't specify a category, it
will show you statistics across all categories: `!spent 2023-08 2023-12`.
You can set one month to show statistics within one month: `!spent 2023-08`.
Finally, you can just ask `!spent` for statistics on a current month across
all categories.

Note that date format should be `YYYY-MM`, no day is accepted.

`!chart` - Shows you a pie-chart statistics for a given request. Command
parameters are the same as in `!spent`.

`!version` - Shows you a current bot version

`!help` - Displays help

## For developers

Create and activate venv

Install requirements

### Local testing

For local testing you need to install `gcloud sdk` https://cloud.google.com/sdk/docs/install

Install firestore emulator https://cloud.google.com/firestore/docs/emulator

You might need to install JDK

Login into your account with `gcloud auth login` (optional?)

Run firestore emulator

```
gcloud emulators firestore start --host-port localhost:8090
```

Set environment variables:

`BUDBOT_PROJECT_ID` assign to your Google Cloud project ID

`FIRESTORE_EMULATOR_HOST` assign according to your firestore
emulator run command

Database emulator state is automatically cleaned up before
each test run, you don't need to restart emulator manually.

Run pytest tests

```
pytest .
```
launch.json for pytest example:
```
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Debug specific pytest file",
            "type": "debugpy",
            "request": "launch",
            "module": "pytest",
            "args": [
                "db_adapters/test_firestore_adapter.py"
            ],
            "justMyCode": true,
            "env": {
                "BUDBOT_PROJECT_ID": "ollaidhbudbot",
                "FIRESTORE_EMULATOR_HOST": "localhost:8090",
            }
        }
    ]
}
```

## Deploy

Use `deploy.py` script for deploying bot to your Discord.

Set the following environment variables:

`GOOGLE_APPLICATION_CREDENTIALS` pointing to a gcloud credentials
json file in bot folder. Don't commit this file! This repo is
configured to ignore files with the `cred-*.json` mask, so you
can name your cred files accordingly to avoid an accidental commit.

To get a credentials json file, go to App Engine, Service accounts,
choose an account, select Keys in a top menu, select Add key,
Create new key, select json and download this file.

`BUDBOT_PROJECT_ID` assign to your Google Cloud project ID

`DISCORD_BOT_TOKEN` your Discord bot token. For more info about
how to get a token refer to https://discord.com/developers/docs/topics/oauth2
