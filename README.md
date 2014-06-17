TinySubscriptions
=================
A simple, embeddable subscription list manager.

 - Allows end-users to subscribe / unsubscribe.
  - Maintains end-user subscriptions via an external subscription service ([SendGrid](http://sendgrid.com/)).
 - Allows admin users to set which subscriptions are available to end-users.
  - Maintains subscription availability locally


Contact / development team
--------------------------
This is a project of [Gleap LLC](http://gleap.org) with copyright 2014.

 - Sam Pottinger ([samnsparky](http://gleap.org/))
 - Rory Olsen ([rolsen](https://github.com/rolsen))


License
-------
GNU GPLv3


Technologies used
-----------------

 - [Flask](http://flask.pocoo.org/)
 - [pymox](https://code.google.com/p/pymox/) (server-side testing)
 - [SendGrid](http://sendgrid.com/)


Local system setup
------------------
Ensure Python 2.7.* and PIP.

 - Python: [Mac](http://docs.python-guide.org/en/latest/starting/install/osx/) (brew is suggested), [Linux](http://docs.python-guide.org/en/latest/starting/install/linux/), [Windows](http://www.python.org/)
 - PIP: [Mac](http://stackoverflow.com/questions/17271319/installing-pip-on-mac-os-x), [Linux](http://docs.python-guide.org/en/latest/starting/install/linux/), [Windows](http://stackoverflow.com/questions/4750806/how-to-install-pip-on-windows)


Local virtual environment setup
-------------------------------
[VirtualEnv](http://virtualenv.readthedocs.org/en/latest/) is recommended, but not required. ```venv``` is in the .gitignore.

Install software
```$ pip install -r requirements.txt```


Local development / testing
---------------------------

Run automated tests
```$ python run_tests.py```

Start local server
```$ python tiny_subscriptions.py```


Development guidelines / standards
----------------------------------
Due to the potential for mutliple deployment and client-driven modification outside of Gleap (the original developer), this project values high test coverage and style adherence.

 - The project asks for 80% test coverage on server-side.
 - Server-side modules, classes, and functions should be documented using [epydoc](http://epydoc.sourceforge.net/).
 - Server-side code should conform to [Google's Python Style Guide](http://google-styleguide.googlecode.com/svn/trunk/pyguide.html).
 - The project uses plain old CSS but should have element, class, and finally ID-based rules in that order.
 - Client-side JS should follow [Google's JavaScript Style Guide](http://google-styleguide.googlecode.com/svn/trunk/javascriptguide.xml).
 - Client-side files, classes, and functions should be documented using [JSDoc](http://usejsdoc.org/).
 - Client-side automated tests are optional but encouraged. For help with getting started on client-side testing, see [Addy Osmani's tutorial](http://addyosmani.com/blog/unit-testing-backbone-js-apps-with-qunit-and-sinonjs/).
 - All code checked in (via Gleap) to master or a version release branch should go through code review.
 - Code produced during pair programming or for initial project bootstrapping does not require code review. However, the results of pair programming should still go through a pull request.
 - Engineers can perform a code review for themselves if another engineer is not available within one working day.


Configuration Settings
----------------------
The application configuration settings are maintained by Flask. The configuration values (held in flask_config.json) should include:

 - REDIS_HOST: The URI where the application redis instance can be accessed.
 - REDIS_PORT: The port where the application redis instance should be accessed.
 - REDIS_DB: The integer ID of the database to use.
 - REDIS_PASSWORD: The password to use to authenticate with the redis service.
 - REDIS_EXPIRATION: The number of seconds that data cached in the redis service should be saved there before being marked invalid.
 - FAKE_MONGO: Boolean indicating if a mongo database should be emulated.
 - BASE_URL: The URL where this module is running out of.
 - SENDGRID_API_USERNAME: The username to use to authenticate with the transactional email service.
 - SENDGRID_API_KEY: The API key (password) to use to authenticate with the transactional email service.
 - FAKE_SENDGRID: Boolean indicating if the sendgrid service should be emulated.
 - BASE_STATIC_URL: The root URL where the static content supporting this module can be found.

These configuration values we be loaded from the 'tinysubscriptions' attribute if that attribute is defined.
