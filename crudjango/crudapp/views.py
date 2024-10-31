from django.shortcuts import render, redirect, get_object_or_404
from .models import BlogPost, Comment
from .forms import BlogPostForm, CommentForm

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

# Delete a blog post
def delete_blog(request, pk):
    blog = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        blog.delete()
        return redirect('blog_list')
    return render(request, 'persons/blog_confirm_delete.html', {'blog': blog})
