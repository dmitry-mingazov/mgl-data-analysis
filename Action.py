class Action:
    """ 
        Action wraps a function in order to run it inside
        the cli
    """

    def __init__(self, _id, fn, desc, args, chain_type):
        self._id = _id
        self.fn = fn
        self.desc = desc
        self.meta_args = args
        self.chain_type = chain_type
        self.args = []

    def run(self, chains):
        if len(self.args) != len(self.meta_args):
            raise Exception("Action was not set properly: use set_args() to set function arguments")
        args = self.args
        # clean args
        self.args = []
        fn = self.fn
        return fn(chains, *args)

    def get_meta_args(self):
        return self.meta_args

    def set_args(self, args):
        self.args = args

    def is_grouped(self):
        if self.chain_type == "grouped":
            return True
        else:
            return False

class ActionGroup():
    def __init__(self, _id, actions, desc, input_char):
        self._id = _id
        self.actions = actions
        self.desc = desc
        self.input_char = input_char

class ActionFactory:
    @staticmethod
    def create_action(_id, action, chain_type):
        fn = action[0]
        args = action[1]
        desc = action[2]
        return Action(_id, fn, desc, args, chain_type)

    @staticmethod
    def create_actions_from_list(id_prefix, actions, gactions):
        action_objs = []
        for index, action in enumerate(actions):
            _id = id_prefix + str(index)
            action_objs.append(ActionFactory.create_action(_id, action, "chain"))
        actions_len = len(actions)
        for index, gaction in enumerate(gactions):
            _id = id_prefix + str(actions_len + index)
            action_objs.append(ActionFactory.create_action(_id, gaction, "grouped"))
        return action_objs

