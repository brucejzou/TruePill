# True Pill  - Article Suggestion [Backend]

### Retrieve Article Text
Filter out unnecessary text from the arbitrary article by a length filter. Longer paragraphs that pass this filter will be added to the ``article_text``.

**Inputs:**

	article_url: "String"

**Outputs:**

	article_text: "String"

### Find Keywords
Uses **[RAKE](https://pypi.org/project/rake-nltk/) (Rapid Automatic Keyword Extraction)** algorithm. 
Returns a list of ranked keywords for the given article text.

**Inputs:**

	article_text : "String"

**Outputs:**
		
	ranked_keywords : ["String"]
	
## Suggested Articles
### Suggested Articles Function
Returns list of suggested ``Articles``  with their respective news source, bias, and URL. The suggested articles are all published from news sources from the list of ``trusted_sources``  and are determined based on the input article's keywords using [NewsAPI](https://newsapi.org/).

**Inputs:**

    article_url: String
**Outputs:**

	suggested_articles: [Article]

	class Article:
		bias: ENUM
		url: "String"

### List of Trusted Sources
Stores a list of trustworthy news sources that we can readily suggest articles from across the spectrum of political biases.
Trusted news sources will be determined based on [credibility](https://mediabiasfactcheck.com/center/), meaning factual reporting and low usage of loaded words.


	trusted_sources: ["String"]


