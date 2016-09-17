.. _models:

Data structure
######

User
====

Login required to provide a username and password. Those information are stored in default Django auth structure.
A user is unique, defined by a username.

Account
=======

A user can own multiple account (which might be represented as Bank account). Current version only allow one account (to simplify development). Model is store in ``django_723e/models/accounts/models.py`` and has the following structure :

.. code-block:: python

	class Account(models.Model):
	    user     = models.ForeignKey(User, related_name="accounts")
	    name     = models.CharField(_(u'Name'), max_length=255)
	    create   = models.DateField(_(u'Creation date'), auto_now=True, editable=False)
	    currency = models.ForeignKey(Currency, related_name='accounts')

By default, an account is related to unique user. It has a name, a creation date, and a main currency *(described bellow)*.

Currency
========

Every transaction is done in a unique currency. Model is store in ``django_723e/models/currency/models.py`` and has the following structure :

.. code-block:: python

	class Currency(models.Model):
	    name = models.CharField(_('Name'), max_length=128)
	    sign = models.CharField(_('Sign'), max_length=6)
	    space = models.BooleanField(_(u'Add a space between amount and sign'), default=True)
	    after_amount = models.BooleanField(_(u'Sign position'), choices=((False, _(u'Before the amount')), (True, _(u'After the amount'))), default=True)

Categories
==========

A transaction can be assign to a category to help classification and manipulation. Model is store in ``django_723e/models/categories/models.py`` and has the following structure :

.. code-block:: python

	class Category(MPTTModel):
	    """
	        Category of transaction.
	    """
	    user        = models.ForeignKey(User, related_name='categories')
	    name        = models.CharField(_(u'Name'), max_length=128)
	    description = models.TextField(_(u'Description'), blank=True, null=True)
	    color       = ColorField(default='ffffff')
	    icon        = models.TextField(_(u'Icon'))
	    parent      = TreeForeignKey('self', null=True, blank=True, related_name='children')
	    selectable  = models.BooleanField(_(u'Selectable'), default=True, help_text=_(u"Can be link to a transaction"))
	    active      = models.BooleanField(_(u'Enable'), default=True, help_text=_(u"Delete a category only disable it"))

A category cannot be deleter if it is assigned to at least one transaction. Instead, it is disabled.
Categories have stored as a modified pre-order traversal tree using `django-mptt libary <https://github.com/django-mptt/django-mptt>`_.

Transactions
============

A transaction can be a ``Change``, or a ``DebitsCredits``. Both extend an abstract model ``AbstractTransaction``.
Models are store in ``django_723e/models/transactions/models.py``.

AbstractTransaction
-------------------

Both ``Change`` and ``DebitsCredits`` own the following attributes.

.. code-block:: python

	class AbstractTransaction(models.Model):
	    account          = models.ForeignKey(Account, related_name='transactions')
	    name             = models.CharField(_(u'Name'), max_length=255)
	    amount           = models.FloatField(_(u'Amount'), null=False, blank=False, help_text=_(u"Credit and debit are represented by positive and negative value."))
	    currency         = models.ForeignKey(Currency, related_name='transactions')
	    category         = models.ForeignKey(Category, related_name='transactions', blank=True, null=True)
	    date             = models.DateField(_(u'Date'), editable=True, default=timezone.now)
	    active           = models.BooleanField(_(u'Enable'), default=True, help_text=_(u"A disabled transaction will be save as a draft and not use in any report."))
	    reference_amount = models.FloatField(_(u'Reference Amount'), null=True, blank=True, editable=False, help_text=_(u"Value based on account curency."))

``reference_amount`` is a stored calculated version of ``amount`` based on ``account.currency``. This is done on purpose to allow fast database calculation and manipulation. However, it involve on account.currency change event to recalculate all transaction in datbase which might consume time and ressources.

``reference_amount`` is also recalculated when a ``change`` model is edited.

.. note::

	This structure seams far from being optimum and should be subject to some refactoring.

DebitsCredits
-------------

``DebitsCredits`` has no difference with ``AbstractTransaction`` and just override *__unicode__* methode.

Change
------

``Change`` keep the same structure as ``AbstractTransaction`` but add two attributes ``new_amount`` and ``new_currency``.

.. code-block:: python

	class Change(AbstractTransaction):
	    new_amount   = models.FloatField(_(u'New Amount'), null=False, blank=False, help_text=_(u"Amount of cash in the new currency"))
	    new_currency = models.ForeignKey(Currency, related_name="change", blank= True, null= True)
