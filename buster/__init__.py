"""
A Django app for appending cache buster strings to html resources, and loading
json file created with gulp-buster.
see: https://github.com/UltCombo/gulp-buster


Example use of the templatetag:
    <script src="{% buster %}{% static "js/app.js" %}{% endbuster %}"></script>

A management command can be used to clear or reload the buster json file in the
django cache. Example:

`manage.py buster reload` or `manage.py buster clear`
"""

import re
import json

from django.core.cache import cache
from django.contrib.staticfiles.storage import staticfiles_storage
from django.conf import settings


BUSTER_FILE = getattr(settings, 'BUSTER_FILE', 'dist/busters.json')
BUSTER_CACHE_KEY = getattr(settings, 'BUSTER_CACHE_KEY', 'BUSTERS_JSON')
BUSTER_CACHE_TIMEOUT = getattr(settings, 'BUSTER_CACHE_TIMEOUT', None)


def get_buster_json(buster_file=BUSTER_FILE):
    """
    Returns json data either from cache or from the busters file from
    staticfiles storage.
    """
    # First check for cached version
    buster_json = cache.get(BUSTER_CACHE_KEY)
    if buster_json is not None:
        return buster_json

    # Look for busters file in staticfiles storage
    buster_json = ''
    if staticfiles_storage.exists(buster_file):
        with staticfiles_storage.open(buster_file) as file_:
            contents = file_.read()
            file_.flush()

        # Try to load the json from file
        try:
            buster_json = json.loads(contents)
        except ValueError:
            pass

    # cache the json
    cache.set(BUSTER_CACHE_KEY, buster_json, BUSTER_CACHE_TIMEOUT)

    return buster_json


def get_buster_for_url(url, busters=None):
    """
    Returns the buster hash for the given url
    """
    # Get the busters json
    if busters is None:
        busters = get_buster_json()
    if not busters:
        return None

    # Cacluate the path relative to static root
    base_url = settings.STATIC_URL
    relpath = re.sub(r'^' + base_url, '', url).lstrip('/')

    # Try to return hash keyed by the path
    try:
        return busters[relpath]
    except KeyError:
        return None


def clear_buster_cache():
    """
    Deletes the buster json data from cache
    """
    cache.delete(BUSTER_CACHE_KEY)


def reload_buster_cache():
    """
    Clears cache, then reloads the buster json data
    """
    clear_buster_cache()
    get_buster_json()  # will fill cache again
