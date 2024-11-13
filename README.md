# Building a CRUD (Create, Retrieve, Update and Delete) Blog Project in Django

Django is a powerful Python web framework that simplifies web development by providing a clean and pragmatic design. One of the most common tasks in web development is creating CRUD (Create, Read, Update, Delete) functionality for your application. In this article, we'll explore how to create a Django CRUD project using function-based views.

### Prerequisites

Before we dive into building our CRUD project, make sure you have the following prerequisites in place:

1. Python and Django: Ensure you have Python installed on your system. You can install Django using pip:
```python
pip install django
```

2. Database: Decide on the database you want to use. By default, Django uses SQLite, but you can configure it to use other databases like PostgreSQL, MySQL, or Oracle.

3. Text Editor or IDE: Choose a code editor or integrated development environment (IDE) of your preference. Popular choices include Visual Studio Code, PyCharm, or Sublime Text.

### Setting Up Your Django Project

Let's start by creating a new Django project and a new app within that project. Open your terminal and run the following commands:

```python
django-admin startproject crudjango
cd crudjango
python manage.py startapp crudapp
```

We've created a new project named "crudjango" and an app named "crudapp."

### Application Registration: you need to configure in your settings.py file

Make sure your app is included in the INSTALLED_APPS list:

```python
INSTALLED_APPS = [
    # ...
    'crudapp',
]
```

### Defining Models

In Django, models are Python classes that define the structure of your database tables. For our CRUD project, let's assume we want to manage a list of orders. Create a model for the orders in `crudapp/models.py`:

```python
from django.db import models

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=100)
    published_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)

class Comment(models.Model):
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

```

Now, it's time to create the database tables for our models. Run the following commands to create the migrations and apply them:

```python
python manage.py makemigrations
python manage.py migrate
```

###  Creating Forms

We mentioned using a form for creating and updating orders. You can define the form in `crudapp/forms.py`:

```python
from django import forms
from .models import BlogPost, Comment

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'author', 'image']
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'content']
```

### Creating Function-Based Views

Function-based views are a simple and straightforward way to handle CRUD operations in Django. In this example, we'll create views for creating, reading, updating, and deleting orders.

1. Create a Order (Create View)
In `crudapp/views.py`, define a view function for creating a new Blog:

```python
from django.shortcuts import render, redirect, get_object_or_404
from .models import BlogPost, Comment
from .forms import BlogPostForm, CommentForm

# Create a new blog post
def create_blog(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)  # Add request.FILES here
        if form.is_valid():
            form.save()
            return redirect('blog_list')
    else:
        form = BlogPostForm()
    return render(request, 'persons/blog_form.html', {'form': form})
```

In this view, we handle both GET and POST requests. If it's a GET request, we render a form for creating a new order. If it's a POST request, we validate the form data and save the new order if it's valid.

2. Read Blogs (List View)
Now, let's create a view to display a list of all books in `crudapp/views.py`:

```python
# List all blog posts
def blog_list(request):
    blogs = BlogPost.objects.all()
    return render(request, 'persons/blog_list.html', {'blogs': blogs})

def blog_detail(request, pk):
    blog = get_object_or_404(BlogPost, pk=pk)
    comments = blog.comments.all()
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.blog_post = blog
            new_comment.save()
            return redirect('blog_detail', pk=blog.pk)
    else:
        comment_form = CommentForm()
    
    return render(request, 'persons/blog_detail.html', {
        'blog': blog,
        'comments': comments,
        'comment_form': comment_form,
    })
```

This view retrieves all orders from the database and renders them using a template.

3. Update a View (Update Blog)
To update a Blog, create a view in `crudapp/views.py`:

```python
# Update an existing blog post
def update_blog(request, pk):
    blog = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=blog)  # Add request.FILES here
        if form.is_valid():
            form.save()
            return redirect('blog_list')
    else:
        form = BlogPostForm(instance=blog)
    return render(request, 'persons/blog_form.html', {'form': form})
```

4. Delete a Order (Delete Blog)
Finally, let's create a view to delete a order in `crudapp/views.py`:

```python
# Delete a blog post
def delete_blog(request, pk):
    blog = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        blog.delete()
        return redirect('blog_list')
    return render(request, 'persons/blog_confirm_delete.html', {'blog': blog})
```

In this view, we confirm the order deletion with a confirmation page.

### Creating Templates
Now, create HTML templates for the views in the crudproject/templates/persons directory. You'll need templates for the following views:

blog_form.html: For the create and update forms.
blog_list.html: For creating and listing all blogs.
blog_detail.html: For reading the details of the blogs.
blog_confirm_detail.html: For confirming blog deletion.

 Below, are the templates as we discussed earlier: 

 ```

`crudproject/templates/persons/blog_list.html`

 ```html
<button>
<a href="{% url 'create_blog' %}">Create New Blog Post</a>
</button>

<ul>
    {% for blog in blogs %}
        <li>
            <!-- Link to the blog post detail page -->
            <h3><a href="{% url 'blog_detail' blog.pk %}">{{ blog.title }}</a> by {{ blog.author }}</h3>
            
            {% if blog.image %}
                <img src="{{ blog.image.url }}" alt="{{ blog.title }}" style="width: 100px; height: auto;">
            {% endif %}
            
            <!-- Display a short preview of the content -->
            <p>{{ blog.content|truncatewords:20 }}</p>
            
            <!-- Edit and Delete links for each blog post -->
            <a href="{% url 'update_blog' blog.pk %}">Edit</a> |
            <a href="{% url 'delete_blog' blog.pk %}">Delete</a>
        </li>
    {% endfor %}
</ul>
 ```

`crudproject/templates/persons/blog_form.html`

 ```html
<center>
<h2>{% if form.instance.pk %}Edit Blog Post{% else %}New Blog Post{% endif %}</h2>
<form method="post" enctype="multipart/form-data">  <!-- Add enctype here -->
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Save</button>
</form>
<a href="{% url 'blog_list' %}">Back to Blog List</a>
 </center>
 ```

 `crudproject/templates/persons/blog_detail.html`

```html
<h2>{{ blog.title }}</h2>
<p>By {{ blog.author }} on {{ blog.published_date }}</p>
{% if blog.image %}
    <img src="{{ blog.image.url }}" alt="{{ blog.title }}" style="width: 300px; height: auto;">
{% endif %}
<p>{{ blog.content }}</p>

<h3>Comments</h3>
<ul>
    {% for comment in comments %}
        <li>
            <strong>{{ comment.name }}</strong> on {{ comment.created_date }}:
            <p>{{ comment.content }}</p>
        </li>
    {% empty %}
        <li>No comments yet.</li>
    {% endfor %}
</ul>

<h3>Add a Comment</h3>
<form method="post">
    {% csrf_token %}
    {{ comment_form.as_p }}
    <button type="submit">Submit Comment</button>
</form>
<a href="{% url 'blog_list' %}">Back to Blog List</a>

```

 `crudproject/templates/persons/blog_confirm_delete.html`

```html
<center>
<h2>Delete Blog Post</h2>
<p>Are you sure you want to delete "{{ blog.title }}" by {{ blog.author }}?</p>
<form method="post">
    {% csrf_token %}
    <button type="submit">Yes, delete</button>
    <a href="{% url 'blog_list' %}">Cancel</a>
</form>
</center>

```


### Wiring Up URLs

Finally, configure the URLs for your views. In your project's crudproject/urls.py file, include the URLs for the crudapp app:


```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('crudapp.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

Then, in your app's crudpp/urls.py file, define the URLs for your views:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('blog/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('create/', views.create_blog, name='create_blog'),
    path('update/<int:pk>/', views.update_blog, name='update_blog'),
    path('delete/<int:pk>/', views.delete_blog, name='delete_blog'),
]
```

### Testing Your CRUD Project

With everything set up, you can start your Django development server:

```python
python manage.py runserver
```

Visit http://localhost:8000/ in your browser, and you should be able to create, read, update, and delete blogs in your Django CRUD project.
