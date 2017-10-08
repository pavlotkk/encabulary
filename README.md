# pyencabulary
Web application for extending English vocabulary

[Demo](http://tpapy.pythonanywhere.com)
**login**: demo
**password**: demo

## General information
* Add personal English words with transcription and multiple translations
* Learn English every day: remember 10 words in a day
* Repeate: repeate learned words every 1, 3, 7 and 30 days
* Easy to add words: automaticaly autocomplite English transcription and translations (for Russian language only)

## Technical information
Backend:
* Python 3
* RESTful API based on [Flask](http://flask.pocoo.org/)
* SQLite database
* [Requests](http://docs.python-requests.org/en/master/) and [lxml](http://lxml.de/) for html scraping

Frontend:
* [Bootstrap](http://getbootstrap.com/)
* [JQuery](https://jquery.com/)
* [Datatables](https://datatables.net/)
* [Bootstrap tags input](http://bootstrap-tagsinput.github.io/bootstrap-tagsinput/examples/)

## Config and run
#### Create virtual environment and install necessary packages
``` make ```

#### Create database (see config.py or instance/config.py)
``` make initdb ```

#### Run tests
``` make tests ```

#### Run application
``` make run ```

#### Help
``` make help ```

## TODO:
* Add API documentation
* ~~Add install and usage tutorial (with screenshots)~~
* ~~Add demo user and deploy project on test server~~
* Add user registration
* ~~Automaticaly download transcription and translate for your language~~
* Native mobile application for iOS and Android
* Use modern js library: React, Angular, Vue, etc
