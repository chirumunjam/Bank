from django.shortcuts import render,HttpResponse,redirect
from .forms import AccountForm
from .models import Account
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

#app password
# ========================
# zhqv nptt wtbk acjp

def index(request):  
    return render(request, 'index.html')

def register(request):
    form = AccountForm()
    if request.method == 'POST':
        form = AccountForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            receiver_mail = form.data['email']
            data =Account.objects.get(email=receiver_mail)
            acc = data.acc_no
            try:
                send_mail(
                    'Account Number',
                    f'Thank you for registering with our Chiru Bank. We are excited to have you on board! Your account number is {acc} \n Thank you \n Regards \n Chiru Bank',
                    settings.EMAIL_HOST_USER, 
                    [receiver_mail],fail_silently = False,
                )
                return redirect('index')
            except Exception as e:
                return HttpResponse(f'Email not sent: {e}')
            
    return render(request, 'register.html',{'form':form})

def pin(request):
    if request.method == 'POST':
        acc = request.POST.get('acc_no')
        mobile = request.POST.get('mobile')
        pin1 = request.POST.get('pin1')
        pin2 = request.POST.get('pin2')
        pin3 = request.POST.get('pin3')
        pin4 = request.POST.get('pin4')
        confirm_pin1 = request.POST.get('confirm_pin1')
        confirm_pin2 = request.POST.get('confirm_pin2')
        confirm_pin3 = request.POST.get('confirm_pin3')
        confirm_pin4 = request.POST.get('confirm_pin4')
        
        pin = int(str(pin1) + str(pin2) + str(pin3) + str(pin4))
        cpin = int(str(confirm_pin1) + str(confirm_pin2) + str(confirm_pin3) + str(confirm_pin4))
        try:
            accno = Account.objects.get(acc_no=acc)
        except:
            return HttpResponse('Account not found')
        finally:
            print('exception handled')
        if accno.mobile == int(mobile):
            if pin == cpin:
                pin+=111
                accno.pin = pin
                accno.save()
                try:
                    send_mail(
                        'Pin Number',
                        f'Thank you for registering with our Chiru Bank. We are excited to have you on board! You have successfully set your PIN. \n Thank you \n Regards \n Chiru Bank',
                        settings.EMAIL_HOST_USER, 
                        [accno.email],fail_silently = False,
                    )
                    return redirect('index')
                except Exception as e:
                    return HttpResponse(f'Email not sent: {e}')   
            else:
                return HttpResponse('Pin does not match')
        else:
            return HttpResponse('Mobile number does not match')
    return render(request, 'pin.html')


def balance(request):
    bal =0
    var = False
    if request.method == 'POST':
        var = True
        acc = request.POST.get('acc_no')
        pin1 = int(request.POST.get('pin1'))
        pin2 = int(request.POST.get('pin2'))
        pin3 = int(request.POST.get('pin3'))
        pin4 = int(request.POST.get('pin4'))
        try:
            accno = Account.objects.get(acc_no=acc)
        except:
            return HttpResponse('Account not found')
        encpin = int(str(pin1) + str(pin2) + str(pin3) + str(pin4))+111
        print(encpin)
        if accno.pin==encpin:
            bal = accno.balance
        else:
            return HttpResponse('Pin does not match')
    return render(request, 'balance.html',{'bal':bal,'var':var})

def deposit(request):
    if request.method == 'POST':
        acc = request.POST.get('acc_no')
        mobile = request.POST.get('mobile')
        amount = int(request.POST.get('amount'))
        try:
            accno = Account.objects.get(acc_no=acc)
        except:
            return HttpResponse('Account not found')
        if accno.mobile == int(mobile):
            if amount>=100 and amount<=10000:
                accno.balance += amount
                accno.save()
                try:
                    send_mail(
                        'Deposit',
                        f'You have successfully deposited {amount}. \n Thank you \n Regards \n Chiru Bank',
                        settings.EMAIL_HOST_USER, 
                        [accno.email],fail_silently = False,
                    )
                    return redirect('index')
                except Exception as e:
                    return HttpResponse(f'Email not sent: {e}')
            else:
                return HttpResponse('Please enter Amount Between 100 and 10000')
        else:
            return HttpResponse('Mobile number does not match')
        
    return render(request, 'deposit.html')


def withdraw(request):
    if request.method == 'POST':
        acc = request.POST.get('acc_no')
        pin1 = request.POST.get('pin1')
        pin2 = request.POST.get('pin2')
        pin3 = request.POST.get('pin3')
        pin4 = request.POST.get('pin4')
        amount = request.POST.get('amount')
        try:
            accno = Account.objects.get(acc_no=acc)
        except:
            return HttpResponse('Account not found')
        encpin = int(str(pin1) + str(pin2) + str(pin3) + str(pin4))+111
        if accno.pin==encpin:
            if accno.balance>=int(amount):
                accno.balance -= int(amount)
                accno.save()
                try:
                    send_mail(
                        'Withdrawal',
                        f'You have successfully withdraw {amount}. \n Thank you \n Regards \n Chiru Bank',
                        settings.EMAIL_HOST_USER, 
                        [accno.email],fail_silently = False,
                    )
                    return redirect('index')
                except Exception as e:
                    return HttpResponse(f'Email not sent: {e}')           
            else:
                return HttpResponse('Insufficient balance')
        else:
            return HttpResponse('Pin does not match')

    return render(request, 'withdraw.html')


def transfer(request):
    if request.method == 'POST':
        acc = request.POST.get('acc_no')
        other_acc = request.POST.get('other_acc_no')
        amount = request.POST.get('amount')
        pin1 = request.POST.get('pin1')
        pin2 = request.POST.get('pin2')
        pin3 = request.POST.get('pin3')
        pin4 = request.POST.get('pin4')
        pin = int(str(pin1) + str(pin2) + str(pin3) + str(pin4))+111
        try:
            accno = Account.objects.get(acc_no=acc)
            
        except:
            return HttpResponse('From Account not found')
        try:
            other_accno = Account.objects.get(acc_no=other_acc)
        except:
            return HttpResponse('To Account not found')
        if accno.balance>=int(amount) and accno.pin==pin:
            accno.balance -= int(amount)
            accno.save()
            other_accno.balance += int(amount)
            other_accno.save()
            try:
                send_mail(
                    'Sent',
                    f'You have successfully transferred {amount} to {other_accno.name} with accoount number {other_accno.acc_no}. \n Thank you \n Regards \n Chiru Bank',
                    settings.EMAIL_HOST_USER, 
                    [accno.email],fail_silently = False,
                )
                send_mail(
                    'Received',
                    f'Your account has been credited with {amount} from {accno.name} with accoount number {accno.acc_no}. \n Thank you . \n Regards \n Chiru Bank',
                    settings.EMAIL_HOST_USER,
                    [other_accno.email],fail_silently = False,
                )
                return redirect('index')
            except Exception as e:
                return HttpResponse(f'Email not sent: {e}')
        else:
            return HttpResponse('Insufficient balance')
    return render(request, 'transfer.html')