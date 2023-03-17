from app import app, db, User
from app.settings import change_settings, console_interface, reset_to_template
from app.website_processing import new_admin, remove_admin


class Console:

    consoles_count = 0

    temp_instruction = """
    Commands:

    help - see commands
    start - turn on website
    change <settings name> <settings new content> - change settings
    reset - reset settings to recommended
    settings - watch all settings and their current content
    clear - clear website console

    """

    temp_title = f"""
--------- Website Console ---------
    { temp_instruction }
-----------------------------------
    """

    temp_interact_symbols = ">>> "

    def __init__(self, title: str = None, instruction: str = None, interact_symbols: str = None) -> None:
        self.id = self.new_console()
        self.title = title or self.temp_title
        self.instruction= instruction or self.temp_instruction
        self.interact_symbols = interact_symbols or self.temp_interact_symbols
        self.last_strings = []
        self.running = False

    def __str__(self) -> str:
        return f"Website console №{self.id}"

    @classmethod
    def new_console(cls) -> int:
        cls.consoles_count += 1
        return cls.consoles_count

    def update_last_strings(self, strings: str) -> None:
        self.last_strings.extend(strings.split("\n"))

    def dispatcher(self, command: str) -> str:
            self.update_last_strings(">>> " + command.strip())
            command.lower()
            if "change" in command:
                command_content = command.split()
                for obj in command_content:
                    if obj == "":
                        command_content.remove(obj)
                if len(command_content) != 3:
                    answer = "Invalid change command - write change command like this:\nchange <settings name> <settings new content>"
                else:
                    answer = change_settings(command_content[1], command_content[2])
            elif "unpromote" in command:
                 with app.app_context():
                    command_content = command.split()
                    for obj in command_content:
                        if obj == "":
                            command_content.remove(obj)
                    if len(command_content) != 2:
                        answer = "Invalid unpromote command - write this command like this:\nunpromote <username>"
                    else:
                        answer = remove_admin(db, User, command_content[1])
            elif "promote" in command:
                with app.app_context():
                    command_content = command.split()
                    for obj in command_content:
                        if obj == "":
                            command_content.remove(obj)
                    if len(command_content) != 2:
                        answer = "Invalid promote command - write this command like this:\npromote <username>"
                    else:
                        answer = new_admin(db, User, command_content[1])
            elif "clear" in command:
                answer = "Console was cleared"
                self.last_strings = []
            elif "help" in command:
                answer = self.instruction
            elif "settings" in command:
                answer = console_interface()
            elif "reset" in command:
                reset_to_template()
                answer = "Settings reseted to recommended"
            elif "start" in command:
                if self.running:
                    self.running = False
                    answer = "Starting website..."
                else:
                    answer = "Command allowed only on server console."
            else:
                answer = "Invalid command. To see commands write \"help\""
            self.update_last_strings(answer)
            return answer

    def run(self) -> None:
        print(self.title)
        self.update_last_strings(self.title)
        self.running = True
        while self.running:
            command = input(self.interact_symbols)
            print(self.dispatcher(command))
