from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Category, Photo, Blog, Comment, ContactMessage


def home(request):
    categories = Category.objects.all()
    blogs = Blog.objects.all().order_by('-created')[:3]

    return render(request, 'index.html', {
        'categories': categories,
        'blogs': blogs
    })


def category_gallery(request, slug):
    category = get_object_or_404(Category, slug=slug)
    photos = Photo.objects.filter(category=category)

    return render(request, 'category_gallery.html', {
        'category': category,
        'photos': photos
    })


def blog_detail(request, id):
    blog = get_object_or_404(Blog, id=id)

    # Only approved top-level comments
    comments = Comment.objects.filter(
        blog=blog,
        parent=None,
        approved=True
    ).order_by('-created')

    success = False
    error = ""

    if request.method == "POST":
        name = request.POST.get('name')
        message = request.POST.get('message')
        parent_id = request.POST.get('parent_id')

        parent = None
        if parent_id:
            parent = Comment.objects.get(id=parent_id)

        if name and message:
            Comment.objects.create(
                blog=blog,
                name=name,
                message=message,
                parent=parent
            )
            success = True  # ✅ FIXED
        else:
            error = "Please enter your name and comment."

    return render(request, 'blog_detail.html', {
        'blog': blog,
        'comments': comments,
        'success': success,
        'error': error
    })


def like_blog(request, id):
    blog = Blog.objects.get(id=id)
    blog.likes += 1
    blog.save()
    return JsonResponse({'likes': blog.likes})

def home(request):
    categories = Category.objects.all()
    blogs = Blog.objects.all().order_by('-created')[:3]

    contact_success = False
    contact_error = ""

    if request.method == "POST":
        form_type = request.POST.get('form_type')

        if form_type == "contact":
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            project_type = request.POST.get('project_type')
            message = request.POST.get('message')

            if first_name and email and message:
                ContactMessage.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    project_type=project_type,
                    message=message
                )
                contact_success = True
            else:
                contact_error = "Please enter your first name, email, and message."

    return render(request, 'index.html', {
        'categories': categories,
        'blogs': blogs,
        'contact_success': contact_success,
        'contact_error': contact_error
    })