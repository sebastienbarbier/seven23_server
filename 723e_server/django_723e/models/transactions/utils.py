# -*- coding: utf-8 -*-

def recalculateAllTransactionsAfterChange(firstChange):

    from django_723e.models.transactions.models import Change, AbstractTransaction

    """
        Get firstChange object and recalculate all transactions before it.
        Arg1 is a Change.
        Clear all firstChange after
        Get All firstChange and for each apply balance on an available transaction
    """
    # If c is not a Change, no actions.
    if type(firstChange) is not Change:
        return None


