Pastebin Lite
--
A Django based prototype developed to get a better sense for the framework and language. 
This readme serves as a documentation on my journey as a newbie at Python and Django to learn and improve my knowledge on the language and framework  
Feel free to perform a code review and inform me of any code smells and best practices i should know about through the issues !     

User Stories
--
- [x] User that visits the root URL should be able to write some text/code. 
- [x] User should be able to set a title for the paste
- [x] User should be able to set an expiry date for the paste
- [x] User should be able save the paste
- [x] Once paste is saved, user should be redirected to the paste view with the special randomly generated url unique to the paste 
- [x] Any user that visits the special URL should be able to see the paste
- [x] Any user that visits the special URL should be able to delete it (no auth)
- [x] User should be able to search any paste in the application
- [x] User should be redirected to a results page once they enter a search query
- [x] User should not be able to view the paste after expiry date
- [x] When a unique user visits a paste, their details will be logged as a hit to the paste
- [x] When a user visits the special URL, they should be able to view paste details including how many hits 

To-do's in progress
--
- [ ] Learn to write unit test in Django
- [ ] Learn to implement caching to improve performance

Starting the development web server
--
Run the following command to run the web application on 127.0.0.1:8000, which is also the URL you'll need to enter into your web browser in order to access the site. Feel free to change the address and/or port depending on your working environment.

```python manage.py runserver 127.0.0.1:8000```

Try opening http://127.0.0.1:8000 in your web browser. If everything worked out correctly, you should now be able to use the web application as normal.

