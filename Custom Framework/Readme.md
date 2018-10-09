# Custom Framework

This Framework is built by using standard python Werkzeug (WSGI) library.

## Installation

### Requirements
* Python 3.4+
* Werkzeug == 0.14.1
* peewee == 3.7.0
* Jinja2 == 2.10
* virutalenv


## Usage

For using this framework you can simply clone this directory or download it from here.

* Create new virtualenv by using this command: 
`$ virtualenv <Name of Application>`

* Create New folder (Recipes) in your virtualenv folder


        ├── virtualenvfolder/          # This folder will contain all virtualenv files/directories
            ├── Recipes/               # This folder will contain our framework or application
            ├── bin/                   # virtualenv default folder contains virtualenv settings
                └── ....            # Some files of virtualenv
            ├── include/
                └── ....            # Some files of virtualenv
            └── lib/
                └── ....            # Some files of virtualenv




* Now go to your cloned/downloaded folder and copy the `framework` folder along with `load.py, requirements.txt` file

* Paste the folder of `framework` and `load.py,requirements.txt` file in your Recipe folder


        ├── virtualenvfolder/          # This folder will contain all virtualenv files/directories
            ├── Recipes/               # This folder will contain our framework or application
                ├── load.py
                ├── requirements.txt
                └── framework/      # This folder contains framework file
            ├── bin/                   # virtualenv default folder contains virtualenv settings
                └── ....            # Some files of virtualenv
            ├── include/
                └── ....            # Some files of virtualenv
            └── lib/
                └── ....            # Some files of virtualenv



* Activate your virutalenv by `$ virtualenvfolder/bin/activate`

* After activating your virtualenv you must change your directory to `Recipes` folder 
 
      `$ cd virtualenvfolder/Recipes` 

* Run `$ pip install -r requirements.txt` command to install/update all of the dependencies

* After installation of dependencies create new folder `application` in your `Recipe` directory along with `framework` folder


        ├── virtualenvfolder/          # This folder will contain all virtualenv files/directories
            ├── Recipes/               # This folder will contain our framework or application
                ├── load.py
                ├── requirements.txt
                ├── framework/      # This folder contains framework file
                └── application/
            ├── bin/                   # virtualenv default folder contains virtualenv settings
                └── ....            # Some files of virtualenv
            ├── include/
                └── ....            # Some files of virtualenv
            └── lib/
                └── ....            # Some files of virtualenv

* Now create 2 more folder `templates\` and `static\` in your application folder


        ├── virtualenvfolder/  # This folder will contain all virtualenv files/directories
            ├── Recipes/               # This folder will contain our framework or application
                    ├── load.py
                    ├── requirements.txt
                    ├── framework/      # This folder contains framework file
                    └── application/
                                ├── templates/ # This Folder will contain all of your html files
                                |     └── record.html
                                └── static/    # This folder will contain all of your css and JS files

            ├── bin/                   # virtualenv default folder contains virtualenv settings
                    └── ....            # Some files of virtualenv
            ├── include/
                    └── ....            # Some files of virtualenv
            └── lib/
                    └── ....            # Some files of virtualenv

* Now create your `.html` files under the templates folder and `.css , .js ` files under static folder

        ├── virtualenvfolder/          # This folder will contain all virtualenv files/directories
            ├── Recipes/               # This folder will contain our framework or application
                ├── load.py
                ├── requirements.txt
                ├── framework/      # This folder contains framework file
                            └── .....  #Framework files
                └── application/
                            ├── templates/ # This Folder will contain all of your html files
                            |     └── record.html
                            └── static/    # This folder will contain all of your css and JS files
                                └──style.css

            ├── bin/                   # virtualenv default folder contains virtualenv settings
                └── ....            # Some files of virtualenv
            ├── include/
                └── ....            # Some files of virtualenv
            └── lib/
                └── ....            # Some files of virtualenv

* After writing your `html` codes you must make a file which will contains all of handler for that pages every handler will be a function
    
     You can see the example application project from the cloned/downloaded folder and see the `view_controllers.py` for handler example

* If you want to use database with your application you must make file which will contains all of the Database Model see the [Peewee.Models](http://docs.peewee-orm.com/en/latest/peewee/models.html)

* Make a list variable in your database models file and write all of the name of your models in that list

* You have to make another file which will have all of your urls mapping in the dictionary shape

```python
url_map = {
  '/': endpoint     #endpoint is the name of your handler for that url
  '/get': 'get_recipes'
}
 
```

* The most important file is `settings.py` it will contain all of your application settings
```python
view_controllers = "application.view_controllers"
template_path = os.path.join(os.path.dirname(__file__), "templates")
static_path = os.path.join(os.path.dirname(__file__), "static")
url_mapping = "application.url_mapping"
DB_URL = os.path.join(os.path.dirname(__file__), "Recipes.db")
DB_MODELS = "application.database_models"
```

   **Settings file must have `view_controllers, template_path, static_path, url_mapping` this variables set this variables are required for framework running**

* After setting all of your things for your application your directory must look like this:

        ├── virtualenvfolder/
            ├── Recipes/
                ├── load.py
                ├── requirements.txt
                ├── framework/      # This folder contains framework file
                            └── .....  #Framework files
                └── application/
                            ├── view_controllers.py  # This file will contain your template_handlers
                            ├── database_models.py   # This file will contain your database models
                            ├── settings.py          # This file will have all your application files path set
                            ├── templates/ # This Folder will contain all of your html files
                            |     └── record.html
                            └── static/    # This folder will contain all of your css and JS files
                                └──style.css

            └── ....

* Now go to your load.py file and set it's `APPLICATION_SETTINGS` variable with your `application.settings` module

* After setting everything you can run your from your `Recipe` directory
                 
            $python load.py

This will successfully run your application 