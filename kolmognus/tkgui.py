#!/usr/bin/env python

import Tkinter
from interface_functions import refresh_stories,manual_train_filter,reevaluate_all,sort_stories,get_feeds,get_filter_stats,train_filter,load_filter,backup,save_stories,is_old
import utils


class App:
    def __init__(self,root):
        self.root=root  #GUI Initialization
        self.root.title("KolmoGNUS intelligent feed reader")
        frame = Tkinter.Frame(root)
        frame.pack()
        self.root.protocol("WM_DELETE_WINDOW", self.quit)
        #Toolbar
        toolbar=Tkinter.Frame(frame)
        self.quitbutton = Tkinter.Button(toolbar,text="quit",command=self.quit)
        self.quitbutton.pack(side=Tkinter.LEFT,)
        like = Tkinter.Button(toolbar,text="Good!",command=self.train_ham)
        like.pack(side=Tkinter.LEFT)
        dislike = Tkinter.Button(toolbar,text="Bad!",command=self.train_spam)
        dislike.pack(side=Tkinter.LEFT,)
        refr = Tkinter.Button(toolbar,text="Refresh",command=self.refresh_list)
        refr.pack(side=Tkinter.LEFT)
        reddit = Tkinter.Button(toolbar,text="Discuss on reddit",command=self.discuss)
        reddit.pack(side=Tkinter.LEFT)

        toolbar.pack(side=Tkinter.TOP,fill=Tkinter.X)

        #Main listbox
        self.lb=Tkinter.Listbox(frame,width=100,height=30)
        self.lb.pack(side=Tkinter.TOP)

        #Event bindings
        self.root.bind("<Return>",self.open_page)
        self.lb.bind("<Double-Button-1>",self.open_page)
        self.root.bind("<Up>",lambda e:self.move_cursor("up"))
        self.root.bind("<Down>",lambda e:self.move_cursor("down"))
        self.root.bind("l",lambda e:like.invoke())
        self.root.bind("d",lambda e:dislike.invoke())
        self.root.bind("r",lambda e:refr.invoke())
        self.root.bind("q",lambda e:self.quit())
        self.root.bind("<FocusIn>", lambda e : self.lb.select_set(self.get_cursor_pos()))

        #Menu
        menu=Tkinter.Menu(root)
        root.config(menu=menu)
        file_menu=Tkinter.Menu(menu)
        menu.add_cascade(label="File",menu=file_menu)
        file_menu.add_command(label="Quit",command=frame.quit)
        tools_menu=Tkinter.Menu(menu)
        menu.add_cascade(label="Tools",menu=tools_menu)
        tools_menu.add_command(label="Manually train filter",command=self.manual_train)
        tools_menu.add_command(label="Show filter info",command=self.show_filter_info)

        #Status bar
        self.stat=Tkinter.Label(root,text="Ready",relief=Tkinter.SUNKEN,anchor=Tkinter.W)
        self.stat.pack(side=Tkinter.BOTTOM,fill=Tkinter.X)
        # Application Initialization
        self.stories,self.slist=None,None
        self.init_stories()
    def get_cursor_pos(self):
        if self.lb.size() == 0:
            return 0
        else:
            current_position=self.lb.curselection()
            if len(current_position) == 0:
                return 0
            else:
                return int(current_position[0])
    def move_cursor(self,direction):
        curpos=self.get_cursor_pos()
        self.lb.select_clear(curpos)
        if direction == "up":
            if curpos == 0:
                self.lb.select_set(self.lb.size()-1)
            else:
                self.lb.select_set(curpos-1)
        elif direction == "down":
            if curpos == self.lb.size() -1:
                self.lb.select_set(0)
            else:
                self.lb.select_set(curpos+1)
    def show_filter_info(self):
        import tkMessageBox
        tkMessageBox.showinfo("Bayesian filter info",get_filter_stats())
    def quit(self):
        save_stories(self.stories)
        print "Now quitting. Bye!"
        self.root.quit()
    def train_spam(self):
        try:
            url=self.get_current_url()
        except Tkinter.TclError:
            pass
        else:
            train_filter(self.stories[url],'spam')
            self.refresh_list(hard=False)
    def train_ham(self):
        try:
            url=self.get_current_url()
        except Tkinter.TclError:
            pass
        else:
            train_filter(self.stories[url],'ham')
            self.refresh_list(hard=False)
    def update_status(self,text):
        self.stat.config(text=text)
        self.root.update()
    def ready_state(self):
        self.stat.config(text="Ready.")
    def get_current_url(self):
        return self.lb.selection_get().split()[1] #very hackish :-/
    def discuss(self):
        """Discuss story on reddit"""
        import urllib
        reddit_submit_url = "http://reddit.com/submit?" + urllib.urlencode([('url',self.get_current_url()),('title','Enter title here')])
        print reddit_submit_url
        self._open_page(reddit_submit_url)
    def open_page(self,dummy):
        #dummy is needed for receiving the tkinter event
        self._open_page()
    def _open_page(self,url=None):
        import webbrowser
        self.update_status("Opening page in browser, please be patient...")
        if url is None:
            webbrowser.open(self.get_current_url())
        else:
            webbrowser.open(url)
        self.ready()
    def refresh_list(self,hard=True):
        self.update_status("Refreshing stories, please be patient...")
        if hard: 
            up_func=lambda x:self.update_status("Please wait... "+x)
            save_stories(self.stories)
            feeds = get_feeds()
            print feeds
            self.stories=refresh_stories(feeds,up_func)
            self.stories=reevaluate_all(self.stories,up_func)
            self.slist=sort_stories(self.stories,up_func)
        self.show_stories(self.slist)
        print "Done refreshing stories!"
    def manual_train(self):
        import tkSimpleDialog
        self.root.lower()
        manual_train_filter(inputfunc=lambda prompt:tkSimpleDialog.askstring("Filter training",prompt))
        self.refresh_list()
    def init_stories(self):
        backup()
        try:
            load_filter()
        except utils.UntrainedFilterException:
            self.manual_train()
        else:
            self.refresh_list()
    def ready(self):
        self.update_status( "Total of %d stories" % len(self.stories.keys()))
    def show_stories(self,story_list):
        curpos=self.get_cursor_pos()
        self.lb.delete(0,self.lb.size()-1) #clear listbox
        for story_text in ["%.2f %s (%s)" % (i[0],i[1],repr(len(self.stories[i[1]].liked)) if self.stories[i[1]].gotadditionalinfo and not self.stories[i[1]].timedout else "?") for i in story_list if not is_old(self.stories[i[1]].url)]:
            self.lb.insert( 0, story_text)
        self.ready()
        if not curpos > self.lb.size(): #Try to replace cursor where it was
            self.lb.select_set(curpos-1 if curpos!=0 else 0)

def main():
    root=Tkinter.Tk()
    App(root)
    root.mainloop()

if __name__ == '__main__':
    main()
