#!/usr/bin/env python

import sys
from PyQt4 import QtCore, QtGui
from kolmognus import Ui_MainWindow
from interface_functions import refresh_stories,manual_train_filter,reevaluate_all,sort_stories,get_feeds,get_filter_stats,train_filter,load_filter,backup,save_stories,is_old
import utils

class StartQT4(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # Application Initialization
        self.stories,self.slist=None,None
        self.init_stories()
        self.ui.FeedList.addItem( "http://www.google.com" )
        self.ui.FeedList.addItem( "http://www.lemonde.fr" )
        self.ui.FeedList.addItem( "http://www.lequipe.fr" )
        # Connect Signal and Slots
        QtCore.QObject.connect(self.ui.RedditBtn,QtCore.SIGNAL("clicked()"), self.discuss)
        #QtCore.QObject.connect(self.ui.BadBtn,QtCore.SIGNAL("clicked()"), self.train_spam)
        #QtCore.QObject.connect(self.ui.GoodBtn,QtCore.SIGNAL("clicked()"), self.train_ham)
        QtCore.QObject.connect(self.ui.RefreshBtn,QtCore.SIGNAL("clicked()"), self.refresh_list)
    def init_stories(self):
        backup()
        try:
            load_filter()
        except utils.UntrainedFilterException:
            self.manual_train()
        else:
            self.refresh_list()
    def update_status_scan(self):
        self.ui.statusbar.showMessage( "Refreshing stories, please be patient..." )
    def update_status_spam(self):
        self.ui.statusbar.showMessage( "Refresh spam filter done..." )
    def discuss(self):
        """Discuss story on reddit"""
        import urllib
        reddit_submit_url = "http://reddit.com/submit?" + urllib.urlencode([('url',self.get_current_url()),('title','Enter title here')])
        print reddit_submit_url
        self._open_page(reddit_submit_url)
    def train_ham(self):
        self.url=self.get_current_url()
        if url.isEmpty() == False:
            train_filter(self.stories[url],'ham')
            self.refresh_list(hard=False)
    def get_current_url(self):
        return self.ui.FeedList.selectedItems().begin()
    def refresh_list(self,hard=True):
        #This should be done via signal and slots
        #self.ui.statusbar.("Refreshing stories, please be patient...")
        if hard: 
            #up_func=lambda x:self.update_status("Please wait... "+x)
            save_stories(self.stories)
            feeds = get_feeds()
            print feeds
            #self.stories=refresh_stories(feeds,up_func)
            #self.stories=reevaluate_all(self.stories,up_func)
            #self.slist=sort_stories(self.stories,up_func)
        self.show_stories(self.slist)
        print "Done refreshing stories!"
    def show_filter_info(self):
        QMessageBox(self,"Bayesian filter info",get_filter_stats())
    #def ready(self):
        #self.update_status( "Total of %d stories" % len(self.stories.keys()))
    def show_stories(self,story_list):
        #curpos=self.get_cursor_pos()
        self.ui.FeedList.clear()
        #for story_text in ["%.2f %s (%s)" % (i[0],i[1],repr(len(self.stories[i[1]].liked)) if self.stories[i[1]].gotadditionalinfo and not self.stories[i[1]].timedout else "?") for i in story_list if not is_old(self.stories[i[1]].url)]:
            #self.ui.FeedList.addItem( story_text )
        #self.ready()
        #if not curpos > self.ui.FeedList.size(): #Try to replace cursor where it was
            #self.lb.select_set(curpos-1 if curpos!=0 else 0)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = StartQT4()
    myapp.show()
    sys.exit(app.exec_())

