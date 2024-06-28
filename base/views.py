from django.http import HttpResponseForbidden
from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from .models import Dosen,Fakultas,Review,DosenGrade
from .forms import DosenForm,ReviewForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.http import JsonResponse
from django.core.paginator import Paginator


def landingPage(request):
    fakultass = Fakultas.objects.all().order_by('name')
    paginator = Paginator(fakultass, 6)  # Adjust number of items per page if necessary


    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'paginator': paginator,
        'page_number': page_number,
        'is_landing_page': True,
    }
    return render(request, "base/landingPage.html", context)

def home (request):
    if request.GET.get('q') != None:
        q = request.GET.get('q')
    else:
        q = ''

    dosens = Dosen.objects.filter(
        Q(fakultas__name__icontains=q) |
        Q(name__icontains=q)
        )
    
    paginator = Paginator(dosens, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    dosen_count = dosens.count()

    fakultass = Fakultas.objects.all().order_by('name')

    context = {
        'dosens':dosens,
        'fakultass' : fakultass, 
        'dosen_count':dosen_count,
        'page_obj': page_obj,
        'paginator': paginator,
        'page_number': page_number,
        }
    return render(request,"base/home.html",context )



def dosen (request, pk):
    dosen = Dosen.objects.get(id=pk)
    reviews = dosen.review_set.all().order_by('-updated')
    review_count = reviews.count()

    possible_grades = DosenGrade.objects.all()

    grade_counts = {}

    for grade in possible_grades:
        grade_count = reviews.filter(grade=grade).count()
        grade_counts[grade.name] = grade_count
    
    total_grades = sum(grade_counts.values())

    for grade in possible_grades:
        if total_grades > 0:
            percentage = (grade_counts[grade.name] / total_grades) * 100
        else:
            percentage = 0
        grade.percentage = percentage
        
    context = {
        'dosen': dosen,
        'reviews': reviews,
        'review_count': review_count,
        'grade_counts': grade_counts,
        'possible_grades': possible_grades,  # Pass the grades with updated percentages
        'total_grades': total_grades
        }
    return render(request,'base/dosen.html',context)

@login_required(login_url='account_login')
def createDosen(request):
    form = DosenForm()

    if request.method == 'POST':
        form = DosenForm(request.POST)
        if form.is_valid:
            dosen = form.save()
            return redirect('create-review',pk = dosen.id)

    context = {'form': form}
    return render(request, 'base/dosen_form.html', context)

@login_required(login_url='account_login')
def editDosen(request,pk):
    dosen = get_object_or_404(Dosen, id=pk)
    form = DosenForm(instance=dosen)

    # check if user is admin
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to perform this action.")

    if request.method == 'POST':
        form = DosenForm (request.POST, instance = dosen)
        if form.is_valid:
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request, 'base/dosen_form.html', context)


@login_required(login_url='account_login')
def deleteDosen(request,pk):

    if request.method == 'DELETE':
        dosen = get_object_or_404(Dosen,pk=pk)
        
        # check if user is admin
        if not request.user.is_staff:
            return JsonResponse({'success': False, 'error': 'You are not authorized to perform this action.'}, status=403)

        dosen.delete()
        return JsonResponse({'success':True})
    
    return JsonResponse({'success':False},status=400)
        


@login_required(login_url='account_login')
def createReview(request,pk):
    form = ReviewForm()
    dosen = Dosen.objects.get(id=pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.dosen = dosen
            review.save()

            # update dosen average rating
            avg_rating = dosen.review_set.aggregate(Avg('rating'))['rating__avg']
            dosen.rating = avg_rating
            dosen.save()

            return redirect('dosen', pk=dosen.id)
        else:
            for error in form.errors.values():
                messages.error(request, error)

    context ={'form':form,'dosen':dosen}
    return render(request, 'base/review_form.html', context)

@login_required(login_url='account_login')
def deleteReview(request, pk):
    if request.method == 'DELETE':
        review = get_object_or_404(Review, pk=pk)
        
        # Check if user is admin
        if not (request.user.is_staff or request.user == review.user):
            return JsonResponse({'success': False, 'error': 'You are not authorized to perform this action.'}, status=403)

        dosen = review.dosen
        review.delete()

        # Update the average rating for the dosen
        avg_rating = dosen.review_set.aggregate(Avg('rating'))['rating__avg']
        dosen.rating = avg_rating if avg_rating is not None else 0  # Handle the case where there are no reviews left

        # Update grade counts and percentages
        reviews = dosen.review_set.all()
        possible_grades = DosenGrade.objects.all()
        grade_counts = {grade.name: 0 for grade in possible_grades}

        for review in reviews:
            grade_counts[review.grade.name] += 1

        total_grades = sum(grade_counts.values())

        for grade in possible_grades:
            percentage = (grade_counts[grade.name] / total_grades) * 100 if total_grades > 0 else 0
            grade.percentage = percentage
            grade.save()  # Save the updated grade percentage

        dosen.save()

        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False}, status=400)


@login_required(login_url='account_login')
def editReview(request,pk):
    review = get_object_or_404(Review, id=pk)
    form = ReviewForm(instance=review)
    dosen = review.dosen

    # check if user is admin
    if not (request.user.is_staff or request.user == review.user):
        return HttpResponseForbidden("You are not authorized to perform this action.")

    if request.method == 'POST':
        form = ReviewForm (request.POST, instance = review)
        if form.is_valid:
            form.save()
            
            # Update dosen average rating
            avg_rating = dosen.review_set.aggregate(Avg('rating'))['rating__avg']
            dosen.rating = avg_rating
            dosen.save()

            return redirect('dosen',pk=dosen.id)

    context = {'form':form}
    return render(request, 'base/review_form.html', context)

@login_required
def dashboard(request):
    user = request.user
    reviews = Review.objects.filter(user=user)
    context={'user':user,'reviews':reviews}
    return render(request,'base/dashboard.html',context)