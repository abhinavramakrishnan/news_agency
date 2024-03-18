Abhinav Ramakrishnan News Agency Client
---------------------------------------

I. Instructions for Using the Client:
   This client allows you to interact with the Abhinav Ramakrishnan News Agency system through a command-line interface. 
   Below are the available commands and their usage:

   1. login <domain_name>
      - Use this command to log in to the news agency system. Replace <domain_name> with the domain name of the service.
      Example: login sc15xyz.pythonanywhere.com

   2. list
      - Lists all available news agencies along with their URLs and codes.

   3. news [-id=<agency_code>] [-cat=<category>] [-reg=<region>] [-date=<date>]
      - Retrieves news stories based on specified filters. You can provide optional filters to narrow down the search:
        -id: Filter by agency code (optional).
        -cat: Filter by category (optional).
            - pol = Politics
            - tech = Technology
            - art = Art
            - trivia = Trivial
        -reg: Filter by region (optional).
            - uk = United Kingdom
            - eu = Europe
            - w = World
        -date: Filter by date, format dd/mm/yyyy (optional).
      Example: news -id="JAD05" -cat="tech" -reg="uk" -date="12/02/2019"

   4. logout
      - Logs out from the news agency system.

   5. post
      - Posts a new story to the news agency system. 
      You will be prompted to provide details such as headline, category, region, and details.

   6. delete <story_key>
      - Deletes a story from the news agency system. Replace <story_key> with the key of the story to be deleted.

   7. exit
      - Exits the client application.

II. PythonAnywhere Domain:
    Domain: sc21a2r.pythonanywhere.com

III. Password for Module Leader's Admin Account:
     Password: ammar123

IV. Additional Information:
    - Ensure you install the modules in the requirements.txt as the client has some external modules to help with
      table generation.
