Presentation
------------

KolmoGNUS is a simple yet powerful program which recommends links to the user based on his tastes. Links are taken from selected del.icio.us feeds, and user tastes are learned with a bayesian inference technique. The program comes with a simple TK interface for easy opening and rating of the links.

This simple concept allows to chose links based both on content and collaborative filtering. It quickly gives very good, personalized recommendations.

Slashdot allowed users to comment, Reddit added the right to submit. KolmoGNUS gives you complete freedom of content! 

Installation
------------

To run KolmoGNUS, you simply need python 2.5 and Tkinter. On windows, Tkinter is bundled with python so you don't
have to install anything apart from python. On linux, packages for Tkinter are available on all major distributions.
For example, on fedora the package is called 'tkinter'

Usage
-----

Simply run the tkgui.py program. On the first run, the program will ask to define your tastes in a few keywords.
This is a very important step, but you will have the occasion to add some keywords later through the "train
filter manually" option.

Keyboard shortcuts are extremely important : "l" for liked, "d" for disliked, "enter" to open link in browser.

Contact
-------

Any questions, contributions or other should go to joel \dot\ schaerer \at/ laposte.net
