# Import necessary modules and functions from Django
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout

# Import the Story model
from .models import Story

# Import module for processing JSON payload
import json
# Import date and time module
from datetime import datetime


# Create your views here.
@csrf_exempt
def Login(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            return HttpResponse("Already logged in", status=200, reason="OK")
        else:
            username = request.POST.get('username')
            password = request.POST.get('password')

            if not username or not password:
                return HttpResponse("Username and password are required", status=401, reason="Unauthorized")
            else:
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return HttpResponse("Welcome!", status=200, reason="OK")
                else:
                    return HttpResponse("Username or password incorrect", status=401, reason="Unauthorized")
    else:
        return HttpResponse("Request not allowed", status=405, reason="Method Not Allowed")

@csrf_exempt
def Logout(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            logout(request)
            return HttpResponse("Goodbye!", status=200, reason="OK")
        else:
            return HttpResponse("Not logged in", status=403, reason="Forbidden")
    else:
        return HttpResponse("Reqeust not allowed", status=405, reason="Method Not Allowed")
    
@csrf_exempt
def Stories(request):
    # User tries to post a story
    if (request.method == 'POST'):
        # Ensure user is logged in
        if request.user.is_authenticated:
            # Read the JSON payload from the request body
            data = json.loads(request.body)
            
            # Unpack the data into appropirate variables
            headline = data.get('headline')
            category = data.get('category')
            region = data.get('region')
            details = data.get('details')

            # Add the story to the database
            try:
                Story.objects.create(
                    headline=headline,
                    category=category,
                    region=region,
                    details=details,
                    author=request.user.author,
                    date=datetime.now().date(),
                    time=datetime.now().time()
                )
                return HttpResponse("Story posted", status=201, reason="CREATED")
            # Handle the exception
            except Exception as e:
                return HttpResponse(f"Error: {e}", status=503, reason="Service Unavailable")
        else:
            return HttpResponse("Not logged in", status=403, reason="Forbidden")
        
    # User tries to get a story
    elif request.method == 'GET':
        # Unpack the data into appropirate variables
        category_filter = request.GET.get('story_cat')
        region_filter = request.GET.get('story_region')
        date_filter = request.GET.get('story_date')

        # Define filters as a dictionary
        filters = {}

        if (category_filter!="*"):
            filters['category'] = category_filter
        if (region_filter!="*"):
            filters['region'] = region_filter
        if (date_filter!="*"):
            # Convert the input date into the correct format to search the database
            formatted_date = datetime.strptime(date_filter, "%d/%m/%Y").date()
            filters['date__gte'] = formatted_date

        stories_qs = Story.objects.filter(**filters)
    
        stories_list = list(stories_qs.values())

        stories_labeled = []
        for record in stories_list:
            story = {
                'key' : record.get('id'),
                'headline' : record.get('headline'),
                'story_cat' : record.get('category'),
                'story_region' : record.get('region'),
                'author' : record.get('author_id'),
                'story_date' : record.get('date'),
                'story_details' : record.get('details')
            }
            stories_labeled.append(story)

        # Create a dictionary containing the list of stories
        stories_json = {
            'stories': stories_labeled
        }
        return JsonResponse(stories_json, status=200)        


@csrf_exempt
def Delete(request, key):
    # User tries to delete a story
    if request.method == 'DELETE':
        # Ensure user is logged in
        if request.user.is_authenticated:
            story = Story.objects.get(pk=key)
            story.delete()
            return HttpResponse("Story deleted", status=200, reason="OK")
        else:
            return HttpResponse("Not logged in", status=403, reason="Forbidden")
    else:
        return HttpResponse("Reqeust not allowed", status=405, reason="Method Not Allowed")
