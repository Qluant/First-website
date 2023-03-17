from wtforms.validators import ValidationError


class Unique(object):
    """ My own validator that checks field uniqueness """
    def __init__(self, table, table_column,
                 message="Contain of this field must be unique, your information already busy."):
        self.table = table
        self.table_column = table_column
        self.message = message

    def __call__(self, form, field):
        is_busy = self.table.query.filter(self.table_column == field.data).first() if field else None
        if is_busy:
            raise ValidationError(self.message)


class AuthorizationName(object):
    """ My own validator that checks if there is a user in table with entered username """
    def __init__(self, table, username_column=None,
                 message="Wrong username. If you aren't registered, click on button \"Sign Up\"."):
        if not username_column:
            username_column = table.username
        self.table = table
        self.username_column = username_column
        self.message = message

    def __call__(self, form, field):
        username_existence = self.table.query.filter(self.username_column == field.data).first() if field else None
        if not username_existence:
            raise ValidationError(self.message)


class AuthorizationPassword(object):
    """ My own validator that checks matching of entered password to password in database """
    def __init__(self, table, username_column=None, password_column=None, message="Wrong password! Try again."):
        if not username_column:
            username_column = table.username
        if not password_column:
            password_column = table.password
        self.table = table
        self.username_column = username_column
        self.password_column = password_column
        self.message = message

    def __call__(self, form, field):
        username = form.username.data
        username_existence = self.table.query.filter(self.username_column == username).first() if field else None
        if username_existence:
            users = self.table.query.all()
            for user in users:
                if user.username == username:
                    if user.password != field.data:
                        raise ValidationError(self.message)
                    return None
