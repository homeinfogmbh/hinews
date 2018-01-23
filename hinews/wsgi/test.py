"""Testing stuff."""

from his import ACCOUNT
from his.orm import Account

from wsgilib import JSON

__all__ = ['ROUTES']


def get_account():
    """Returns the actual account ORM model's instance."""

    return Account.get(Account.id == ACCOUNT.id)


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

    return 'Invalid argument: {}.'.format(arg)


ROUTES = (('GET', '/test/<arg>', test, 'test'),)
