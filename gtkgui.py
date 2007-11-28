#!/usr/bin/env python

import gobject, gtk

from interface_functions import refresh_stories,manual_train_filter_no_func,reevaluate_all,sort_stories,get_feeds,get_filter_stats,train_filter,load_filter,backup,save_stories,is_old

import utils

COLUMN_SCORE, COLUMN_URL, COLUMN_OTHERS_LIKED = (0, 1, 2)

#TODO: update_status

#TODO: Status bar code
#TODO: Threading
#TODO: gtk.Window + gtk.Treeview for selecting spam+ham tags

class UserTags():
    def __init__(self, init_tags=None):
        self.tags = set()
        if init_tags:
            tag_list = init_tags.split()
            for tag in tag_list:
                self.tags.add(tag)

    def add_tags(self, tag_string):
        tag_list = tag_string.split()
        for tag in tag_list:
            self.tags.add(tag)

    def remove_tags(self, tag_string):
        tag_list = tag_string.split()
        for tag in tag_list:
            self.tags.remove(tag)

    def all_tags(self):
        return ' '.join(list(self.tags))

class KolmoWin(gtk.Window):
    def __init__(self, parent=None, title="KolmoGNUS intelligent feed reader"):
        gtk.gdk.threads_init()
        gtk.Window.__init__(self)

        self.stories = None # Dictionary of story entries
        self.slist = None # Sorted tuples of the stories of form (story.score, story.url)
        
        self.slist = [(0.2, "http://www.google.com")]
        self.ham_tags = UserTags("lisp ruby java c c++ factor smalltalk python") # Example default ham tags, to be changed later
        self.spam_tags = UserTags("digg") # Example default spam tags, to be changed later
        manual_train_filter_no_func(self.ham_tags.all_tags(), self.spam_tags.all_tags())


        self.setup_win(parent, title)

    def setup_win(self, parent, title):
        try:
            self.set_screen(parent.get_screen())
            self.connect("destroy", self.quit_win)
        except AttributeError:
            self.connect("destroy", self.quit_win)

        self.set_title(title)

        self.set_border_width(8)
        self.set_default_size(300, 250)

        vbox = gtk.VBox(False, 2)
        self.add(vbox)

        stories_lstore = self.make_lstore()
        stories_treeview = gtk.TreeView(stories_lstore)
        stories_treeview.set_rules_hint(False)
        stories_treeview.set_search_column(COLUMN_SCORE)

        self.stories_lstore = stories_lstore
        self.stories_treeview = stories_treeview

        button_row = gtk.HBox(False, 2)
        like_button = gtk.Button()
        like_button.connect("clicked", self.train_ham, stories_lstore, stories_treeview)
        like_button.set_label("Good!")
        dislike_button = gtk.Button()
        dislike_button.connect("clicked", self.train_spam, stories_lstore, stories_treeview)
        dislike_button.set_label("Bad!")
        refresh_button = gtk.Button()
        refresh_button.connect("clicked", lambda widget, treeview: self.refresh_story_list(treeview), stories_lstore)
        refresh_button.set_label("Refresh")
        view_button = gtk.Button()
        view_button.connect("clicked", lambda widget, treeview: self.open_page(treeview), stories_treeview)
        view_button.set_label("View")
        reddit_button = gtk.Button()
        reddit_button.connect("clicked", self.discuss, stories_treeview)
        reddit_button.set_label("Discuss on Reddit")
        button_row.pack_start(like_button, False, False)
        button_row.pack_start(dislike_button, False, False)
        button_row.pack_start(refresh_button, False, False)
        button_row.pack_start(view_button, False, False)
        button_row.pack_start(reddit_button, False, False)
        vbox.pack_start(button_row, False, False)

        sw = gtk.ScrolledWindow()
        sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        sw.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        vbox.pack_start(sw)

        self.status_bar = gtk.Statusbar()
        vbox.pack_start(self.status_bar, False, False)
        #context_id = self.status_bar.get_context_id("Status messages")

        

        treeselect = stories_treeview.get_selection()
        treeselect.set_mode(gtk.SELECTION_SINGLE)
        sw.add(stories_treeview)
        self.add_columns(stories_treeview)

        self.init_stories(stories_lstore)

        self.show_all()
        
    def make_lstore(self):
        lstore = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING)
        self.populate_stories(lstore)
        #self.populate_test(lstore)
        return lstore

    def populate_test(self, lstore):
        lstore.append(["0.2", "www.google.com", "(20)"])
        lstore.append(["0.4", "www.del.ici.ous.com", "(20)"])

    def populate_stories(self, lstore):
        if self.stories:
            for (story_score, story_url) in self.slist:
                story = self.stories[story_url]
                if not is_old(story.url):
                    iter = lstore.append()

                    if story.gotadditionalinfo and not story.timedout:
                        lstore.set(iter, COLUMN_SCORE, "%.2f" %story_score, COLUMN_URL, story_url, COLUMN_OTHERS_LIKED,\
                                       "%s others" %repr(len(story.liked)))
                    else:
                        lstore.set(iter, COLUMN_SCORE, "%.2f" %story_score, COLUMN_URL, story_url, COLUMN_OTHERS_LIKED, "?")
        self.ready()

    def add_columns(self, treeview):
        column = gtk.TreeViewColumn("Score", gtk.CellRendererText(), text=COLUMN_SCORE)
        column.set_sort_column_id(COLUMN_SCORE)
        treeview.append_column(column)

        column = gtk.TreeViewColumn("URL", gtk.CellRendererText(), text=COLUMN_URL)
        column.set_sort_column_id(COLUMN_URL)
        treeview.append_column(column)
        
        column = gtk.TreeViewColumn("Others Liked", gtk.CellRendererText(), text=COLUMN_OTHERS_LIKED)
        column.set_sort_column_id(COLUMN_OTHERS_LIKED)
        treeview.append_column(column)

    def refresh_story_list(self, lstore, hard=True):
        self.update_status("Refreshing stories, please be patient...")
        if hard:
            on_update = lambda x: self.update_status("Please wait... " + x)
            save_stories(self.stories)
            feeds = get_feeds()
            print feeds
            self.stories = refresh_stories(feeds, on_update)
            self.slist = reevaluate_all(self.stories, on_update)
            self.slist = sort_stories(self.stories, on_update)
        lstore.clear()
        self.populate_stories(lstore)

    def get_current_url(self, treeview):
        treeselect = treeview.get_selection()
        (model, model_iter) = treeselect.get_selected()
        return model.get_value(model_iter, COLUMN_URL)

    def train_ham(self, widget, lstore, treeview):
        url = self.get_current_url(treeview)
        train_filter(self.stories[url], 'ham')
        self.refresh_story_list(lstore, False)

    def train_spam(self, widget, lstore, treeview):
        url = self.get_current_url(treeview)
        train_filter(self.stories[url], 'spam')
        self.refresh_story_list(lstore, False)

    def open_page(self, treeview, url=None):
        import webbrowser
        import webbrowser
        self.update_status("Opening page in browser, please be patient...")
        if url is None:
            webbrowser.open(self.get_current_url(treeview))
        else:
            webbrowser.open(url)
        self.ready()

    def discuss(self, widget, treeview):
        """Discuss story on Reddit"""
        import urllib
        reddit_submit_url = "http://reddit.com/submit?" + urllib.urlencode([('url',self.get_current_url(treeview)),('title','Enter title here')])
        print reddit_submit_url
        self.open_page(treeview, reddit_submit_url)

    def refresh_list(self, widget, treeview):
        print self.get_current_url(treeview)

    def update_status(self, update_str):
        context_id = self.status_bar.get_context_id("Status messages")
        self.status_bar.push(context_id, update_str)
        #self.status_bar.pop(context_id)

    def ready(self):
        if self.stories:
            self.update_status( "Total of %d stories" % len(self.stories.keys()))

    def init_stories(self, lstore):
        backup()
        try:
            load_filter()
        except utils.UntrainedFilterException:
            # TODO: Prompt for filters
            print "utils.UntrainedFilterException"
        else:
            self.refresh_story_list(lstore)

    def quit_win(self, widget):
        save_stories(self.stories)
        print "Now quitting. Bye!"
        gtk.main_quit()

def main():
    KolmoWin()
    gtk.main()

if __name__ == '__main__':
    main()

