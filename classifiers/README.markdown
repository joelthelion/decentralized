Decentralized links recomandation
=================================

Usage
-----

1.   Run `rsslinks.py`. This will parse several rss feeds and put those links in a database.
2.   Run `update_prediction.py`. Update good/bad prediction on new links. This script trains classifiers on half the training set.
3.   Run `dumb_ui.py` or use another backend to rate new links.
4.   Repeat to 1 to get new links.

Database
--------

Data is stored into a sqlite database called `test.db`.
There is 3 main tables on the database.

-    links: store records of parsed links.
-    predictions: contains the prediction of a classifier about a link.
-    link_sources: where does that link comes from?

