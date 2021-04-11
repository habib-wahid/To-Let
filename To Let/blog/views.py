from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
     ListView,
     DetailView,
     CreateView,
     UpdateView,
     DeleteView
)
from django.http import HttpResponse
from .models import Post

"""
posts = [
    {
        'owner': 'Gourab Saha',
        'location': 'Sylhet',
        'content': 'Hostel',
        'date_posted': '1 December,2020'
    },
    {
        'owner': 'Sourav Saha',
        'location': 'Gopalganj',
        'content': 'Family House',
        'date_posted': '31 December,2020'
    },
    {
        'owner': 'Md. Habib',
        'location': 'BBaria',
        'content': 'Ladies Hostel',
        'date_posted': '1 December,2021'
    }
]

"""
def home(request):
    context ={
#        'posts': posts
         'posts': Post.objects.all()

    }
    return render (request ,'blog/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5


    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(owner=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['location','content']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin,  UpdateView):
    model = Post
    fields = ['location','content']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.owner:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.owner:
            return True
        return False



def about(request):
    return render (request, 'blog/about.html', {'title': 'About'})
