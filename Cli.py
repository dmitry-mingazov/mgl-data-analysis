import os
from Action import Action, ActionFactory
from filters import get_filter_action_group

ESCAPE_CHAR = 'q'
RESET_CHAR = 'r'

class Cli:

    def __init__(self, groups):
        self.groups = groups
        self.chains = []
        self.grouped_chains = {}

    def set_chains(self, chains):
        self.chains = chains

    def set_grouped_chains(self, grouped_chains):
        self.grouped_chains = grouped_chains

    def print_error(self, msg):
        print(f"ERROR: {msg}")

    def print_info(self, msg):
        print(msg)

    def wait_for_input(self):
        input("Press Enter to continue . . .")

    def __print_header(self):
        self.__clear_screen()
        print("---------------------------------------------")
        print(f"Chains: {len(self.chains)}")
        if self.grouped_chains:
            print(f"Grouped chains: {len(self.grouped_chains)}")
        else:
            print("Grouped chains: --- no groups created yet ---")
        print("---------------------------------------------")

    def select_group(self):
        while True:
            self.__print_header()
            self.__print_groups()
            user_input = input("Choice: ")
            group = [g for g in self.groups if g.input_char == user_input][:1]
            if group:
                return group[0]
            if user_input == ESCAPE_CHAR:
                return None

    def select_action(self, group):
        while True:
            self.__print_header()
            self.__print_actions(group)
            user_input = input("Choice: ")
            _id = group._id + str(user_input)
            action = [a for a in group.actions if a._id == _id][:1]
            if action:
                return action[0]

    def __get_arg_input(self, name, arg_type, default_value=None):
        if default_value:
            value = input(f"Insert @{name} value ({default_value}): ")
            if not value:
                value = default_value
        else:
            value = input(f"Insert @{name} value: ")
        if arg_type == "int":
            return int(value)
        else:
            return value

    def input_action_args(self, action):
        self.__print_header()
        self.__print_action(action)
        args = []
        args_meta = action.meta_args
        for arg_meta in args_meta:
            name = arg_meta[0]
            arg_type = arg_meta[1]
            default_value = None
            if len(arg_meta) > 2:
                default_value = arg_meta[2]
            arg = self.__get_arg_input(name, arg_type, default_value)
            args.append(arg)
        self.__clear_screen()
        action.set_args(args)

    def __print_groups(self):
        for group in self.groups:
            print(f"{group.input_char}) {group.desc}")
        print("----------------------------")

    def __print_action(self, action):
        print(f"{action._id[3:]}) {action.desc}")

    def __print_actions(self, group):
        for action in group.actions:
            self.__print_action(action)
        print("----------------------------")

    def __clear_screen(self):
        if os.name == 'nt':
            os.system("cls")
        else:
            os.system("clear")

