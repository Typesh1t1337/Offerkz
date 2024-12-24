

from django.contrib.auth import get_user_model
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from tasks.models import Task,Chat,AssignedTask,Message
from django.db.models import Q
from django.http import HttpResponseRedirect
from tasks.forms import TaskForm, FilterTaskForm,EditTaskForm
from django.views.generic import ListView, DeleteView, FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class IndexView(LoginRequiredMixin,ListView):
    model = Task
    template_name = "tasks/main.html"
    context_object_name = "tasks"
    paginate_by = 18
    redirect_field_name = "tasks/"
    form_class = FilterTaskForm


    def __init__(self, *args, **kwargs):
        self.is_filter = kwargs.pop('is_filter', False)
        super().__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['user'] = self.request.user
        context['filter_form'] = FilterTaskForm(self.request.GET or None)
        context['is_filter'] = self.is_filter
        context['linkFind'] = 'link-green'
        context['linkUpload']= 'link-grey'
        context['sizeOfName'] = 16

        if len(self.request.user.username) >=6:
            context['sizeOfName'] = 14


        return context

    def get_queryset(self,**kwargs):
        queryset = Task.objects.all().exclude(author=self.request.user.id)
        form = FilterTaskForm(self.request.GET)

        if form.is_valid():
            category = form.cleaned_data['category']
            price_min = form.cleaned_data['price_min']
            price_max = form.cleaned_data['price_max']
            order_by_time = form.cleaned_data['order_by_time']
            order_by_price = form.cleaned_data['order_by_price']
            query = form.cleaned_data['query']

            if category:
                queryset = queryset.filter(category=category)
                self.is_filter = True
            if price_min is not None:
                queryset = queryset.filter(price__gte=price_min)
                self.is_filter = True
            if price_max is not None:
                queryset = queryset.filter(price__lte=price_max)
                self.is_filter = True
            if order_by_time:
                queryset = queryset.order_by(order_by_time)
                self.is_filter = True
            if order_by_price:
                queryset = queryset.order_by(order_by_price)
                self.is_filter = True
            if query:
                queryset = queryset.filter(Q(title__icontains=query) | Q(description__icontains=query))
                self.is_filter = True

        return queryset




@csrf_protect
@login_required
def upload_task(request):
    user = request.user
    error_agreement = ""
    user_balance = get_user_model().objects.all().filter(username=user).values('balance').first()

    size_of_name_text = 16
    if len(user.username) > 6:
        size_of_name_text = 14

    if request.method == 'POST':
        tasks_form = TaskForm(request.POST)
        if tasks_form.is_valid():
            agreement_check_box = tasks_form.cleaned_data['isAgreed']
            if agreement_check_box:
                if float(tasks_form.cleaned_data['price']) <= float(user_balance['balance']):
                    task = tasks_form.save(commit=False)
                    task.author = request.user
                    task.save()
                    return HttpResponseRedirect(f'/tasks/my_tasks/{user.username}')
                else:
                    error_agreement = f"У вас недостаточно среств на балансе "
            else:
                error_agreement = "Вы объязаны согласиться с правилами сайта!"
    else:
        tasks_form = TaskForm()

    nav_status = ['nav-not-active', 'nav-active', 'nav-not-active', 'nav-not-active', 'nav-not-active']
    a_status = ['a-not-active', 'a-active', 'a-not-active', 'a-not-active', 'a-not-active']

    customs = {
        'user': user,
        'linkFind': 'link-grey',
        'linkUpload': 'link-green',
        'tasks_form':tasks_form,
        'error_agreement':error_agreement,
        'sizeOfName': size_of_name_text,
        'nav_status': nav_status,
        'a_status': a_status
    }
    return render(request,'tasks/upload.html',customs)


class MytasksView(LoginRequiredMixin,ListView):
    model = Task
    template_name = "tasks/mytasks.html"
    context_object_name = "my_tasks"
    paginate_by = 5

    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        query_set = Task.objects.all().filter(author=self.request.user.id)
        return query_set


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.kwargs['user_name_path']
        context['user'] = self.request.user
        context['linkFind'] = 'link-grey'
        context['linkUpload'] = 'link-grey'
        context['sizeOfName'] = 16
        context['nav_status'] =['nav-not-active', 'nav-active', 'nav-not-active', 'nav-not-active', 'nav-not-active']
        context['a_status'] = ['a-not-active', 'a-active', 'a-not-active', 'a-not-active', 'a-not-active']
        if len(self.request.user.username) >=6:
            context['sizeOfName'] = 14

        return context


@csrf_protect
@login_required
def delete_task(request,task_id):
    if(request.method == 'POST'):
        user = request.user
        task = get_object_or_404(Task, pk=task_id)
        if task.author == user:
            task.delete()
            return redirect('my_tasks',user.username)
        else:
            return redirect('my_tasks', user.username)





@csrf_protect
@login_required
def edit_task(request,task_id):
    task = get_object_or_404(Task, pk=task_id)
    user = request.user
    error_agreement = ""
    size_of_name_text = 16
    if len(user.username) > 6:
        size_of_name_text = 14


    if request.method == 'POST':
        form = EditTaskForm(request.POST, instance=task)
        if task.author == user:
            if form.is_valid():
                agreement_check_box = form.cleaned_data['isAgreed']
                if agreement_check_box:
                    task.save()
                    return redirect('my_tasks',user.username)
                else:
                    error_agreement = "Вы объязаны согласиться с правилами сайта!"
    else:
        form = EditTaskForm(instance=task)

    nav_status = ['nav-not-active', 'nav-active', 'nav-not-active', 'nav-not-active', 'nav-not-active']
    a_status = ['a-not-active', 'a-active', 'a-not-active', 'a-not-active', 'a-not-active']

    customs = {
    'user': user,
    'linkFind': 'link-grey',
    'linkUpload': 'link-green',
    'error_agreement': error_agreement,
    'sizeOfName': size_of_name_text,
    'nav_status': nav_status,
    'a_status': a_status,
    'task_id': task_id,
    'edit_form': form
    }

    return render(request,'tasks/edit_task.html', customs)


@csrf_protect
@login_required
def interact_task(request,task_id, first_id, second_id):
    user = request.user
    task = get_object_or_404(Task, pk=task_id)
    assignment_status = AssignedTask.objects.filter(task_id=task_id,user_id=user.pk).values('status').first()
    if assignment_status:
        if assignment_status['status'] == "Assigned":
            return redirect('task_chat_page', task_id, user.pk, second_id)
        elif assignment_status['status'] == "In Progress":
            return redirect('task_chat_page', task_id, user.pk, second_id)
        elif assignment_status['status'] == "Completed":
            return redirect("my_tasks",user.username)
    else:
        if request.method == 'POST':
            task_author_id = request.POST['task_author']
            AssignedTask.objects.create(task_id=int(task_id), status="Assigned", user_id=user.pk)
            Chat.objects.create(first_user_id=user.pk, second_user_id=int(task_author_id),task_id=int(task_id))

            return redirect('task_chat_page',task_id,user.pk,task_author_id)


    custom = {
        'linkFind': 'link-grey',
        'linkUpload': 'link-grey',
        'task_id': task_id,
        'task': task,
    }
    return render(request,'tasks/taskpage.html',custom)

@csrf_protect
@login_required
def task_chat_page(request,task_id,first_id,second_id):
    user = request.user
    task = get_object_or_404(Task, pk=task_id)
    chat = Chat.objects.filter(first_user_id=first_id,second_user_id=second_id)
    chat_id = chat[0].id
    user_db = get_user_model().objects.get(pk=second_id)
    user_avatar_url = user_db.photo.url if user_db.photo else 'static/default/default.jpg'
    messages = Message.objects.filter(chat_id=chat_id).order_by('date')

    if request.method == 'POST':
        report = request.POST['report']
        Message.objects.create(sender_id=user.pk,receiver_id=second_id,message=report,chat_id=chat_id)
        update_message = Chat.objects.get(id=chat_id)
        update_message.latest_message = report
        update_message.save(update_fields=['latest_message'])
        return redirect('task_chat_page', task_id, user.pk, second_id)
    custom = {
        'user': user,
        'linkFind': 'link-grey',
        'linkUpload': 'link-grey',
        'task_id': task_id,
        'task': task,
        'chat': chat,
        'first_id': first_id,
        'second_id': second_id,
        'messages': messages,
        'user_avatar_url': user_avatar_url,
    }


    return render(request,'tasks/task_chat.html',custom)

class MyTaskChatsView(LoginRequiredMixin,ListView):
    model = Chat
    template_name = 'tasks/my_tasks_chats.html'
    paginate_by = 13
    context_object_name = 'chats'

    def get_queryset(self):
        return Chat.objects.select_related('first_user', 'second_user').filter(second_user_id=self.request.user.pk)


    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.kwargs['user_name_path']
        context['user'] = self.request.user
        context['linkFind'] = 'link-grey'
        context['linkUpload'] = 'link-grey'
        context['sizeOfName'] = 16
        context['nav_status'] = ['nav-not-active', 'nav-active', 'nav-not-active', 'nav-not-active', 'nav-not-active']
        context['a_status'] = ['a-not-active', 'a-active', 'a-not-active', 'a-not-active', 'a-not-active']
        if len(self.request.user.username) >=6:
            context['sizeOfName'] = 14


        return context



def my_task_chat(request,task_id,first_id,second_id):
    user = request.user
    task = get_object_or_404(Task, pk=task_id)
    chat = Chat.objects.filter(first_user_id=first_id,second_user_id=user.pk)
    chat_id = chat[0].id
    user_from_db = get_user_model().objects.get(pk=first_id)
    avatar_url = user_from_db.photo.url if user_from_db.photo else '/static/default/default.jpg'
    messages = Message.objects.filter(chat_id=chat_id).order_by('date')
    if request.method == 'POST':
        report = request.POST['report']
        Message.objects.create(sender_id=user.pk,receiver_id=first_id,message=report,chat_id=chat_id)
        update_latest_message = Chat.objects.get(id=chat_id)
        update_latest_message.latest_message = report
        update_latest_message.save(update_fields=['latest_message'])
        return redirect('my_task_chat_page',task_id,first_id,second_id)

    nav_status = ['nav-not-active', 'nav-active', 'nav-not-active', 'nav-not-active', 'nav-not-active']
    a_status = ['a-not-active', 'a-active', 'a-not-active', 'a-not-active', 'a-not-active']

    size_of_name_text = 16
    if len(user.username) > 6:
        size_of_name_text = 14

    customs = {
        'user': user,
        'linkFind': 'link-grey',
        'linkUpload': 'link-green',
        'sizeOfName': size_of_name_text,
        'nav_status': nav_status,
        'a_status': a_status,
        'messages': messages,
        'task': task,
        'chat': chat,
        'avatar_url': avatar_url,
    }



    return render(request,'tasks/my_task_chat.html',customs)


def alter_value_assignment(request,task_id,first_id,second_id):
    if request.method == 'POST':
        value_action = request.POST['action']
        task_assign = AssignedTask.objects.get(task_id=task_id,user_id=second_id)

        if value_action == 'deny':
            task_assign.delete()
            return redirect('task_chat_page',task_id,first_id,second_id)
        elif value_action == 'submit':
            task_assign.status = "completed"
            task_assign.save(update_fields=['status'])
            return redirect('tasks')
        





