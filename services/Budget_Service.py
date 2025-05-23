
class Budget_Service:
    """
        Budget entry has the following columns:
        Category : string; classifies what the specific budget is for and acts as a pseudo-id
        Limit : int; identifies what the spending limit of this specific Budget entry is
        Spent : int; identifies how much money has been spent towards this category of budget
    """


    DIRECTORY: str = 'users-budget'

    def __init__(self):
        pass

    def get_all(self):
        pass

    def get(self, item_to_get: str):
        pass

    def create_budget(self, category: str, limit: int):
        """
            Creates a Budget Entry given a category and limit\n
            This will default the spend column to 0
        """
        # Should create budget category, budget limit according to an input, 
        # and initialize with a spent budget of 0 
        pass

    def edit_budget_limit(self, category: str, new_limit: int):
        """
            Given a category, 
        """
        pass

    def edit_budge(self, item_to_remove: str):
        pass
