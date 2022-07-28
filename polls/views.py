import imp
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.edit import CreateView
from django.contrib import messages
from .models import *
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

# Create your views here.

class MyAnswerDeleteView(DeleteView):
    model = QuestionsForm
    success_url = reverse_lazy('answers')
    template_name = "polls/delete.html"
    
    #customized method 'post' of DeleteView
    def post(self, request, *args, **kwargs):
        messages.success(request, f'Answer deleted!')
        return super().post(self, request, *args, **kwargs)


class MyQuestionsView(CreateView): #context - 'form.as_p'. In may case - custom form (polls/questions.html)
    model = QuestionsForm
    fields = ['color', 'car', 'beer', 'owner']

    #customized method 'post' of CreateView
    def post(self, request):
        messages.success(request, f'Answer received!')
        return super().post(self, request)


#var context_object_name - to cahnge default "object_list" name to custom name
class MyQuestionsListView(ListView): #context - 'object_list'
    model = QuestionsForm
    template_name = "polls/answers.html" 
    

class MyAnswersView(DetailView): #class object in context - "object"
    model = QuestionsForm
    template_name = "polls/detail.html"
