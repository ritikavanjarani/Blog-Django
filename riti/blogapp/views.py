from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db import connection
# Create your views here.

def home(request):
    
    cursor = connection.cursor()
    cursor.execute("SELECT * from post where softdelete = 0")
    columns = [col[0] for col in cursor.description]
    posts =  [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
    print(posts)
    context = {
        'keyposts': posts
    }
    return render(request,'blogapp/home.html',context)

def create(request):
    return render(request,'blogapp/form.html')

def insert(request):
    title = request.POST['blogTitle']
    content = request.POST['content']
    cursor = connection.cursor()
    cursor.execute("INSERT INTO post (`title`,`content`) VALUES ( %s, %s );", (title, content))
    cursor = connection.cursor()
    cursor.execute("SELECT * from post where softdelete = 0")
    return redirect('/blog/home')

def edit(request, pk):
    cursor = connection.cursor()
    cursor.execute(f"SELECT * from post where id={pk} and  softdelete = 0 ")
    columns = [col[0] for col in cursor.description]
    posts =  [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
    print(posts)
    context = {
        'keyposts': posts[0]
    }
    return render(request, 'blogapp/editform.html', context)

def update(request):
    title = request.POST['blogTitle']
    content = request.POST['content']
    id = request.POST['id']
    cursor = connection.cursor()
    cursor.execute("UPDATE post set title = %s, content=%s where id=%s",(title,content,id))
    cursor = connection.cursor()
    cursor.execute("SELECT * from post where softdelete = 0")
    return redirect('/blog/home')

def delete(request,pk):
   
    
    cursor = connection.cursor()
    cursor.execute(f"UPDATE post set softdelete = 1 where id={pk}")
    cursor = connection.cursor()
    
    return redirect('/blog/home')
 