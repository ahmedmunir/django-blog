# Django-blog:
This is my final project for course [CS50's Web programming with Python and Javascript](https://www.edx.org/course/cs50s-web-programming-with-python-and-javascript).  
My website is about writing articles and sharing it with the others, choose appropriate categories for each article and interact with the articles of the others by adding comments.  
My website template is powered by [Bootstrap Blog Template](https://bootstrapious.com/p/bootstrap-blog) with some modifications from me.

## Installation
use the package manager [pip](https://pip.pypa.io/en/stable/) to install required packages
```bash
pip install -r requirements.txt
```
For security reasons there are some sensetive informations that i didn't provide at **settings.py** file like:  
Email Host - Secreyt key - AWS credentials.  
so you need to provide those info using **virtual environments** or **config.json** file to be able to run the application, and both ways are provided at **settings.py** file.

## Advantages of my website code:
There are some tricks that you can learn how to do from my website code:
- Custom User model where Email field is required to login and must be unique.
- Depend on **AJAX request** to add new comment (rather than default behavior which will redirect you to new form page to add new comment).
- Use **AWS S3** for scalability between server that will launch project code and server that will serve media files.
- Use **RichTextField** that allows user to add photos, links, quotes..etc to the article.
- Two default images for (Male & Female) and image will be associated with account according to gender.

## Roadmap:
Things to be done in the future to enhance website:
- Give user the ability to add new Category.
- Send token to registeration email for confirmation.
- Login using Gmail and Facebook.
- Add marketing (When someone subscribes to website, he gets lates news from website).
- Add more test cases to help for Continuous integration using [Travis CI](https://travis-ci.org/).

## Website Link:
Enjoy writing articles through here:  
https://djangosocialnetwork.herokuapp.com/