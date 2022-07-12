<p align="center">
    <img src="https://github.com/puravparab/Songswipe/blob/1a39812a5a3feef8b823157670a0defc0da48aa1/static/app/assets/images/apple-touch-icon.png"/>
</p>

<p align="center">
	<h1 align="center">
		SONGSWIPE
	</h1>
	<p align="center">
		Swipe on songs
	</p>
</p>

<p align="center">
    <a target="_blank" href="https://www.python.org/downloads/" title="Python version"><img src="https://img.shields.io/badge/python-%3E=_3.9-green.svg"></a>
	<a target="_blank" href="LICENSE" title="License: MIT"><img src="https://img.shields.io/badge/License-MIT-blue.svg"></a>
</p>

<p align="center">
	<a href="#Installation">INSTALLATION</a>
	&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
	<a href="#License">LICENSE</a>
</p>

# Installation:

Clone the respository
```
$ git clone https://github.com/puravparab/Songswipe.git
```
Change the working directory to Chattrr
```
$ cd Songswipe
```
Install pipenv to your machine
```
$ pip install --user pipenv
```
Install dependencies from Pipfile
```
$ pipenv install
```
Run the virtual environment
```
$ pipenv shell
```
Create  a file called .env
<br>
Update the entries in the .env file.
```
SECRET_KEY= <create a secret key>
DEBUG=True
DJANGO_SETTINGS_MODULE=songswipe.settings.dev
ALLOWED_HOSTS=localhost 127.0.0.1

<Add your Spotify API keys>
SPOTIFY_CLIENT_ID=
SPOTIFY_CLIENT_SECRET=
SPOTIFY_REDIRECT_URI= <Your Domain>/spotify/callback
```
Run the following commands
```
$ python manage.py migrate
$ python manage.py collectstatic
```
This completes the backend/server configuration.

---

Add a superuser to Django Admin
```
$ python manage.py createsuperuser
```
Run the server at http://127.0.0.1:8000 or http://localhost:3000
```
$ python manage.py runserver
```

---

# LICENSE

MIT License

Copyright (c) 2022 Songswipe

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

Original Creator - [Purav Parab](https://github.com/puravparab)