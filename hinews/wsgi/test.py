"""Testing stuff."""

from peewee import DoesNotExist

from wsgilib import JSON

from his import ACCOUNT
from his.orm import Account

__all__ = ['ROUTES']


def get_account():
    """Returns the actual account ORM model's instance."""

    return Account.get(Account.id == ACCOUNT.id)


def get_test_left():

    return Account.get(Account.id == ACCOUNT)


def get_test_right():

    return Account.get(ACCOUNT == Account.id)


def test(arg):
    """Runs tests."""

    if arg == 'account':
        return str(dir(ACCOUNT)) + '\n\n' + str(dir(get_account()))
    elif arg == 'eq':
        account = get_account()
        return JSON({
            'account == ACCOUNT': account == ACCOUNT,
            'ACCOUNT == account': ACCOUNT == account,
            'ACCOUNT.id == account.id': ACCOUNT.id == account.id,
            'account.id == ACCOUNT.id': account.id == ACCOUNT.id})
    elif arg == 'get':
        try:
            account_left = get_test_left()
        except DoesNotExist:
            account_left = None
        else:
            account_left = account_left.to_dict()

        try:
            account_right = get_test_right()
        except DoesNotExist:
            account_right = None
        else:
            account_right = account_left.to_dict()

        return JSON({'left': account_left, 'right': account_right})
    elif arg == 'expr':
        expression = Account.id == ACCOUNT
        return JSON({
            'str': str(expression),
            'repr': repr(expression),
            'type': type(expression)})

    return 'Invalid argument: {}.'.format(arg)


ROUTES = (('GET', '/test/<arg>', test, 'test'),)
