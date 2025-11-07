from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.http import HttpResponse
from django.views.generic import CreateView, ListView
from transactions.constants2 import DEPOSIT, WITHDRAWAL,LOAN, LOAN_PAID
from datetime import datetime
from django.db.models import Sum
from transactions.forms import (
    DepositForm,
    WithdrawForm,
    LoanRequestForm,
)
from transactions.models import Transaction
from .forms import TransferForm
from django.shortcuts import render, redirect
from django.db import transaction
from django.views.generic.edit import FormView
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.mail import send_mail




def Email_feature(user, amount, subject, template, extra_context=None):
    context = {
        'user': user,
        'amount': amount,
    }
    if extra_context:
        context.update(extra_context)

    message = render_to_string(template, context)
    send_email = EmailMultiAlternatives(subject, '', to=[user.email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()








class TransactionCreateMixin(LoginRequiredMixin, CreateView):
    template_name = 'transaction/transaction_form.html'
    model = Transaction
    title = ''
    success_url = reverse_lazy('transaction_report')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account': self.request.user.account
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # template e context data pass kora
        context.update({
            'title': self.title
        })

        return context


class DepositMoneyView(TransactionCreateMixin):
    form_class = DepositForm
    title = 'Deposit'

    def get_initial(self):
        initial = {'transaction_type': DEPOSIT}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account
        # if not account.initial_deposit_date:
        #     now = timezone.now()
        #     account.initial_deposit_date = now
        account.balance += amount # amount = 200, tar ager balance = 0 taka new balance = 0+200 = 200
        account.save(
            update_fields=[
                'balance'
            ]
        )

        messages.success(
            self.request,
            f'{"{:,.2f}".format(float(amount))}$ was deposited to your account successfully'
        )
       

        Email_feature(self.request.user,amount,"Deposit Transaction",'transaction/deposit_Email.html')
        return super().form_valid(form)


class WithdrawMoneyView(TransactionCreateMixin):
    form_class = WithdrawForm
    title = 'Withdraw Money'

    def get_initial(self):
        initial = {'transaction_type': WITHDRAWAL}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')

        self.request.user.account.balance -= form.cleaned_data.get('amount')
        # balance = 300
        # amount = 5000
        self.request.user.account.save(update_fields=['balance'])

        messages.success(
            self.request,
            f'Successfully withdrawn {"{:,.2f}".format(float(amount))}$ from your account'
        )
        
        Email_feature(self.request.user,amount,"Withdraw Transaction",'transaction/deposit_Email.html')
        
        return super().form_valid(form)

class LoanRequestView(TransactionCreateMixin):
    form_class = LoanRequestForm
    title = 'Request For Loan'

    def get_initial(self):
        initial = {'transaction_type': LOAN}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        current_loan_count = Transaction.objects.filter(
            account=self.request.user.account,transaction_type=3,loan_approve=True).count()
        if current_loan_count >= 3:
            return HttpResponse("You have cross the loan limits")
        messages.success(
            self.request,
            f'Loan request for {"{:,.2f}".format(float(amount))}$ submitted successfully'
        )

        Email_feature(self.request.user,amount,"Loan Request ",'transaction/loan_Email.html')

        return super().form_valid(form)
    
class TransactionReportView(LoginRequiredMixin, ListView):
    template_name = 'transaction/transaction_report.html'
    model = Transaction
    balance = 0 # filter korar pore ba age amar total balance ke show korbe
    
    def get_queryset(self):
        queryset = super().get_queryset().filter(
            account=self.request.user.account
        )
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')
        
        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            
            queryset = queryset.filter(timestamp__date__gte=start_date, timestamp__date__lte=end_date)
            self.balance = Transaction.objects.filter(
                timestamp__date__gte=start_date, timestamp__date__lte=end_date
            ).aggregate(Sum('amount'))['amount__sum']
        else:
            self.balance = self.request.user.account.balance
       
        return queryset.distinct() # unique queryset hote hobe
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'account': self.request.user.account
        })

        return context
    
        
class PayLoanView(LoginRequiredMixin, View):
    def get(self, request, loan_id):
        loan = get_object_or_404(Transaction, id=loan_id)
        print(loan)
        if loan.loan_approve:
            user_account = loan.account
                # Reduce the loan amount from the user's balance
                # 5000, 500 + 5000 = 5500
                # balance = 3000, loan = 5000
            if loan.amount < user_account.balance:
                user_account.balance -= loan.amount
                loan.balance_after_transaction = user_account.balance
                user_account.save()
                loan.loan_approved = True
                loan.transaction_type = LOAN_PAID
                loan.save()
                return redirect('loan_list')
            else:
                messages.error(
            self.request,
            f'Loan amount is greater than available balance'
        )

        return redirect('loan_list')


class LoanListView(LoginRequiredMixin,ListView):
    model = Transaction
    template_name = 'transaction/loan_request.html'
    context_object_name = 'loans' # loan list ta ei loans context er moddhe thakbe

    def get_queryset(self):
        user_account = self.request.user.account
        queryset = Transaction.objects.filter(account=user_account,transaction_type=3)
        print(queryset)
        return queryset




class TransferView(LoginRequiredMixin, FormView):
    template_name = 'transaction/transfer.html'
    form_class = TransferForm
    success_url = reverse_lazy('transaction_report')

    @transaction.atomic
    def form_valid(self, form):
        sender = self.request.user.account
        receiver = form.cleaned_data['receiver_account']
        amount = form.cleaned_data['transfer_amount']


        if sender == receiver:
            form.add_error(None, "You cannot transfer money to your own account.")
            return self.form_invalid(form)


        if sender.balance < amount:
            form.add_error(None, "Insufficient balance.")
            return self.form_invalid(form)


        sender.balance -= amount
        receiver.balance += amount
        sender.save()
        receiver.save()

        # Create transaction records
        Transaction.objects.create(
            account=sender,
            amount=amount,
            balance_after_transaction=sender.balance,
            transaction_type=5
        )
        Transaction.objects.create(
            account=receiver,
            amount=amount,
            balance_after_transaction=receiver.balance,
            transaction_type=1
        )


        receiver_name = receiver.user.get_full_name() if hasattr(receiver, 'user') else 'Unknown User'
        receiver_account_no = getattr(receiver, 'account_no', 'N/A')

        # ✅ Send transfer confirmation email to sender
        Email_feature(
        user=self.request.user,
        amount=amount,
        subject="Money Transfer Confirmation",
        template='transaction/transferMoney_Email.html',
        extra_context={
            'receiver_name': receiver.user.get_full_name(),
            'receiver_account': receiver.account_no,
            'user_balance': sender.balance
            }
        )


        return super().form_valid(form)




class TransferListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'transaction/transfer_list.html'
    context_object_name = 'transfers'

    def get_queryset(self):
        user_account = self.request.user.account
        # Filter only transfer transactions (transaction_type=5)
        return Transaction.objects.filter(account=user_account, transaction_type=5).order_by('-timestamp')
