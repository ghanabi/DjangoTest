from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator
from django.views.generic import View
from .models import Blog
from .forms import BlogUpdate
from . import xhtml2pdf
# Create your views here.

def home(request):
    blogs = Blog.objects.order_by('-id')
    blog_list = Blog.objects.all().order_by('-id')
    paginator = Paginator(blog_list,3)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    return render(request,'home.html', {'blogs':blogs,'posts':posts})    

def detail(request, blog_id):
    blog_detail = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'detail.html', {'blog': blog_detail})
    #return render(request, 'detail.html')

def create(request):
    return render(request, 'create.html')

def postcreate(request):
    blog = Blog()
    blog.title = request.POST['title']
    blog.body = request.POST['body']
    blog.images = request.FILES['images']
    blog.pub_date = timezone.datetime.now()
    blog.save()
    return redirect('/crudapp/detail/' + str(blog.id))

def update(request, blog_id):
    blog = Blog.objects.get(id=blog_id)

    if request.method =='POST':
        form = BlogUpdate(request.POST)
        if form.is_valid():
            blog.title = form.cleaned_data['title']
            blog.body = form.cleaned_data['body']
            blog.pub_date=timezone.now()
            blog.save()
            return redirect('/crudapp/detail/' + str(blog.id))
    else:
        form = BlogUpdate(instance = blog)
 
        return render(request,'update.html', {'form':form})

def delete(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    blog.delete()
    return redirect('/')

def search(request):
    blogs = Blog.objects.all().order_by('-id')

    q = request.POST.get('q', "") 

    if q:
        blogs = blogs.filter(title__icontains=q)
        return render(request, 'search.html', {'blogs' : blogs, 'q' : q})
    
    else:
        return render(request, 'search.html')

def new(request):
    full_text = request.GET['fulltext']

    word_list = full_text.split()

    word_dictionary = {}

    for word in word_list:
        if word in word_dictionary:
            # Increase
            word_dictionary[word] += 1
        else:
            # add to the dictionary
            word_dictionary[word] = 1

    return render(request, 'new.html', {'fulltext': full_text, 'total': len(word_list), 'dictionary': word_dictionary.items()} )


# 리포팅 테스트 - PDF 만들기.
from django.http import HttpResponse
from reportlab.pdfgen import canvas
def some_view(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response

def test(request):
    blogs = Blog.objects.order_by('-id')
    today = timezone.now()
    params = {
        'today': today,
        'blogs': blogs,            
        'request': request
    }
    return render(request, 'test.html',params)

def test2(request):
    blogs = Blog.objects.order_by('-id')
    today = timezone.now()
    params = {
        'today': today,
        'blogs': blogs,            
        'request': request
    }
    return xhtml2pdf.render_pdf_view('test.html', params)
