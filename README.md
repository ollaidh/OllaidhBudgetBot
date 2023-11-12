# BUDGET BOT

This is a simple budget-tracking bot for Discord.
Database is run on Google Cloud - Firestore database.
You send a message to the bot with the purchase information
(name, price, category), bot adds it to database. 
Bot can return you simple statistics like money spent for certain period,
product category, piechart of spent money etc.

## To start working
???? Command line parameters (user, currency etc.)????

## Wake up the bot
Go to `https://ollaidhbudbot.ew.r.appspot.com`

#TODO: check how it would be changed if bot is run on other's GCloud
#TODO: now there is only collection "months" for my budget.How would it work if we add other users? Create a new collection for username? What about security?

## Commands:
`!help` - 

`!buy` - 

`!del` - 

`!spent`- 

`!chart` - 

`!version` - 


## Purchase

### Purchase parameters:
Each purchase has the following parameters:

`name` - name of purchase *(steak, coffee, vegetables, books etc.)*

`price` - price in chosen currency *(30.5, 1230, 3.4 etc.)*

`category` - category of the purchase *(food, transport, utilities etc.)*
It is strongly recommended to stick to limited number of categories,
otherwise statistics would be less representative. But it's always up to the user.

All purchase parameters are defined by the user.
There is a limited number of pre-defined categories:

category *'meat'* : *'steak', 'pork', 'chicken', 'liver', 'bacon', 'meat'*

category *'takeaway'* : *'coffee', 'pasrty', 'breakfast', 'lunch', 'dinner', 'takeaway'*

category *'utilities'* : *'electricity', 'water', 'internet'*

category *'sweets'* : *'cookies', 'chocolate', 'sweets'*

category *'vegetables'* : *'potatoes', 'green', 'avocado', 'vegetables'*

category *'dairy'* : *'milk', 'yogurt', 'cheese', 'dairy'*

If you do not define category while adding a purchase, it will be 
automatically defined for purchases with pre-defined categories.
For purchases without pre-defined category the category will automatically be
defined as *'uncategorized'*

`date` - date making the purchase

### Add purchase:
Send message with purchase information:

`!buy %purchase_name% %price% %category%`

example:

`!buy coffee 2.5 takeaway`

Date of purchase is automatically detected as date of sending the message.

### Delete purchase

Only last purchase can be deleted by sending a message to bot:

`!del`

## Get statistics
Spent money statistics can be provided for parameters set by user.
Parameters are:

`Period of time` can come in three formats:

- %start month% %end month% - for period of time from start month to end month including both
- %month% - for provided month
- no period - if no period provided, statistics come for current month

`Category of products`
If no category is provided, the total spent amount + spent for each category will be shown

Examples:

`!spent 2023-02 2023-05 takeaway`
![Alt text](pics/spent1.png?raw=true "Title")

### Get pie chart

## Tests

## Dependencies

## Environmental variables

## Repo structure

## Prerequisites
- Python 3.10

