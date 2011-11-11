from gi.repository import Gtk as gtk
import time
import sqlalchemy as sqla
from sqlalchemy.orm import sessionmaker
import model

class UI(object):
    """
    """
    
    def __init__(self, ui):
        """
        
        Arguments:
        - `ui`:
        """
        self._ui = ui
        self._cache = {}
        
        self._builder = gtk.Builder()
        self._builder.add_from_file('ui.xml')

    def __getattr__(self, name):
        """
        
        Arguments:
        - `self`:
        - `name`:
        """
        try:
            widget = self._cache[name]
        except KeyError:
            widget = self._builder.get_object(name)
            self._cache[name] = widget

        return widget
        
    def connect_signals(self, o):
        """
        
        Arguments:
        - `self`:
        """
        self._builder.connect_signals(o)



class MainWin(object):
    """
    """

    def quit_app(self, w, data=None):
        gtk.main_quit()

    def new_pok(self, w, data=None):
        """
        
        Arguments:
        - `self`:
        """
        self.ui.newPokeWin.show_all()
        
        #self.statusBar.push(1, 'New pokemon created.')

    def close_newPokeWin(self, w=None, data=None):
        self.ui.newPokeWin.hide()
        self.ui.newPokeNumber.set_value(0)
        self.ui.newPokeName.set_text('')
        self.ui.newPokeType1.set_active(0)
        self.ui.newPokeType2.set_active(0)


    def save_newPoke(self, w, data=None):
        number = int(self.ui.newPokeNumber.get_value())
        name = self.ui.newPokeName.get_text()
        buff = self.ui.newPokeDesc.get_buffer()
        desc = buff.get_text(buff.get_start_iter(), buff.get_end_iter(), True)

        #Persist pokemon here
        print number, ' : ', name, '\n', desc
        #mew = model.PokemonType(number, name, desc)

        self.close_newPokeWin()

    def togglePokeInfo(self, w, data=None):
        """
        
        Arguments:
        - `self`:
        - `w`:
        - `data`:
        """
        self.ui.pokeInfoPane.set_visible(not self.ui.pokeInfoPane.get_visible())
        

    def about_popup(self, w, data=None):
        """
        """
        self.ui.aboutPopup.show()



    def clear_status_bar(self, w, text, data=None):
        """
        """
        print("plop")
        time.sleep(5)
        self.ui.statusBar.pop(1)


    def populate_list(self, session):
        for p in session.query(model.PokemonType).order_by(model.PokemonType.id):
            print p.id, p.name, p.description
            self.ui.pokemonTypeStore.append([p.id, p.name, p.description])
        
    
    def __init__(self, ui, session):
        """
        """
        self.session = session
        self.ui = UI(ui)
        
        self.ui.connect_signals(self)

        self.tmp_set_up_treeView()



    def start(self):
        """
        
        Arguments:
        - `self`:
        """
        self.ui.mainWin.show_all()
        gtk.main()

    def tmp_set_up_treeView(self):
        """
        Stolen from http://www.eurion.net/python-snippets/snippet/Tree%20View%20Column.html
        Arguments:
        - `self`:
        """
        # create the TreeViewColumns to display the data
        self.columnNumber = gtk.TreeViewColumn('Number')
        self.columnName = gtk.TreeViewColumn('Name')

        # add columns to treeview
        self.ui.pokemonTypeView.append_column(self.columnNumber)
        self.ui.pokemonTypeView.append_column(self.columnName)

        # create a CellRenderers to render the data
        self.cell = gtk.CellRendererText()
        #self.cell1 = gtk.CellRendererText()

        # add the cells to the columns - 2 in the first
        self.columnNumber.pack_start(self.cell, True)
        self.columnName.pack_start(self.cell, True)

        # set the cell attributes to the appropriate liststore column
        self.columnNumber.add_attribute(self.cell, 'text', 0)
        self.columnName.add_attribute(self.cell, 'text', 1)


        

if __name__ == '__main__':
    #sqlite
    engine = sqla.create_engine('sqlite:///:memory:', echo=True)
    Session = sessionmaker(bind=engine)
    model.Base.metadata.create_all(engine)
    mew = model.PokemonType(151, 'Mew', 'Crazy_shit')
    session = Session()
    session.add(mew)

    mine = MainWin('ui.xml', session)
    mine.populate_list(session)                
    mine.start()

    
    
