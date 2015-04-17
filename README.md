# django-buster

A simple Django utility for adding cache busters to static assets. This project is meant as a companion to use alongside [gulp-buster](https://www.npmjs.org/package/gulp-buster). You can use gulp-buster as part of your build process to generate a busters.json file, and use django-buster from within your Django templates to read the file and append the hashes to your static asset urls.

## Generating a busters.json file
If building your static assets with gulp, you may use gulp-buster to save a hash for each of your static assets. You must configure your gulpfile to output a busters.json using gulp-buster. This file will contain a mapping of each file path to its hash. A busters.json file might look like the following:

```
{
    "path/to/styles.css": "f77f5bee5ef6a19bf63fe66aa0971576",
    "path/to/app.js": "03cbc5dc0b5b117264ae74515cd3fb76"
}
```

This file can be deployed along with your other static assets, for example, using the `django collectstatic` command.  
See the [gulp-buster](https://www.npmjs.org/package/gulp-buster) project for more details on busters.json and how to integrate with your gulp build process.


## Integrating with Django

In your Django templates, use the `{% buster %}` templatetag to append a cachebuster querystring to your asset urls. For example:

```
<link rel="stylesheet" href="{% buster %}{% static "dist/styles.css" %}{% endbuster %}" type="text/css" />
<script src="{% buster %}{% static "dist/app.js" %}{% endbuster %}" type="text/javascript"></script>

```

Would output something like the following

```
<link rel="stylesheet" href="/path/to/dist/styles.css?f77f5bee5ef6a19bf63fe66aa0971576" %}" type="text/css" />
<script src="/path/to/dist/app.js?03cbc5dc0b5b117264ae74515cd3fb76" %}" type="text/javascript"></script>

```

## Operation

Upon rendering a template, the `buster` template will read the busters.json using Django's staticfiles storagefile. It will append the hash found in that file if it exists. The busters.json file is only read once, after which it is cached until either the cache timeout setting is reached or a reload is forced using the management command (see below).

## Management commands

Because django-buster caches the busters.json file, a management command is provided to re-read the file. It is advised to run this command as part of your deployment process.

`manage.py reload`: will re-read the busters.json file and re-cache its contents. Run this after deploying static assets.

`manage.py clear`: will clear the cached version of the busters.json file.

## Settings

`BUSTER_FILE`  
This is the location of your busters.json file. This path is relative to your STATIC_ROOT directory.  Defaults to `dist/busters.json`

`BUSTER_CACHE_KEY`  
The cache key to use for caching the busters.json file. Defaults to `BUSTERS_JSON`

`BUSTER_CACHE_TIMEOUT`  
The timeout for caching the busters.json file contents. Defaults to cache indefinitely.
