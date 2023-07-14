from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from .forms import oderform1
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .decoraters import *
from django.contrib.auth.models import Group

@unauthenticated
def loginform(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'Username or Password is invalid')
    context={}
    return render(request,'accounts/login.html',context)

@unauthenticated
def registerform(request):
    form=createuserform()
    if request.method=='POST':
        form=createuserform(request.POST)
        if form.is_valid():
            user= form.save()
            group=Group.objects.get(name='customer')
            user.groups.add(group)
            messages.success(request,'account created successfully')
            return redirect('login')
    context={'form':form}
    return render(request,'accounts/register.html',context)

def logoutuser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@admin_only
def home(request):
    customer=Customer.objects.all()
    orders=Order.objects.all()
    total_orders=orders.count()
    total_delivered=orders.filter(status='delivered').count()
    total_pending=orders.filter(status='pending').count()
    context={'customer':customer,'orders':orders,'total_orders':total_orders,'total_delivered':total_delivered,'total_pending':total_pending}
    return render(request,'accounts/dashboard.html',context) 

def user_page(request):
    context={}
    return render(request,"accounts/userpage.html",context)

@login_required(login_url='login')
def products(request):
    products=Product.objects.all()
    return render(request,'accounts/products.html',{'products':products})

@login_required(login_url='login')
def customer(request,pk):
    customer=Customer.objects.get(id=pk)
    orders=customer.order_set.all()
    order_count=orders.count()
    context={'customer':customer,'orders':orders,'order_count':order_count}
    return render(request,'accounts/customers.html',context)
@login_required(login_url='login')
def create_order(request,pk):
    OrderFormSet=inlineformset_factory(Customer,Order,fields=('product','status'),extra=5)
    customer=Customer.objects.get(id=pk)
    #form=orderform(initial={'customer':customer})
    formset=OrderFormSet(queryset=Order.objects.none(),instance=customer)
    if request.method=="POST":
        #form=orderform(request.POST)
        formset=OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context={'formset':formset}
    return render(request,'accounts/order_form.html',context)
@login_required(login_url='login')
def update_order(request,pk):
    order=Order.objects.get(id=pk)
    form=oderform1(instance=order)
    if request.method=="POST":
        form=oderform1(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context={'form':form}
    return render(request,'accounts/update_order.html',context)

@login_required(login_url='login')
def delete_order(request,pk):
    order=Order.objects.get(id=pk)
    if request.method=='POST':
        order.delete()
        return redirect('/')
    context={'item':order}
    return render(request,'accounts/delete_order.html',context)
