# -*- coding: utf-8 -*-

def recalculateAllTransactionsAfterChange(firstChange):
    
    from django_723e.models.transactions.models import Change, Transaction, Transaction2Change

    """
        Get firstChange object and recalculate all transactions before it.
        Arg1 is a Change.
        Clear all firstChange after
        Get All firstChange and for each apply balance on an available transaction
    """
    # If c is not a Change, no actions.
    if type(firstChange) is not Change:
        return None
    
    list_change = Change.objects.filter(account=firstChange.account, date__gte=firstChange.date, new_currency=firstChange.new_currency).order_by("date")
    
    # On supprime toutes les transactions
    for c in list_change:
        for t in c.transactions.all():
            t.delete()
            
    list_change = list_change.all()
    currentChangeIndex = 0
    currentChange = list_change[currentChangeIndex]
    # List of transaction with same currency and after firstChange date
    list_transactions = Transaction.objects.filter(currency=firstChange.new_currency, date__gte=firstChange.date).order_by("date")
    # For each transaction
    for t in list_transactions:
        if currentChange.date <= t.date:
            if not t.is_change_complete():
                while len(list_change) > currentChangeIndex and t.due_to_change() != 0.0:
                    if currentChange.balance >= t.due_to_change():
                        due = t.due_to_change()
                        Transaction2Change.objects.create(transaction=t,
                                                          transaction_amount=due,
                                                          change=currentChange,
                                                          change_amount=(currentChange.amount*due/currentChange.new_amount))
                    else:
                        Transaction2Change.objects.create(transaction=t,
                                                          transaction_amount=currentChange.balance,
                                                          change=currentChange,
                                                          change_amount=(currentChange.amount*currentChange.balance/currentChange.new_amount))
                        currentChangeIndex += 1
                        if len(list_change) > currentChangeIndex:
                            currentChange = list_change[currentChangeIndex]

