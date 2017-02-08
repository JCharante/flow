Contribution Guide
================

## Etiquette

* When you need to use a branch, use the naming scheme `#{issue_number}`. This will lead to branch names `#3`, `#23`, `#245`
* **Don't commit directly into the master branch**
* When you add or modify a route in the restful api, you **must** update swagger in a future commit, and link to the commit page on github from swagger.

## Style

* Have an empty line at the end of all files (exclusing `*.json`)
* Use tabs (except for `*.yaml`, use 2 spaces)

## Useful Tools

* If Using Chromium or a derivitive of Chromium:
    * The extension `Allow-Control-Allow-Origin: *` is useful to have, with the intercepter url being `*://localhost/*`
    * The extension `JSON Viewer` is great for exploring the endpoints on the auth server
	* Postman is great for manually creating requests to test the auth server
		* Postman Interceptor is also great for finding out what requests were sent out when debugging the client
* [Ubuntu](https://www.ubuntu.com/) is great to use, as most documentation is geared towards it. It's extremely friendly to beginners.
* [Pycharm](https://www.jetbrains.com/pycharm/) is a great IDE to use, just make sure to follow the readme for a subdirectory before importing it.
