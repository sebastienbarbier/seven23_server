.. _rules:

Rules
#####

A set of rules keep consistency in datas. Mostly on multi currency calculation.
Those rules are subject to many unittest.

Refresh reference_amount
========================

When changing ``account.currency`` or a ``change`` object, we have to recalculate ``DebitsCredits.reference_amount`` to keep consistency in our data structure.

On ``account.currency`` modification, we select all ``DebitsCredits`` and update the amount.

On ``change`` modification, we only select ``DebitsCredits`` younger than it and older than the same transaction type which will be used for even younger change.

.. note::
	This process is really expensive on time and ressource, should be used carefully

To calculate the exchange rate, we need to consulte ``Change`` object, but also try to combine them if more than two currency are involced.

**Example** :
Changing ``10€ > 20 CHF``, then ``20 CHF > 30 USD``, exchange rate should be seen as ``10€ > 30 USD``.
This simple case is recursive and apply for ``n`` currency. Also will be able to change ``USD > EUR`` or ``EUR > USD`` by looking at reversed transaction.
