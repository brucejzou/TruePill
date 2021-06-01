# True Pill Server

## Setup
Install dependencies
`pip install -r requirements.txt`

## Running
### Unix
```
$ export FLASK_APP=api.py
$ flask run
```

### Windows PowerShell
```
PS C:\path\to\app> $env:FLASK_APP = "api.py"
PS C:\path\to\app> flask run
```
If `flask run` doesn't work, an alternative is `python -m flask run`.

The server will run locally at http://127.0.0.1:5000/

## Creating Media Bias database
Run `python create_bias_db.py` to create a tinyDB database at `'media_bias_db.json'`.

### Running tests
```
pytest -v
```
Run the above command in the api folder.


## Example output from server:
```
Input: 
{
    "article_url" : "https://www.nytimes.com/2021/02/07/us/politics/trump-impeachment.html"
}
```

```
Output:
{
	"article_url":"https://www.bbc.com/news/world-asia-56228357",
	"bias":"LEFT_CENTER",
	"suggested_articles":[
		{
			"article_url":"https://www.cnn.com/2021/02/27/asia/myanmar-un-ambassador-fired-intl-hnk/index.html",
			"bias":"LEFT"
		},
		{
			"article_url":"https://www.startribune.com/un-human-rights-office-says-18-killed-in-myanmar-crackdown/600028529/",
			"bias":"LEFT_CENTER"
		},
		{
			"article_url":"https://news.yahoo.com/deadliest-day-myanmar-protests-police-192021295.html",
			"bias":"LEFT_CENTER"
		},
		{
			"article_url":"https://www.csmonitor.com/World/Asia-Pacific/2021/0228/Myanmar-police-intensify-violence-against-anti-coup-protests?icid=rss",
			"bias":"CENTER"
		}
	]
}
```
