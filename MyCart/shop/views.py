from PayTM import Checksum
from django.shortcuts import render
from django.http import HttpResponse
from math import ceil
from .models import Product, Contact, Orders, OrderUpdate
import json
from django.views.decorators.csrf import csrf_exempt

MERCHANT_KEY = 'kbzk1DSbJiV_03p5'

# Create your views here.
def index(req):
    # products = Product.objects.all()
    # print(products)
    # n = len(products)
    # nSlides = n//4 + ceil((n/4) - (n//4))
    # #params = {'no of slides': nSlides, 'range':range(1,nSlides), 'product':products}
    # allprods = [[products, range(1,nSlides), nSlides],[products, range(1,nSlides), nSlides]]
    # params = {'allProds':allProds}

    allProds = []
    catProds = Product.objects.values('category','id')
    print(catProds)
    cats = {item['category'] for item in catProds}
    print(cats)
    for cat in cats:
        prod = Product.objects.filter(category = cat)
        n = len(prod)
        nSlides = n//4 + ceil((n/4) - (n/4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds':allProds}
    return render(req,'shop/index.html',params)

def searchMatch(query, item):
    '''return true only if query matches the item'''
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(req):
    query = req.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]

        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg": ""}
    if len(allProds) == 0 or len(query)<4:
        params = {'msg': "Please make sure to enter relevant search query"}
    return render(req, 'shop/search.html', params)

def about(req):
    return render(req,'shop/about.html')

def contact(req):
    thank = False
    if req.method=='POST':
        name = req.POST.get('name')
        email = req.POST.get('email')
        phone = req.POST.get('phone')
        desc = req.POST.get('desc')
        print(name, email, phone, desc)
        cont = Contact(name=name, email= email, phone=phone, desc=desc)
        cont.save()
        id = cont.con_id
        thank = True
        return render(req,'shop/contact.html',{'thank':thank,'id':id})
    return render(req,'shop/contact.html')

def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status":"success", "updates": updates, "itemsJson": order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')

    return render(request, 'shop/tracker.html')

def prodview(req, myid):
    #Fetch the product using the id
    product = Product.objects.filter(id=myid)
    print(product)
    return render(req,'shop/prodview.html',{'product':product[0]})

def checkout(req):
    thank = False
    if req.method=="POST":
        items_json = req.POST.get('itemsJson', '')
        name = req.POST.get('name', '')
        amount = req.POST.get('amount', '')
        email = req.POST.get('email', '')
        address = req.POST.get('address1', '') + " " + req.POST.get('address2', '')
        city = req.POST.get('city', '')
        state = req.POST.get('state', '')
        zip_code = req.POST.get('zip_code', '')
        phone = req.POST.get('phone', '')
        order = Orders(items_json=items_json, name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone, amount=amount)
        order.save()
        update = OrderUpdate(order_id = order.order_id, update_desc="The order has been placed..")
        update.save()
        thank = True
        id = order.order_id
    #     return render(req, 'shop/checkout.html', {'thank':thank, 'id': id})
    # return render(req,'shop/checkout.html')
        # Request paytm to transfer the amount to your account after payment by user
        param_dict = {
                'MID': 'WorldP64425807474247',
                'ORDER_ID': str(order.order_id),
                'TXN_AMOUNT': str(amount),
                'CUST_ID': email,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlerequest/',

        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(req, 'shop/paytm.html', {'param_dict': param_dict})

    return render(req, 'shop/checkout.html')

@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    # form = request.POST
    # response_dict = {}
    # # checksum = request.POST.get('CHECKSUMHASH')
    # for i in form.keys():
    #     response_dict[i] = form[i]
    #     if i == 'CHECKSUMHASH':
    #         checksum = form[i]
    # #
    # verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    # if verify:
    #     if response_dict['RESPCODE'] == '01':
    #         print('order successful')
    #     else:
    #         print('order was not successful because' + response_dict['RESPMSG'])
    # return render(request, 'shop/paymentstatus.html', {'response': response_dict})
    return HttpResponse("done")
