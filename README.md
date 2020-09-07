For our lab

Credit to  Leonardo de Souza - Florianópolis, Brazil [link](https://github.com/Leonardo8133/stock_manage) for providing such a wonderfull template.


## Importing data from a CSV file
Since we had an already populated inventory list in excel, we needed to figure out how to import it into the current model database.

[link](https://dev.to/coderasha/how-to-export-import-data-django-package-series-3-39mk)

- Step 1 install the package, 

    pip install django-import-export

Then, in your settings.py add ***'import-export',*** library into INSTALLED_APPS:

I also recommend to add optional configuration to end of settings.py:

    IMPORT_EXPORT_USE_TRANSACTIONS = True

The default value is False. It determines if the library will use database transactions on data import.

- Step 2: Create Model
The django-import-export library works with the concept of Resource, which is class definition very similar to how Django handles model forms and admin classes.

- Step 3: Django Admin code
If you want to use import export in admin then simply add following code in your admin.py:

        from import_export.admin import ImportExportModelAdmin
        from django.contrib import admin
        from .models import Employee

        @admin.register(Employee)
        class EmployeeAdmin(ImportExportModelAdmin):
            pass

- Step 4: Import Data

Assume that we have file named employees.csv:

            first_name,last_name,email,day_started,location,id
            Peter,Parker,peter@parker.com,2015-05-18,New York,
            James,Bond,james007@bond.com,2014-08-11,London,


The id must be present because it is the primary key. It will be generated automatically.

