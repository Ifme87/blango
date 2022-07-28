from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.edit import CreateView
from django.contrib import messages
from .models import *
from django.urls import reverse_lazy

# Create your views here.



class MyAnswerDeleteView(DeleteView):
    model = QuestionsForm
    success_url = reverse_lazy('answers')
    template_name = "polls/delete.html"

#checks if user is ok and login
class MyQuestionsView(CreateView): 
    model = QuestionsForm
    fields = ['color', 'car', 'beer', 'owner']
    def post(self, request):
        messages.success(request, f'Answer received!')
        return super().post(self, request)

#generates 'object_list' for use in templates (see in polls/answers.html)
#var context_object_name - to cahnge default "object_list" name to custom name
class MyQuestionsListView(ListView):
    model = QuestionsForm
    template_name = "polls/answers.html" 
    

class MyAnswersView(DetailView):
    model = QuestionsForm
    template_name = "polls/detail.html"
