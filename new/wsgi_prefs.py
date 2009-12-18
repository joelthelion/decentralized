
import cPickle as pp

class Preferences:
    default_prefs = {"cssfilename":"pierre.css"}

    def __init__(self):
        try:
            fh = open("preferences.pck","rb")
            loaded_prefs = pp.load(fh)
            fh.close()
        except IOError:
            loaded_prefs = {}
        self._prefs = Preferences.default_prefs
        for loaded_key,loaded_value in loaded_prefs.items():
            self._prefs[loaded_key] = loaded_value

    def save(self):
        stripped_prefs = {}
        for key,value in self._prefs.items():
            if key in Preferences.default_prefs and Preferences.default_prefs[key] == value:
                continue
            stripped_prefs[key] = value
        fh = open("preferences.pck","wb")
        pp.dump(stripped_prefs,fh)
        fh.close()

    def get(self,key):
        return self._prefs[key]

    def set(self,key,value):
        self._prefs[key] = value
        self.save()

prefs = Preferences()
