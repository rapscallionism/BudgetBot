class Grocery:

    name: str = ""
    amount: int = 1

    def __init__(self, name: str, amount: int = 1):
        self.name = name
        self.amount = amount

    def format_to_markdown_string(self):
        """
            Formats to markdown friendly string 
        """
        return f"- {self.name} ({self.amount})\n"