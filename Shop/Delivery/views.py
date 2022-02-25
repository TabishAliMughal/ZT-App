from django.shortcuts import render , redirect , get_object_or_404
from .models import *
from .forms import *
from Shop.Orders.forms import *
import datetime
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
from Authentication.user_handeling import allowed_users


def ManageDeliveryPersonListView(request):
    user = request.user.groups.values('name')
    persons = []
    for i in DeliveryPerson.objects.all():
        persons.append(i)
    context = {
        'user' : user,
        'persons' : persons ,
    }
    return render(request , 'delivery/person/list.html',context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Delivery'])
def ManageDeliveryPersonDataView(request):
    user = request.user.groups.values('name')
    form = ManageDeliveryPersonDataForm()
    person = ''
    stime = ''
    etime = ''
    for i in DeliveryPerson.objects.all():
        if str(i.user.pk) == str(request.user.pk):
            person = i
            stime = str(person.start_time)
            etime = str(person.end_time)
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
            }or None , instance = person)
        else:
            form = ManageDeliveryPersonDataForm({
                'user' : request.user.pk ,
                'name' : data.get('name') ,
                'start_time' : data.get('start_time') ,
                'end_time' : data.get('end_time') ,
                'active' : 'Active' ,
            })
        form.save()
        return redirect('/')
    else:
        context = {
            'stime': stime ,
            'etime': etime ,
            'person': person,
            'user' : user,
            'form': form ,
        }
        return render(request,'delivery/person/Data.html',context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Delivery'])
def ManageDeliveryPersonTasksListView(request):
    user = request.user.groups.values('name')
    tasks = []
    for i in DeliveryTasks.objects.all():
        if str(i.person.user.pk) == str(request.user.pk):
            tasks.append(i)
    context = {
        'user' : user,
        'tasks' : tasks ,
    }
    return render(request , 'delivery/person/Tasks/list.html',context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Delivery'])
def ManageDeliveryPersonTaskDetailView(request,task):
    user = request.user.groups.values('name')
    task = get_object_or_404(DeliveryTasks, pk = int(task))
    task_from = {'lat': task.task_from.address[1] , 'lon': task.task_from.address[0]}
    task_to = {'lat': task.task_to.address[1] , 'lon': task.task_to.address[0]}
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
    context = {
        'user' : user ,
        'task' : task ,
        'task_from' : task_from ,
        'task_to' : task_to ,
        'price':price ,
        'delivery':delivery ,
        'proof' : proof ,
    }
    return render(request , 'delivery/person/Tasks/detail.html',context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Public'])
def ManageDeliveryPersonTasksCreateView(request):
    if request.method == 'POST':
        data = request.POST
        shop = data.get('shop')
        delivery = data.get('delivery')
        person = data.get('person')
        order = data.get('order')
        date = str(datetime.date.today())
        for i in DeliveryTasks.objects.all():
            if str(i.order.pk) == str(order) and str(i.task_from) == str(shop) and str(i.task_to) == str(delivery) and str(i.date) == str(date):
                return render(request,'error.html',{'return':'Already Called'})
        taskform = ManageDeliveryPersonTasksForm({
            'person' : person ,
            'order' : order ,
            'task_from' : int(shop) ,
            'task_to' : int(delivery) ,
            'status' : 'Pending' ,
            'date' : date ,
        })
        taskform.save()
        person = get_object_or_404(DeliveryPerson,pk = person)
        personform = ManageDeliveryPersonDataForm({
            'user' : person.user ,
            'name' : person.name ,
            'start_time' : person.start_time ,
            'end_time' : person.end_time ,
            'active' : 'Bussy' ,
        } or None , instance = person)
        personform.save()
        order = get_object_or_404(Order, pk = order)
        orderform = OrderCreateForm({
            'user' : order.user ,
            'price' : order.price ,
            'delivery' : order.delivery ,
            'status' : 'Delivery Called' ,
        } or None , instance = order)
        orderform.save()
        return redirect('shop:shop_orders')

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Delivery'])
def ManageDeliveryPersonTaskCompleteView(request,task):
    order = get_object_or_404(DeliveryTasks, pk = int(task)).order
    if request.method == 'POST':
        image = Image.open(request.FILES.get('image'))
        size = image.size
        image = image.convert('RGB')
        rsize = []
        rsize.append(int(275*1))
        rsize.append(int(275*(size[0]/size[1])))
        rimg = image.resize(((rsize[1]),(rsize[0])),Image.ANTIALIAS)
        img_io = BytesIO()
        rimg.save(img_io, format='JPEG', quality=100)
        img_content = ContentFile(img_io.getvalue(),"img.jpg" )
        form = ManageDeliveryProofForm({
            'order' : order,
        },{
            'image': img_content
        })
        form.save()
        person = get_object_or_404(DeliveryPerson,user = int(request.user.pk))
        personform = ManageDeliveryPersonDataForm({
            'user' : person.user ,
            'name' : person.name ,
            'start_time' : person.start_time ,
            'end_time' : person.end_time ,
            'active' : 'Active' ,
        } or None , instance = person)
        personform.save()
        task = get_object_or_404(DeliveryTasks,pk = int(task))
        taskform = ManageDeliveryPersonTasksForm({
            'person' : task.person ,
            'order' : task.order ,
            'task_from' : task.task_from ,
            'task_to' : task.task_to ,
            'status' : 'Completed' ,
            'date' : task.date ,
        }or None , instance = task)
        taskform.save()
        order = get_object_or_404(Order, pk = int(order.pk))
        orderform = OrderCreateForm({
            'user' : order.user ,
            'price' : order.price ,
            'delivery' : order.delivery ,
            'paid' : True ,
            'status' : 'Delivered' ,
        } or None , instance = order)
        orderform.save()
        return redirect('delivery:delivery_person_tasks')
    else:
        return render(request,'delivery/person/Tasks/Deliver/Proof.html')



