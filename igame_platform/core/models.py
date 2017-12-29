# -*- coding: utf-8 -*-
from decimal import Decimal
from model_utils import Choices
from model_utils.models import TimeStampedModel

from django.db import models
from django.db import transaction
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


class Bonus(models.Model):
    """
    TODO: add me
    """
    class Meta:
        verbose_name = 'Bonus'
        verbose_name_plural = 'Bonuses'

    EVENT_TYPES = Choices(
        ('login', 'Login'),
        ('deposit', 'Deposit'),
    )
    BONUS_TYPES = Choices(
        ('RM', 'Real money'),
        ('BM', 'Bonus money'),
    )

    name = models.CharField(max_length=10, choices=EVENT_TYPES, unique=True)
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    rule = models.CharField(max_length=100, blank=True, default='')
    wagering_requirement = models.PositiveSmallIntegerField(
        blank=True, null=True,
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    bonus_type = models.CharField(
        max_length=10,
        choices=BONUS_TYPES,
        default=BONUS_TYPES.RM,
    )
    is_active = models.BooleanField(
        'active',
        default=True,
    )

    @classmethod
    def apply_bonus(cls, bonus_name, user, kwargs={}):
        """
        TODO: add me
        """
        success = False
        message = ''
        try:
            bonus_obj = cls.objects.get(name=bonus_name)
        except cls.DoesNotExist:
            # Here maybe is a good place to log a message
            message = 'The requested bonus does not exist'
            return success, message

        if bonus_obj.is_real_money_bonus:
            # Perform a deposit in the user account
            Account.deposit_real_money_bonus(user, bonus_obj.amount)
            success = True
            return success, message

        if bonus_obj.is_default_money_bonus:
            # Create bonus object to wager
            pass

        return success, message

    @property
    def is_real_money_bonus(self):
        return self.bonus_type == self.BONUS_TYPES.RM

    @property
    def is_default_money_bonus(self):
        return self.bonus_type == self.BONUS_TYPES.BM


class Account(TimeStampedModel):

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

    user = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
    )
    balance = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        validators=[MinValueValidator(Decimal('0'))]
    )

    @classmethod
    def create(cls, user):
        """
        Create account.
        """
        with transaction.atomic():
            account = cls.objects.create(
                user=user,
                balance=0,
            )

        return account

    @classmethod
    def deposit(cls, user, amount):
        return cls.handle_transaction(
            user, amount, Transaction.TRANSACTION_TYPES.deposit, 'add'
        )

    @classmethod
    def bet(cls, user, amount):
        return cls.handle_transaction(
            user, amount, Transaction.TRANSACTION_TYPES.bet, 'substract'
        )

    @classmethod
    def deposit_win(cls, user, amount):
        return cls.handle_transaction(
            user, amount, Transaction.TRANSACTION_TYPES.win_benefit, 'add'
        )

    @classmethod
    def deposit_real_money_bonus(cls, user, amount):
        return cls.handle_transaction(
            user, amount, Transaction.TRANSACTION_TYPES.real_bonus, 'add'
        )

    @classmethod
    def deposit_wagered_bonus(cls, user, amount):
        return cls.handle_transaction(
            user, amount, Transaction.TRANSACTION_TYPES.wagering, 'add'
        )

    @classmethod
    def handle_transaction(cls, user, amount, trans_type, action):

        with transaction.atomic():
            account = cls.objects.select_for_update().get(user=user)
            if action == 'add':
                account, new_transaction = account.add_to_balance(
                    amount, trans_type
                )
            elif action == 'substract':
                account, new_transaction = account.substract_from_balance(
                    amount, trans_type
                )
            else:
                account, new_transaction = None, None
        return account, new_transaction

    def add_to_balance(self, amount, trans_type):

        self.balance += amount
        self.save()

        new_transaction = Transaction.create(self, trans_type, amount)

        return self, new_transaction

    def substract_from_balance(self, amount, trans_type):

        self.balance -= amount
        self.save()

        new_transaction = Transaction.create(self, trans_type, -amount)

        return self, new_transaction


class Transaction(models.Model):

    TRANSACTION_TYPES = Choices(
        ('deposit', 'Deposit'),
        ('bet', 'Bet'),
        ('win_benefit', 'Win'),
        ('real_bonus', 'Real bonus money'),
        ('wagering', 'Wagered bonus'),
    )

    account = models.ForeignKey(Account, related_name='transactions_info')
    trans_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    delta = models.DecimalField(
        decimal_places=2,
        max_digits=12
    )
    debug_balance = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        validators=[MinValueValidator(Decimal('0'))]
    )
    created = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create(cls, account, trans_type, delta):

        with transaction.atomic():
            new_transaction = cls.objects.create(
                account=account,
                trans_type=trans_type,
                delta=delta,
                debug_balance=account.balance,
            )

        return new_transaction
