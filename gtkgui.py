#!/usr/bin/env python

import gobject, gtk

from interface_functions import refresh_stories,manual_train_filter_no_func,reevaluate_all,sort_stories,get_feeds,get_filter_stats,train_filter,load_filter,backup,save_stories,is_old

import utils

COLUMN_SCORE, COLUMN_URL, COLUMN_OTHERS_LIKED = (0, 1, 2)
COLUMN_TAGS = 0


#TODO: Add functionality to status bar code*
#TODO: Threading**
#TODO: Fix initial dimensions of HamSpamWin()
#TODO: Enable saving of current Ham/Spam tags
#TODO: Keyboard shortcuts/double-click to view

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
    
    def tags_iter(self):
        for tag in self.tags: yield tag

class HamSpamWin(gtk.Window):
    def __init__(self, parent, title="Configure User Interests"):
        gtk.gdk.threads_init()
        gtk.Window.__init__(self)
        

        self.ham_tags = parent.ham_tags
        self.spam_tags = parent.spam_tags
        self.setup_win(parent, title)

    def setup_win(self, parent, title):
        self.set_screen(parent.get_screen())
        self.set_title(title)
        self.set_border_width(8)
        self.set_default_size(200, 250)
        

        vbox = gtk.VBox(False, 2)
        self.add(vbox)

        ham_lstore = self.ham_lstore = self.make_ham_lstore()
        ham_treeview = self.ham_treeview  = gtk.TreeView(ham_lstore)
        spam_lstore = self.spam_lstore = self.make_spam_lstore()
        spam_treeview = self.spam_treeview = gtk.TreeView(self.spam_lstore)

        ## Widget layout looks like this:
        ## Tree: Vbox
        ##
        ## Vbox: ham_label, ham_hbox, ham_entry, spam_label, spam_hbox, spam_entry
        ##
        ## ham_hbox: ham_scroll, ham_vbox
        ## ham_scroll: ham_treeview
        ## ham_vbox: ham_add_button, ham_remove_button
        ##
        ## spam_hbox: spam_scroll, spam_vbox
        ## spam_scroll: spam_treeview
        ## spam_vbox: spam_add_button, spam_remove_button

        ### Ham entries 

        ## Ham Label

        ham_label = gtk.Label("Like Tags")
        ham_label.set_justify(gtk.JUSTIFY_LEFT)
        vbox.pack_start(ham_label, False, False)

        ham_hbox = gtk.HBox(False, 2)

        ## Ham Scrolled-treeview

        ham_scroll = gtk.ScrolledWindow()
        ham_scroll.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        ham_scroll.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        treeselect = self.ham_treeview.get_selection() # Grab selection and set single selection mode
        treeselect.set_mode(gtk.SELECTION_SINGLE)
        ham_scroll.add(ham_treeview)
        ham_hbox.pack_start(ham_scroll)

        ## Ham buttons
        ham_button_vbox = gtk.VBox(False, 2)
        ham_add_button = gtk.Button()
        ham_add_button.connect("clicked", self.ham_add_callback)
        ham_add_button.set_label("Add")
        ham_remove_button = gtk.Button()
        ham_remove_button.connect("clicked", lambda w: self.remove_selected_ham())
        ham_remove_button.set_label("Remove")
        ham_button_vbox.pack_start(ham_add_button, False, False)
        ham_button_vbox.pack_start(ham_remove_button, False, False)
        ham_hbox.pack_start(ham_button_vbox)
        vbox.pack_start(ham_hbox)

        ## Ham Text Entry

        self.ham_entry = ham_entry = gtk.Entry(max=0)
        self.ham_entry.connect("activate", self.ham_add_callback)
        vbox.pack_start(ham_entry)

        ### Spam section

        ## Spam label
        
        spam_label = gtk.Label("Dislike Tags")
        spam_label.set_justify(gtk.JUSTIFY_LEFT)
        vbox.pack_start(spam_label, False, False)

        spam_hbox = gtk.HBox(False, 2)

        ## Spam Scrolled-Treeview

        spam_scroll = gtk.ScrolledWindow()
        spam_scroll.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        spam_scroll.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        treeselect = self.spam_treeview.get_selection() # Grab selection and set single selection mode
        treeselect.set_mode(gtk.SELECTION_SINGLE)
        spam_scroll.add(spam_treeview)
        spam_hbox.pack_start(spam_scroll)

        ## Spam add and remove buttons

        spam_button_vbox = gtk.VBox(False, 2)
        spam_add_button = gtk.Button()
        spam_add_button.connect("clicked", self.spam_add_callback)
        spam_add_button.set_label("Add")
        spam_remove_button = gtk.Button()
        spam_remove_button.connect("clicked", lambda w: self.remove_selected_spam())
        spam_remove_button.set_label("Remove")
        spam_button_vbox.pack_start(spam_add_button, False, False)
        spam_button_vbox.pack_start(spam_remove_button, False, False)
        spam_hbox.pack_start(spam_button_vbox)

        vbox.pack_start(spam_hbox)

        self.spam_entry = spam_entry = gtk.Entry(max=0)
        self.spam_entry.connect("activate", self.spam_add_callback)
        vbox.pack_start(spam_entry)

        self.ham_add_columns()
        #self.load_ham()
        self.spam_add_columns()
        #self.load_spam()

        self.show_all()

    def make_ham_lstore(self):
        lstore = gtk.ListStore(gobject.TYPE_STRING)
        self.populate_ham_lstore(lstore)
        return lstore

    def populate_ham_lstore(self, lstore):
        for tag in self.ham_tags.tags_iter(): lstore.append([tag])

    def make_spam_lstore(self):
        lstore = gtk.ListStore(gobject.TYPE_STRING)
        self.populate_spam_lstore(lstore)
        return lstore

    def populate_spam_lstore(self, lstore):
        for tag in self.spam_tags.tags_iter(): lstore.append([tag])

    def ham_add_columns(self):
        column = gtk.TreeViewColumn("Tags", gtk.CellRendererText(), text=COLUMN_TAGS)
        column.set_sort_column_id(COLUMN_TAGS)
        self.ham_treeview.append_column(column)

    def load_ham(self):
        self.populate_ham_lstore(self.ham_lstore)

    def spam_add_columns(self):
        column = gtk.TreeViewColumn("Tags", gtk.CellRendererText(), text=COLUMN_TAGS)
        column.set_sort_column_id(COLUMN_TAGS)
        self.spam_treeview.append_column(column)

    def spam_add_callback(self, widget):
        text = self.spam_entry.get_text()
        if text:
            self.spam_tags.add_tags(text)
            self.spam_entry.set_text('')
            self.spam_lstore.clear()
            self.populate_spam_lstore(self.spam_lstore)

    def ham_add_callback(self, widget):
        text = self.ham_entry.get_text()
        if text:
            self.ham_tags.add_tags(text)
            self.ham_entry.set_text('')
            self.ham_lstore.clear()
            self.populate_ham_lstore(self.ham_lstore)

    def get_tag_selection(self, treeview):
        treeselect = treeview.get_selection()
        (model, model_iter) = treeselect.get_selected()
        return model.get_value(model_iter, COLUMN_TAGS)

    def get_spam_selection(self):
        treeselect = self.ham_treeview.get_selection()
        (model, model_iter) = treeselect.get_selected()
        return model.get_value(model_iter, COLUMN_TAGS)

    def get_ham_selection(self):
        treeselect = self.spam_treeview.get_selection()
        (model, model_iter) = treeselect.get_selected()
        return model.get_value(model_iter, COLUMN_TAGS)

    def remove_selected_ham(self):
        self.ham_tags.remove_tags(self.get_tag_selection(self.ham_treeview))
        self.ham_lstore.clear()
        self.populate_ham_lstore(self.ham_lstore)

    def remove_selected_spam(self):
        self.spam_tags.remove_tags(self.get_tag_selection(self.spam_treeview))
        self.spam_lstore.clear()
        self.populate_spam_lstore(self.spam_lstore)


class KolmoWin(gtk.Window):
    def __init__(self, parent=None, title="KolmoGNUS intelligent feed reader"):
        gtk.gdk.threads_init()
        gtk.Window.__init__(self)

        self.stories = None # Dictionary of story entries
        self.slist = None # Sorted tuples of the stories of form (story.score, story.url)
        
        #self.slist = [(0.2, "http://www.google.com")]
        #manual_train_filter_no_func(self.ham_tags.all_tags(), self.spam_tags.all_tags())


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

        menubar = self.make_menu()
        vbox.pack_start(menubar, expand=False)

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
        refresh_button.connect("clicked", lambda widget: self.refresh_story_list())
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

    def refresh_story_list(self, hard=True):
        self.update_status("Refreshing stories, please be patient...")
        if hard:
            on_update = lambda x: self.update_status("Please wait... " + x)
            save_stories(self.stories)
            feeds = get_feeds()
            print feeds
            self.stories = refresh_stories(feeds, on_update)
            self.slist = reevaluate_all(self.stories, on_update)
            self.slist = sort_stories(self.stories, on_update)
        self.stories_lstore.clear()
        self.populate_stories(self.stories_lstore)

    def make_menu(self):

        ag = gtk.ActionGroup('WindowActions')
        actions = [
            ('FileMenu', None, '_File'),
            ('Quit',     gtk.STOCK_QUIT, '_Quit', '<control>Q',
             'Quit application', self.quit_win),
            ('ActionsMenu', None, '_Actions'),
            ('Refresh', None, '_Refresh', '<control>R',
             'Refresh stories', lambda action: self.refresh_story_list()),
            ('ToolsMenu', None, '_Tools'),
            ('ManualTrain', None, 'Manually Train Filter', None, 'Manually Train Filter',
             lambda action: HamSpamWin(self)),
            ('FilterInfo', None, 'Filter Info', None, 'Filter Information')
            ]
        ag.add_actions(actions)
        self.ui = gtk.UIManager()
        self.ui.insert_action_group(ag, 0)
        self.ui.add_ui_from_file("gtkgui_menu.xml")
        self.add_accel_group(self.ui.get_accel_group())

        return self.ui.get_widget("/Menubar")

    def get_current_url(self, treeview):
        treeselect = treeview.get_selection()
        (model, model_iter) = treeselect.get_selected()
        return model.get_value(model_iter, COLUMN_URL)

    def train_ham(self, widget, lstore, treeview):
        url = self.get_current_url(treeview)
        train_filter(self.stories[url], 'ham')
        self.refresh_story_list(hard=False)

    def train_spam(self, widget, lstore, treeview):
        url = self.get_current_url(treeview)
        train_filter(self.stories[url], 'spam')
        self.refresh_story_list(hard=False)

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
            HamSpamWin() # If no tags are loaded, display tag-request window
            print "utils.UntrainedFilterException"
        else:
            self.refresh_story_list()

    def quit_win(self, widget):
        save_stories(self.stories)
        print "Now quitting. Bye!"
        gtk.main_quit()

def main():
    KolmoWin()
    gtk.main()

if __name__ == '__main__':
    main()

