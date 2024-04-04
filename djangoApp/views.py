#views.py
import boto3
from django.conf import settings
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from .filters import *
import logging
from django.core.cache import cache

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')



# Create your views here.
@login_required
def serve_presigned_media(request, file_key):
    if not file_key.startswith('media/'):
        file_key = f'media/{file_key}'
    logging.debug(f'Received file key: {file_key}')
    print("Generating pre-signed URL for key:", file_key)
    """Serve a pre-signed URL for authenticated users."""
    cache_key = f'presigned_url_{file_key}'
    presigned_url = cache.get(cache_key)

    if not presigned_url:
       
      s3_client = boto3.client('s3', 
                              region_name=settings.AWS_S3_REGION_NAME,
                              aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
      )
    
      try:
         presigned_url = s3_client.generate_presigned_url('get_object',
                                                         Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                                                                 'Key': file_key},
                                                         ExpiresIn=3600)
         cache.set(cache_key, presigned_url, timeout=3500) 
         logging.debug(f'Generated presigned URL: {presigned_url}')
      except Exception as e:
        logging.error(f'Error generating presigned URL: {e}')
        # Log the error
        raise Http404("Error generating URL")

    # Redirect to the pre-signed URL
    return redirect(presigned_url)

def home(request):
   return render(request,'djangoApp/home.html')

@login_required(login_url='loginpage')
def trainingjournal(request):
   current_user= request.user
   journalentry = TrainingLogEntry.objects.filter(user=current_user)
   jFilter = TrainingLogFilter(request.GET, queryset=journalentry)
   journalentry= jFilter.qs
   context = {'jFilter': jFilter, 'journalentry':journalentry}
   return render(request, 'djangoApp/trainingjournal.html', context) 

@login_required(login_url='loginpage')
def techniquelibrary(request):
   current_user=request.user
   techniqueentry = TechniqueLibraryEntry.objects.filter(user=current_user)
   tFilter = TechniqueLibraryFilter(request.GET, queryset=techniqueentry)
   techniqueentry = tFilter.qs
   context = {'tFilter': tFilter, 'techniqueentry': techniqueentry}
   return render(request, 'djangoApp/techniquelibrary.html', context)

def loginpage(request):
   if request.user.is_authenticated:
      return redirect('home')
   else:

      if request.method == 'POST':
         username = request.POST.get('username')
         password = request.POST.get('password')
         user= authenticate(request, username=username, password=password)
         if user is not None:
            login(request, user)
            return redirect('home')
         else:
            messages.info(request,'Username or Password is incorrect.')
            
      context = {} 
      return render(request,'djangoApp/loginpage.html', context)

def logoutuser(request):
   logout(request)
   return redirect ('loginpage')

def registerpage(request):
   if request.user.is_authenticated:
      return redirect('home')
   else:
      form = CreateUserForm()
      if request.method == 'POST':
         form = CreateUserForm(request.POST)
         if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect ('loginpage')

      context = {'form':form}
      return render(request, 'djangoApp/registerpage.html', context)
   
@login_required(login_url='loginpage')
def journalform(request):
   form = JournalForm()
   if request.method== 'POST':
      form= JournalForm(request.POST, request.FILES, user=request.user)
      if form.is_valid():
         form.save()
         return redirect('trainingjournal')
   else:
      form =JournalForm(user=request.user)
   context = {'jform': form }
   return render(request, 'djangoApp/journalform.html', context)

@login_required(login_url='loginpage')
def techniqueform(request):
   form = TechniqueForm()
   if request.method == 'POST':
      form = TechniqueForm(request.POST, request.FILES, user=request.user)
      if form.is_valid():
         form.save()
         return redirect('techniquelibrary')
   else:
      form = TechniqueForm(user=request.user) 
   context = {'tform':form}
   return render(request, 'djangoApp/techniqueform.html', context)
   
@login_required(login_url='loginpage')
def updatejournal(request, pk):
   journalentry = TrainingLogEntry.objects.get(id=pk)
   form = JournalForm(instance=journalentry)
   if request.method== 'POST':
         form= JournalForm(request.POST, request.FILES, instance=journalentry)
         if form.is_valid():
            form.save()
            return redirect('trainingjournal')
   else:
      form = JournalForm(instance=journalentry, user=request.user)
   context={'jform':form}
   return render (request, 'djangoApp/journalform.html', context)

@login_required(login_url='loginpage')
def updatetechnique(request, pk):
   techniqueentry = TechniqueLibraryEntry.objects.get(id=pk)
   form = TechniqueForm(instance=techniqueentry)
   if request.method== 'POST':
         form= TechniqueForm(request.POST, request.FILES, instance=techniqueentry)
         if form.is_valid():
            form.save()
            return redirect('techniquelibrary')
   else: 
      form = TechniqueForm(instance=techniqueentry, user=request.user)
   context={'tform':form}
   return render (request, 'djangoApp/techniqueform.html', context)

def deletejournal(request, pk):
   journalentry = TrainingLogEntry.objects.get(id=pk)
   if request.method == 'POST':
      journalentry.delete()
      return redirect ('trainingjournal')
   context = {'journalentry': journalentry}
   return render (request, 'djangoApp/deletejournal.html', context)

def deletetechnique(request, pk):
   techniqueentry = TechniqueLibraryEntry.objects.get(id=pk)
   if request.method == 'POST':
      techniqueentry.delete()
      return redirect ('techniquelibrary')
   context = {'techniqueentry': techniqueentry}
   return render (request, 'djangoApp/deletetechnique.html', context)

@login_required(login_url='loginpage')
def techniqueseries(request):
    current_user = request.user
    series_entries = TechniqueSeriesEntry.objects.filter(user=current_user)
    context = {'series_entries': series_entries}
    return render(request, 'djangoApp/techniqueseries.html', context)

@login_required(login_url='loginpage')
def techniqueseriesform(request):
    if request.method == 'POST':
        form = TechniqueSeriesForm(request.POST, request.FILES)
        if form.is_valid():
            series_entry = form.save(commit=False)
            series_entry.user = request.user
            series_entry.save()
            form.save_m2m()  # Save the form's many-to-many data
            return redirect('techniqueseries')
    else:
        form = TechniqueSeriesForm()
    context = {'jform': form}
    return render(request, 'djangoApp/techniqueseriesform.html', context)

@login_required(login_url='loginpage')
def updatetechniqueseries(request, pk):
    series_entry = TechniqueSeriesEntry.objects.get(id=pk, user=request.user)
    if request.method == 'POST':
        form = TechniqueSeriesForm(request.POST, request.FILES, instance=series_entry)
        if form.is_valid():
            form.save()
            return redirect('techniqueseries')
    else:
        form = TechniqueSeriesForm(instance=series_entry)
    context = {'jform': form}
    return render(request, 'djangoApp/techniqueseriesform.html', context)

@login_required(login_url='loginpage')
def deletetechniqueseries(request, pk):
    series_entry = TechniqueSeriesEntry.objects.get(id=pk, user=request.user)
    if request.method == 'POST':
        series_entry.delete()
        return redirect('techniqueseries')
    context = {'series_entry': series_entry}
    return render(request, 'djangoApp/deletetechniqueseries.html', context)
