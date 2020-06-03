using [django-lab-inventory 0.4.0](https://pypi.org/project/django-lab-inventory/) as a stating guide

1. Add `inventory` to your INSTALLED_APPS setting like this:

2. Include the inventory URLconf in your project urls.py like this::

```python
url(r'^inventory/', include(inventory.urls')),
```

3. Run `python manage.py migrate` to create the inventory models.

4. Start the development server and visit http://127.0.0.1:8000/admin/inventory/
to create items, vendors, manufacturers, etc. (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/inventory/ to use views.

