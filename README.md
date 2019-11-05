# **Utilizing Yelp Data to Predict Zip Code Affluence**






## **Problem Statement**
This tool will estimate the affluence of a neighborhood based on the number of $ of businesses and services (according to Yelp) in a given neighborhood ($, $$, $$$, $$$$). This tool will expect to get, as an input, a list of zip codes and will estimate the wealth of the locality. While traditional methods typically estimate wealth of a locality based on demographic characteristics (e.g. income or unemployment rate), the novelty of this approach is in its use of big data related to commercial activity and cost of product and services as an indicator for affluency.




## **Repository Contents**
- Assets  
  - `.json` files required for webscraping process
- Code   
  - `01 - Yelp Webscraping.ipynb`
  - `02 - Yelp Data Merging & Cleaning.ipynb`
  - `03 - Yelp Adding IRS Income to Dataframe.ipynb`
  - `04 - Yelp Modeling.ipynb`
  - `A1_creating-zip-code-coordinate-dictionary.ipynb`
  - `A2_graphql-API.ipynb`
- Data
  - `.csv` files acquired from webscraping process
- Flask  
  - Materials to launch the Flask application




## **Data Dictionary**
The dictionary for the final dataframe used for our model.

|Feature|Type|Description|
|------|----------|-------|
|**zip_code**|object|Unique zip code in dataframe.|
|**ave_agi**|float|IRS data on average adjusted gross income for a zip code.|
|**count**|int|Number of businesses in a zip code.|
|**latitude**|float|Latitude location of zip code.|
|**longitude**|float|Longitude location of zip code.|
|**price**|float|Average number of $ for all businesses in a zip code.|
|**price*rating**|float|An engineered feature that multiplies price and rating together for each business and then averages all of the businesses together in that zip code.|
|**rating**|float|Average star rating (out of 5) for all businesses in a zip code.|
|**review_count**|float|Average number of review counts for all businesses in a zip code.|




## **Executive Summary**
Insert some summary about our results  

|Metric|Score|
|------|----------|
|Some Metric|Some Score|
|Some Metric|Some Score|
|Some Metric|Some Score|
|Some Metric|Some Score|
|Some Metric|Some Score|
|Some Metric|Some Score|




## **Conclusions & Recommendations**
Some conclusion about how our app should be used and it's limitations, and maybe some pretty graphs about some basic info of our data (ie. distribution of price $).



## **Sources**
Insert links here.
