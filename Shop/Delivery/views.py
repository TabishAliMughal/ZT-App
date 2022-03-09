from multiprocessing import context
from django.shortcuts import render , redirect , get_object_or_404

from App.User.models import UserData
from .models import *
from .forms import *
from Shop.Orders.forms import *
from datetime import datetime
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
from App.Authentication.user_handeling import allowed_users
from math import sin, cos, sqrt, atan2, radians


def ManageDeliveryPersonListView(request):
    persons = []
    for i in DeliveryPerson.objects.all():
        persons.append(i)
    context = {
        'persons' : persons ,
    }
    return render(request , 'Delivery/Person/list.html',context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Delivery'])
def ManageDeliveryPersonDataView(request):
    form = ManageDeliveryPersonDataForm()
    person = ''
    stime = ''
    etime = ''
    lat = ''
    lon = ''
    for i in DeliveryPerson.objects.all():
        if str(i.user) == str(request.user.pk):
            person = i
            stime = str(person.start_time)
            etime = str(person.end_time)
            lat = str(person.area[1])
            lon = str(person.area[0])
    if person != '':
        form = ManageDeliveryPersonDataForm(instance=person)
    if request.method == 'POST':
        data = request.POST
        if person != '':
            form = ManageDeliveryPersonDataForm({
                'user' : request.user.pk ,
                'name' : data.get('name') ,
                'start_time' : data.get('start_time') ,
                'end_time' : data.get('end_time') ,
                'active' : 'Active' ,
                'mobile' : data.get('mobile') ,
                'nic' : data.get('nic') ,
                'bank_account' : data.get('bank_account') ,
                'easypaisa' : data.get('easypaisa') ,
                'area' : data.get('area') ,
            }or None , instance = person)
        else:
            form = ManageDeliveryPersonDataForm({
                'user' : request.user.pk ,
                'name' : data.get('name') ,
                'start_time' : data.get('start_time') ,
                'end_time' : data.get('end_time') ,
                'active' : 'Active' ,
                'mobile' : data.get('mobile') ,
                'nic' : data.get('nic') ,
                'bank_account' : data.get('bank_account') ,
                'easypaisa' : data.get('easypaisa') ,
                'area' : data.get('area') ,
            })
        form.save()
        return redirect('/')
    else:
        context = {
            'stime': stime ,
            'etime': etime ,
            'lat': lat ,
            'lon': lon ,
            'person': person,
            'form': form ,
        }
        return render(request,'Delivery/Person/Data.html',context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Delivery'])
def ManageDeliveryPersonTasksListView(request):
    tasks = []
    rider = get_object_or_404(DeliveryPerson,user = request.user.pk)
    for i in DeliveryTasks.objects.all():
        if str(i.person.user) == str(request.user.pk):
            tasks.append(i)
    context = {
        'tasks' : tasks ,
        'rider' : rider ,
    }
    return render(request , 'Delivery/Person/Tasks/list.html',context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Delivery'])
def ManageDeliveryPersonTaskDetailView(request,task):
    task = get_object_or_404(DeliveryTasks, pk = int(task))
    task_from = {'lat': task.task_from.address[1] , 'lon': task.task_from.address[0]}
    print()
    task_to = {'lat': (get_object_or_404(UserData , pk = task.task_to)).address[1] , 'lon': (get_object_or_404(UserData , pk = task.task_to)).address[0]}
    price = int('0')
    proof = []
    for i in OrderItem.objects.all():
        if str(i.order.pk) == str(task.order.pk):
            price = i.order.price
            delivery = i.order.delivery
            if str(i.order.status) == 'Delivered':
                for t in DeliveryProof.objects.all():
                    if i.order == t.order:
                        proof.append(t.image.url)
    total = int(price) + int(delivery)
    context = {
        'task' : task ,
        'task_from' : task_from ,
        'task_to' : task_to ,
        'total':total ,
        'proof' : proof ,
    }
    return render(request , 'Delivery/Person/Tasks/detail.html',context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Delivery'])
def ManageDeliveryPersonTasksCreateView(request):
    if request.method == 'POST':
        data = request.POST
        rider = get_object_or_404(DeliveryPerson, user = data.get('rider'))
        order = get_object_or_404(Order , pk = data.get('order'))
        for k in OrderItem.objects.all().filter(order = order):
            pick = k.product.shop
        form = ManageDeliveryPersonTasksForm({
            'person' : rider ,
            'order' : order ,
            'task_from' : get_object_or_404(Shops ,pk = data.get('from')) ,
            'task_to' : get_object_or_404(UserData , pk = data.get('to')).pk ,
            'status' : 'Processing' ,
        })
        print(form)
        task = form.save()
        Order.objects.filter(pk = order.pk).update(status = 'OrderPickProcessing')
        DeliveryPerson.objects.filter(pk = rider.pk).update(active = 'Bussy')
        return redirect('shop_delivery:delivery_person_task_detail',task.pk)
    else:
        orders = []
        for i in Order.objects.all().filter(status = 'DeliveryCalled'):
            for k in OrderItem.objects.all().filter(order = i):
                pick = k.product.shop
                break
            drop = get_object_or_404(UserData,pk = i.user)
            R = 6373.0
            lat1 = radians(pick.address[0])
            lon1 = radians(pick.address[1])
            lat2 = radians(drop.address[0])
            lon2 = radians(drop.address[1])
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            distance = R * c
            orders.append({'order': i , 'pick' : pick , 'drop' : drop , 'distance' : str(distance)[:5]})
        context = {
            'orders' : orders ,
        }
        return render(request,'Delivery/Person/PickOrder.html',context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Delivery'])
def ManageDeliveryPersonTaskCompleteView(request,task=None):
    order = get_object_or_404(DeliveryTasks, pk = int(task)).order
    if request.method == 'POST':
        import base64
        im = Image.open(BytesIO(base64.b64decode(request.POST.get('image')[22:])))
        image = im.convert('RGB')
        size = image.size
        rsize = []
        rsize.append(int(275*1))
        rsize.append(int(275*(size[0]/size[1])))
        rimg = image
        img_io = BytesIO()
        rimg.save(img_io, format='JPEG', quality=75)
        img_content = ContentFile(img_io.getvalue(),"img.jpg" )
        print(img_content)
        form = ManageDeliveryProofForm({
            'order' : order,
        },{
            'image': img_content
        })
        print(form)
        form.save()
        # person = get_object_or_404(DeliveryPerson,user = int(request.user.pk))
        # person.update(active = 'Active')
        DeliveryPerson.objects.filter(user = int(request.user.pk)).update(active = 'Active')
        # personform = ManageDeliveryPersonDataForm({
        #     'user' : person.user ,
        #     'name' : person.name ,
        #     'start_time' : person.start_time ,
        #     'end_time' : person.end_time ,
        #     'active' : 'Active' ,
        # } or None , instance = person)
        # personform.save()
        task = DeliveryTasks.objects.filter(pk = int(task)).update(status = 'Completed',drop = datetime.now())
        # taskform = ManageDeliveryPersonTasksForm({
        #     'person' : task.person ,
        #     'order' : task.order ,
        #     'task_from' : task.task_from ,
        #     'task_to' : task.task_to ,
        #     'status' : 'Completed' ,
        #     'date' : task.date ,
        # }or None , instance = task)
        # taskform.save()
        order = Order.objects.filter(pk = int(order.pk)).update(status = 'Delivered',paid = 'True')
        # order = get_object_or_404(Order, pk = int(order.pk))
        # orderform = OrderCreateForm({
        #     'user' : order.user ,
        #     'price' : order.price ,
        #     'delivery' : order.delivery ,
        #     'paid' : True ,
        #     'status' : 'Delivered' ,
        # } or None , instance = order)
        # orderform.save()
        return redirect('shop_delivery:delivery_person_tasks')
    else:
        context = {
        }
        return render(request,'Delivery/Person/Tasks/Deliver/Proof.html',context)

def ManageDeliveryPersonPickOrderView(request,pk):
    task = get_object_or_404(DeliveryTasks,pk = pk)
    DeliveryTasks.objects.filter(pk = pk).update(pick = datetime.now())
    Order.objects.filter(pk = task.order.pk).update(status = 'OutForDelivery')
    return redirect('shop_delivery:delivery_person_task_detail',task.pk)
    

