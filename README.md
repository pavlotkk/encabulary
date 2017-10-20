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
* [Bootstrap](http://getbootstrap.com/) (desktop only)
* [JQuery](https://jquery.com/) (desktop only)
* [Datatables](https://datatables.net/) (desktop only)
* [Bootstrap tags input](http://bootstrap-tagsinput.github.io/bootstrap-tagsinput/examples/) (desktop only)
* [Vue.js](https://vuejs.org/) (mobile only)
* [Framework7](https://framework7.io/) (mobile only)

## Config and run

#### Help
``` make help ```

#### Create virtual environment and install necessary packages. Install node packages and build frontend
``` make ```

#### Create database (see config.py or instance/config.py)
``` make initdb ```

#### Run tests
``` make tests ```

#### Run application
``` make run ```

#### Install node modules
``` make frontend-install ```

#### Run webpack dev server
``` make frontend-dev ```

#### Build frontend
``` make frontend-build ```


## TODO:
* Add API documentation
* ~~Add install and usage tutorial (with screenshots)~~
* ~~Add demo user and deploy project on test server~~
* Add user registration
* ~~Automaticaly download transcription and translate for your language~~
* Native mobile application for iOS and Android
* ~~Use modern js library: React, Angular, Vue, etc~~
