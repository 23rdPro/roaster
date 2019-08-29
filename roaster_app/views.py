# from django.http import HttpResponse, HttpResponseRedirect
from django.db import models
from django.contrib import messages 
from django.shortcuts import render, redirect, get_object_or_404
# from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login
# from django.contrib.auth.decorators import user_passes_test

from django.views.generic import View

from electronic_roaster.utils import render_to_pdf 

# from django.template.loader import get_template



from roaster_app.forms import UserCreationForm, ChangeForm
from roaster_app.models import Profile


def welcome_page(request):
	if request.user.is_authenticated():
		title = 'Welcome'
		queryset = Profile.objects.all()

	else:

		title = 'Unauthenticated User'
		queryset = Profile.objects.all()

	context = {
		"title": title,
		"queryset": queryset,
	}
	return render(request, 'welcome.html', context)



def home_page_home(request):

	if request.method == "POST":
		form = UserCreationForm(request.POST or None)
		if form.is_valid():
			profile = form.save(commit=False)
			profile.save()
			username = request.POST['username']
			password = request.POST['password1']
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				url = redirect('welcome')
				return url
	else:
		form = UserCreationForm()
	context = {
		"form": form,
	}
	return render(request, 'home.html', context)

from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def admin_function(request):
	title = 'EDIT, DELETE, VIEW RECORD'
	# template = get_template('record.html')

	queryset = Profile.objects.all()
	paginator = Paginator(queryset, 10)

	page = request.GET.get('page')

	try:
		profile = paginator.page(page)
	except PageNotAnInteger:
		profile = paginator.page(1)
	except EmptyPage:
		profile = paginator.page(paginator.num_pages)

	context = {
		"title": title,
		"queryset": queryset,
		"profile": profile
	}

	return render(request, 'record.html', context)

@staff_member_required
def super_admin_list(request):
	title = 'EDIT, DELETE AND VIEW RECORDS'
	queryset = Profile.objects.all()
	paginator = Paginator(queryset, 10)

	page = request.GET.get('page')

	try:
		profile = paginator.page(page)
	except PageNotAnInteger:
		profile = paginator.page(1)
	except EmptyPage:
		profile = paginator.page(paginator.num_pages)

	context = {
		"title": title,
		"queryset": queryset,
		"profile": profile,
	}

	return render(request, 'super_admin_list.html', context)

def record_detail(request, id):
	instance = get_object_or_404(Profile, id=id)
	title = "USER DETAILS"
	template_name = 'record_detail.html'
	context = {
		"instance": instance,
		"title": title,
	}

	return render(request, template_name, context)

def delete_record(request, id):
	
	instance = get_object_or_404(Profile, id=id)
	instance.delete()
	title = 'Delete User'
	messages.success(request, "Successfully deleted", fail_silently=True)
	return redirect('super')
	
	# context = {
	# 	"instance": instance,
	# }
	
	# return render(request, 'delete_record.html', context)


def update_record(request, id):
	instance = get_object_or_404(Profile, id=id)
	template_name = 'update_record.html'
	form = ChangeForm(request.POST or None, instance=instance)
	if request.method == 'POST':
		if form.is_valid():
			form = form.save(commit=False)
			form.save()
			messages.success(request, "Successfully updated", fail_silently=True)
			return redirect('super')
	context = {
		"instance": instance,
		"form": form,
	}
	return render(request, template_name, context)



def get_pdf(request):
	results = Profile.objects.all()
    #Retrieve data or whatever you need
	return render_to_pdf(
		'pdf.html',
        {
            # 'pagesize':'A5',
            'mylist': results,
        }
    )































