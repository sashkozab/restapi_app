from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, Http404


from django.db.models import Q
from .models import Post
from .forms import PostForm
from accounts.models import MyUser

def home(request):
    today = timezone.now().date()
    queryset_list = Post.objects.all() #.order_by("-timestamp")
    queryset_list_accounts = MyUser.objects.all()
    print("queryset_list_accounts: ", queryset_list_accounts)
    print("queryset_list: ", queryset_list)
    all_emails = MyUser.objects.values_list('email', flat=True)

    print(all_emails)
    [print(obj.user_id) for obj in queryset_list]
    
    query = request.GET.get("q")
    query_author = request.GET.get("author")
    if query:
        queryset_list = queryset_list.filter(
                Q(title__icontains=query)|
                Q(content__icontains=query)
                ).distinct()

    print(queryset_list)
    if query_author:
        particular_email = MyUser.objects.get(email = query_author)
        particular_email_id = particular_email.id
        post_objects = Post.objects.filter(user_id = particular_email_id)
        queryset_list = post_objects
    paginator = Paginator(queryset_list, 5) # Show 5 contacts per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    [print(obj.user.__class__) for obj in queryset]

    context = {
        "object_list": queryset, 
        "authors_list": all_emails,
        "page_request_var": page_request_var,
        "today": today,
    }
    return render(request, "home.html", context)

def post_create(request):
    if not request.user.is_authenticated:
        raise Http404
        
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        # message success
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form,
    }
    return render(request, "post_form.html", context)

def post_detail(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    queryset_list = Post.objects.all()
    context = {
        "title": instance.title,
        "instance": instance,
        "full_object_list" : queryset_list,
    }
    return render(request, "post_detail.html", context)

def post_update(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    if request.user.is_authenticated and request.user != instance.user:
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Item Saved", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": instance.title,
        "instance": instance,
        "form":form,
    }
    return render(request, "post_form.html", context)



def post_delete(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    if request.user.is_authenticated and request.user != instance.user:
        raise Http404
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("home")