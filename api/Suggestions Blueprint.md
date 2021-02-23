# True Pill  - Article Suggestion [Backend]

The get suggested articles process is split into the following components:

## Retrieve Article Text
Filter out unnecessary text from the arbitrary article's webpage (e.g, headers, side bar text, etc.) by a length filter to get the main article text. Longer paragraphs that pass this filter will be added to the `article_text`.

**Inputs:**

	article_url: "String"

**Outputs:**

	article_text: "String"

##  Find Keywords
Uses **[RAKE](https://pypi.org/project/rake-nltk/) (Rapid Automatic Keyword Extraction)** algorithm. 
Returns a list of ranked keywords for the given article text.

**Inputs:**

	article_text : "String"

**Outputs:**
		
	ranked_keywords : ["String"]
	
## Suggested Articles
Returns list (length `num_suggestions`) of suggested article urls. The suggested articles are all published from news sources from the list of `trusted_sources`  and are determined based on the input article's keywords. To find the suggested articles, we use Google News RSS queries.

**Inputs:**

    article_keywords: [String]
	num_suggestions: int
	trusted_sources: [String]
**Outputs:**

	suggested_article_urls: [String]

### List of Trusted Sources
Stores a list of trustworthy news sources that we can readily suggest articles from across the spectrum of political biases.
Trusted news sources will be determined based on [credibility](https://mediabiasfactcheck.com/center/), meaning factual reporting and low usage of loaded words.


## Get Biases
Gets the biases for a list of article urls.

**Inputs:**

	article_urls: [String]

**Outputs:**

	articles: [Articles]

	class Article:
		bias: ENUM
		url: "String"

