from django import forms
from .models import Transaction,UserBankAccount
class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            'amount',
            'transaction_type'
        ]

    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account') # account value ke pop kore anlam
        super().__init__(*args, **kwargs)
        self.fields['transaction_type'].disabled = True # ei field disable thakbe
        self.fields['transaction_type'].widget = forms.HiddenInput() # user er theke hide kora thakbe

    def save(self, commit=True):
        self.instance.account = self.account
        self.instance.balance_after_transaction = self.account.balance
        return super().save()


class DepositForm(TransactionForm):
    def clean_amount(self): # amount field ke filter korbo
        min_deposit_amount = 100
        amount = self.cleaned_data.get('amount') # user er fill up kora form theke amra amount field er value ke niye aslam, 50
        if amount < min_deposit_amount:
            raise forms.ValidationError(
                f'You need to deposit at least {min_deposit_amount} $'
            )

        return amount


class WithdrawForm(TransactionForm):

    def clean_amount(self):
        account = self.account
        min_withdraw_amount = 500
        max_withdraw_amount = 20000
        balance = account.balance # 1000
        amount = self.cleaned_data.get('amount')
        if amount < min_withdraw_amount:
            raise forms.ValidationError(
                f'You can withdraw at least {min_withdraw_amount} $'
            )

        if amount > max_withdraw_amount:
            raise forms.ValidationError(
                f'You can withdraw at most {max_withdraw_amount} $'
            )

        if amount > balance: # amount = 5000, tar balance ache 200
            raise forms.ValidationError(
                f'You have {balance} $ in your account. '
                'You can not withdraw more than your account balance'
            )

        return amount



class LoanRequestForm(TransactionForm):
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')

        return amount





class TransferForm(forms.ModelForm):
    to_account = forms.CharField(
        label="Receiver Account Number",
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )
    transfer_amount = forms.DecimalField(
        label="Amount ($)",
        max_digits=12,
        decimal_places=2,
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',

        })
    )

    class Meta:
        model = Transaction
        fields = []  # ✅ no need to include 'account' here — set it in the view manually

    def clean(self):
        cleaned_data = super().clean()
        to_account_no = cleaned_data.get('to_account')
        amount = cleaned_data.get('transfer_amount')

        # Validate receiver account
        try:
            receiver = UserBankAccount.objects.get(account_no=to_account_no)
        except UserBankAccount.DoesNotExist:
            raise forms.ValidationError("Receiver account not found.")

        # store for use in the view
        cleaned_data['receiver_account'] = receiver

        if amount and amount <= 0:
            raise forms.ValidationError("Transfer amount must be greater than zero.")

        return cleaned_data