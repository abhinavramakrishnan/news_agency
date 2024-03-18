import requests
import json
from tabulate import tabulate

# Create a session object for making HTTP requests
session = requests.Session()

# Flag to track if the user is authenticated or not
authenticated = False

# Function to login to the system
def login(url):
    global authenticated
    # Prompt user for username and password
    username = input("Enter username: ")
    password = input("Enter password: ")

    try:
        # Send POST request to login API endpoint with provided credentials
        response = session.post(f"https://{url}/api/login/", data={'username': username, 'password': password})
        if response.status_code == 200:
            authenticated = True
            print(response.text)
        else:
            print(f"An error occurred while logging in: {response.text}")
    except Exception as e:
        print("An error occurred while making the request:", e)

# Function to logout from the system
def logout(url):
    # Send POST request to logout API endpoint
    response = session.post(f"https://{url}/api/logout/")
    print(response.text)

# Function to post a story to the system
def post_story(url):
    headline = input("Headline: ")
    category = input("Category: ")
    region = input("Region: ")
    details = input("Details: ")
    
    story_json = {
        "headline": headline,
        "category" : category,
        "region" : region,
        "details" : details
    }

    # Send POST request to stories API endpoint with story data in JSON format
    response = session.post(f"https://{url}/api/stories/", json=story_json)

    return response.text

# Function to retrieve stories based on filters
def get_stories(base_url, category_filter, region_filter, date_filter):
    # Send GET request to stories API endpoint with provided filters
    response = session.get(f"{base_url}/api/stories/", 
                            params={"story_cat" : category_filter,
                                  "story_region" : region_filter,
                                  "story_date" : date_filter
                                 })

    if response.status_code == 200:
        try:
            # Parse the JSON response
            data = response.json()
            stories = data.get('stories', [])

            if not stories:
                print("No stories found matching the filters.")
            else:
                # Prepare data for tabulate
                table_data = []
                for story in stories:
                    key = story.get('key')
                    headline = story.get('headline')
                    category = story.get('story_cat')
                    region = story.get('story_region')
                    author = story.get('author')
                    date = story.get('story_date')
                    details = story.get('story_details')
                    
                    table_data.append([key, headline, category, region, author, date, details])

                # Print stories in table format
                print(tabulate(table_data, headers=['Key', 'Headline', 'Category', 'Region', 'Author', 'Date', 'Details'], tablefmt='simple_grid'))

                
        except ValueError:
            print("Error parsing JSON response.")
    else:
        print(f"Error retrieving stories: {response.status_code}")

# Function to delete a story from the system
def delete_story(base_url, key):
    # Send DELETE request to stories API endpoint with provided story key
    response = session.delete(f"https://{base_url}/api/stories/{key}")
    return response.text

# Function to retrieve agencies from the system
def get_agencies():
    response = session.get("https://newssites.pythonanywhere.com/api/directory")

    if response.status_code == 200:
        try:
            data = response.json()
            if not data:
                return None
            else:
                return data
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            return None
    else:
        print(f"Error retrieving agencies: {response.text}")
        return None
    
# Function to list agencies
def list_agencies():
    data = get_agencies()
    if not data:
        print("No agencies found")
    
    agencies = []
    for agency in data:
        name = agency.get('agency_name')
        url = agency.get('url')
        code = agency.get('agency_code')
        agencies.append([name, url, code])

    print(tabulate(agencies, headers=["Name", "URL", "Code"], tablefmt="simple_grid"))
    
# Function to fetch news from all agencies or a specific agency
def all_news(category_filter, region_filter, date_filter):
    data = get_agencies()
    if not data:
        print("No agencies found")

    agencies_url = []
    for agency in data:
        name = agency.get('agency_name')
        url = agency.get('url')
        agencies_url.append([name, url])
    
    for agency in agencies_url:
        print(f"Stories from: {agency[0]}")
        get_stories(agency[1], category_filter, region_filter, date_filter)

# Function to fetch news from a specific agency
def collect_news(agency_id, category_filter, region_filter, date_filter):
    data = get_agencies()
    if not data:
        print("No agencies found")
    
    for agency in data:
        url = agency.get('url')
        code = agency.get('agency_code')
        if agency_id == code:
            get_stories(url, category_filter, region_filter, date_filter)
        

# Main function to execute the program
def main():
    print("|==================================|")
    print("| Abhinav Ramakrishnan News Agency |")
    print("|==================================|")

    base_url = None

    while True:
        global authenticated
        user_input = input("> ").strip().lower()
        while user_input == "":
            user_input = input("> ").strip().lower()

        # Split input into command and arguments
        command, *arguments = user_input.split()

        if (command == "login"):
            if len(arguments) != 1:
                print("Invalid number of arguments. Please try again")
            else:
                if base_url is None:
                    base_url = arguments[0]
                login(base_url)

        elif command == "list":
            list_agencies()

        elif command == "news":
            agency_id = None
            category_filter = "*"
            region_filter = "*"
            date_filter = "*"
            for arg in arguments:
                if arg.startswith("-id="):
                    agency_id = (arg.split('=')[1].strip('\"')).upper()
                if arg.startswith("-cat="):
                    category_filter = arg.split('=')[1].strip('\"')
                if arg.startswith("-reg="):
                    region_filter = arg.split('=')[1].strip('\"')
                if arg.startswith("-date="):
                    date_filter = arg.split('=')[1].strip('\"')

            if agency_id != None:
                collect_news(agency_id, category_filter, region_filter, date_filter)
            else:
                all_news(category_filter, region_filter, date_filter)

        
        elif authenticated:
            if command == "logout":
                logout(base_url)
            
            elif command == "post":
                post_story(base_url)
            
            elif command == "delete":
                if len(arguments) != 1:
                    print("Invalid number of arguments")
                else:
                    try:
                        key = int(arguments[0])
                        delete_story(base_url, key)
                    except ValueError:
                        print("Invalid key. Please provide a valid integer key.")
            
            elif command == "exit":
                break
            else:
                print("Invalid command. Please try again.")
        else:
            print("Please login first")

    session.close()

if __name__ == "__main__":
    main()
