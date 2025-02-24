# BudgetBot
Discord Bot to help me calculate my expenses for the month

## TODO LIST 
- Register the test bot for testing into the server
- Code up the implementations of the data additions + removals
- DB connection onto local
    - For now, settle with CSV option
- Stretch goal: Dockerize and figure out how to get it to run in ephemeral env.
- Stretch goal: Shopping List Report
    - Generate a baseline/checkpoint for how much money the allocated budget will be 
        - Call Amazon API? Walmart API? Determine by the user? 
            - Have to figure out API Price plans at that point
    - Workflow:
        - Grab the user's shopping list
        - Loop through and make a call to any of the APIs listed above
            - Tally up total after making each call and getting the prices
        - Return back a price result