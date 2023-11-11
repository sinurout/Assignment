from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import StudentForm
from .models import Student 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Student
from .models import StudentSerializer



def create_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            stud = Student.objects.all()
            form.save()
            redirect_url = f'/student-details/?page={1}'
            
            return redirect(redirect_url)
        else:
            return JsonResponse({'error': 'Invalid data'})
    else:
        form = StudentForm()
        stud = Student.objects.all().order_by('-roll_no')
        return render(request, 'home.html', {'form': form, 'stu': stud})
def student_Details(request):
    # Get the page number from the request's GET parameters, default to 1 if not specified
    page = request.GET.get('page', 1)

    # Get the sorting criteria from the request's GET parameters, default to 'name' if not specified
    sort_criteria = request.GET.get('sort', 'name')

    # Query all students
    all_students = Student.objects.all()

    # Sort students based on the selected criteria
    if sort_criteria == 'name':
        all_students = all_students.order_by('name')
    elif sort_criteria == 'roll_no':
        all_students = all_students.order_by('roll_no')
    elif sort_criteria == 'subject1':
        all_students = all_students.order_by('-score1')
    elif sort_criteria == 'subject2':
        all_students = all_students.order_by('-score2')
    elif sort_criteria == 'subject3':
        all_students = all_students.order_by('-score3')
    elif sort_criteria == 'subject4':
        all_students = all_students.order_by('-score4')
    elif sort_criteria == 'subject5':
        all_students = all_students.order_by('-score5')
    

    # Set the number of students per page
    students_per_page = 10  # You can adjust this number based on your preference

    # Use Django's Paginator to paginate the student list
    paginator = Paginator(all_students, students_per_page)

    try:
        # Get the current page
        students = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page.
        students = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver the last page of results.
        students = paginator.page(paginator.num_pages)

    return render(request, 'studentDetails.html', {'stu': students})


class GetStudentsView(generics.ListAPIView):
    serializer_class = StudentSerializer

    def get_queryset(self):
        class_filter = self.request.query_params.get('class', None)

        
        data_selection = self.request.query_params.get('data', None)
        if data_selection:
            fields = data_selection.split(',')
            # Include 'total_score' in fields only if it's explicitly requested
            if 'total_score' not in fields:
                fields.append('total_score')
            self.serializer_class.Meta.fields = fields
        else:
            # If 'data' parameter is not provided, use all fields
            self.serializer_class.Meta.fields = '__all__'

      
        queryset = Student.objects.all()
        if class_filter:
            queryset = queryset.filter(class_level=class_filter)

        # Calculate the combined score for each student
        queryset = sorted(queryset, key=lambda student: sum([
            student.score1, student.score2, student.score3, student.score4, student.score5
        ]), reverse=True)

        return queryset

