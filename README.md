## Installation

- Install libraries:

```shell
$ pip install Flask
$ pip install flask_sqlalchemy
$ pip install SQLAlchemy
$ pip install pyjwt
$ pip install bs4
$ pip install BeautifulSoup
```

## Usage

put chromedriver.exe and write path to this file, chrome version should be updated

Put you URI in database
   ```shell
   app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/dbname'
   ```
Run your app.py
## Examples
run app.py then provide to the link that you can see in the terminal

```python
http://127.0.0.1:5000/
```
Provide a name of coin and submit.

```python
http://127.0.0.1:5000/coin
```
After that you can see summarization of the text of  each coin that you write
