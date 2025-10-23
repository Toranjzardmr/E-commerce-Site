from django.shortcuts import render,redirect
from . import models
from django.core.paginator import Paginator
from django.contrib import messages

# Create your views here.

def index(request):

    product_obj = models.Products.objects.all()

    #Search code
    item_name = request.GET.get('item_name')
    if item_name != '' and item_name is not None:
        product_obj = models.Products.objects.filter(title__icontains=item_name)

    #Pagination code
    paginator = Paginator(product_obj,4)
    page = request.GET.get('page')
    product_obj = paginator.get_page(page)

    context = {
        'product_obj':product_obj
    }
    return render(request,'shop/index.html',context)

def detail(request,item_id):

    product_obj = models.Products.objects.get(pk = item_id)

    context = {
        'product_obj':product_obj
    }
    return render(request,'shop/detail.html',context)


def checkout(request):

    if request.method == "POST":
        name = request.POST.get('name',"")
        email = request.POST.get('email',"")
        address = request.POST.get('address',"")
        city = request.POST.get('city',"")
        total = request.POST.get('total',"")
        items = request.POST.get('items',"")

        order = models.Order(name=name, email=email, address=address, total=total, city=city, items=items)
        order.save()
        messages.success(request,'Your order has been placed.')
        
        return redirect('index')

    return render(request,'shop/checkout.html',context={})