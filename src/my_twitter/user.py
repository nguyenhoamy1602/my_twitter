class User(object):
    """ encapsulate the user as an object """

    def __init__(self, email, name):
        """ instantiate the class """
        self.key = None
        self.values = {}
        self._validate_args(**kwargs)
        self._set_key(kwargs[KEY_NAME])
        self._set_values()
