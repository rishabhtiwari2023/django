from django.shortcuts import render
from .models import*
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
def get_student(request):

    queryset=Student.objects.all()
    if request.GET.get('search'):
        search=request.GET.get('search')
        queryset=queryset.filter(Q(student_name__icontains=search)|Q(department__department__icontains=search)
                                |Q(student_email__icontains=search))
    # posts = Post.objects.all()  # fetching all post objects from database
    p = Paginator(queryset, 10)  # creating a paginator object
    # getting the desired page number from url
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    return render(request,'student.html',{'queryset':page_obj})
# Create your views here.
