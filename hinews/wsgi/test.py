"""Testing stuff."""

from peewee import DoesNotExist

from wsgilib import JSON

from his import ACCOUNT, CUSTOMER
from his.orm import Account

__all__ = ['ROUTES']


def get_account():
    """Returns the actual account ORM model's instance."""

    return Account.get(Account.id == ACCOUNT.id)


def get_accounts():

    return Account.select().where(Account.customer == CUSTOMER)


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
        return JSON([account.to_dict() for account in get_accounts()])
    elif arg == 'expr':
        expression = Account.id == ACCOUNT
        expression2 = Account.id == ACCOUNT.id
        select = Account.select().where(expression)
        return JSON({
            'expression1': {
                'str': str(expression),
                'repr': repr(expression),
                'type': str(type(expression)),
                'rhs': str(expression.rhs),
                'rhs_type': str(type(expression.rhs))},
            'expression2': {
                'str': str(expression2),
                'repr': repr(expression2),
                'type': str(type(expression2)),
                'rhs': str(expression2.rhs),
                'rhs_type': str(type(expression2.rhs))},
            'select': {
                'str': str(select),
                'repr': repr(select),
                'type': str(type(select))}})
    elif arg == 'eq2':
        co = ACCOUNT._get_current_object()
        return JSON({
            '1 == ACCOUNT': str(1 == ACCOUNT),
            '1 == ACCOUNT.id': str(1 == ACCOUNT.id),
            'ACCOUNT == 1': str(ACCOUNT == 1),
            'ACCOUNT.id == 1': str(ACCOUNT.id == 1),
            'current_object': {
                'str': str(co),
                'repr': repr(co),
                'type': str(type(co))}})
    elif arg == 'acc':
        return JSON(ACCOUNT.to_dict())

    return 'Invalid argument: {}.'.format(arg)


ROUTES = (('GET', '/test/<arg>', test, 'test'),)
