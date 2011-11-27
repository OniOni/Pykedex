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


def populate_db(session):
    l = ["Normal","Fire","Water","Electric","Grass","Ice","Fighting","Poison",
         "Ground","Flying","Psychic","Bug","Rock","Ghost","Dragon","Dark",
         "Steel"]

    for n in l:
        p = model.Type(n)
        session.add(p)

class MainWin(object):
    """
    """

    def quit_app(self, w, data=None):
        self.session.commit()
        gtk.main_quit()

    def new_pok(self, w, data=None):
        """
        
        Arguments:
        - `self`:
        """
        self.ui.newPokeWin.show_all()

    def edit_pok(self, w, date=None):
        """
        
        Arguments:
        - `self`:
        - `w`:
        - `date`:
        """
        selected = self.ui.pokemonTypeView.get_selection().get_selected()
        poke = self.session.query(model.PokemonType).filter_by(id=self.ui.pokemonTypeStore[selected[1]][0]).one()
        print "selected pokemon : " + repr(poke)

        try:
            self.ui.newPokeNumber.set_value(self.ui.pokemonTypeStore[selected[1]][0])
            self.ui.newPokeName.set_text(self.ui.pokemonTypeStore[selected[1]][1])
            self.ui.newPokeDescBuff.set_text(self.ui.pokemonTypeStore[selected[1]][2])
        except Exception as e:
            print e

        
        poke.types
        try:            
            self.ui.newPokeType1.set_active_id(poke.types[0].name)
            self.ui.newPokeType2.set_active_id(poke.types[1].name)
        except IndexError as e:
            print e


        self.ui.newPokeWin.show_all()

        self.ui.saveNewPoke.set_visible(False)
        self.ui.saveEditPoke.set_visible(True)

        
        #TODO
        #self.ui.newPokeType1.set_active(0)
        #self.ui.newPokeType2.set_active(0)


    def close_newPokeWin(self, w=None, data=None):
        self.ui.newPokeWin.hide()
        self.ui.newPokeNumber.set_value(0)
        self.ui.newPokeName.set_text('')
        self.ui.newPokeDescBuff.set_text('')
        self.ui.newPokeType1.set_active(0)
        self.ui.newPokeType2.set_active(0)

        if self.ui.saveEditPoke.get_visible():
            self.ui.saveNewPoke.set_visible(True)
            self.ui.saveEditPoke.set_visible(False)


    def getPokemonTypeFromPropWin(self):
        """
        
        Arguments:
        - `self`:
        """
        number = int(self.ui.newPokeNumber.get_value())
        name = self.ui.newPokeName.get_text()
        buff = self.ui.newPokeDesc.get_buffer()
        desc = buff.get_text(buff.get_start_iter(), buff.get_end_iter(), True)
        
        poke = model.PokemonType(number, name, desc)
        
        type1 = self.typeList[self.ui.newPokeType1.get_active_id()]
        type2 = self.typeList[self.ui.newPokeType2.get_active_id()]
        poke.types += [type1, type2]

        print (type1, type2)

        return poke


    def save_newPoke(self, w, data=None):
        p = self.getPokemonTypeFromPropWin()
        #Persist pokemon here
        self.session.add(p)

        self.ui.pokemonTypeStore.append([p.id, p.name, p.description])
        self.ui.statusBar.push(1, 'New pokemon created.')

        self.close_newPokeWin()


    def save_editedPoke(self, w=None, data=None):
        """
        
        Arguments:
        - `self`:
        - `w`:
        - `data`:
        """
        pokemon = self.getPokemonTypeFromPropWin()

        selected = self.ui.pokemonTypeView.get_selection().get_selected()

        self.ui.pokemonTypeStore[selected[1]][0] = pokemon.id
        self.ui.pokemonTypeStore[selected[1]][1] = pokemon.name
        self.ui.pokemonTypeStore[selected[1]][2] = pokemon.description

        self.session.merge(pokemon)

        self.ui.saveNewPoke.set_visible(True)
        self.ui.saveEditPoke.set_visible(False)

        self.ui.statusBar.push(1, 'Pokemon edited')

        self.close_newPokeWin()


    def togglePokeInfo(self, w, data=None):
        """
        
        Arguments:
        - `self`:
        - `w`:
        - `data`:
        """
        self.ui.pokeInfoPane.set_visible(self.ui.toolBarToggleInfo.get_active())

        self.ui.statusBar.push(1, 'Info pane {0} '.format('visible' if self.ui.pokeInfoPane.get_visible() else 'hidden'))

    def populate_InfoPane(self, w, lol=None, data=None):
        """
    
        Arguments:
        - `self`:
        """
        selected = self.ui.pokemonTypeView.get_selection().get_selected()
        try:
            if not self.ui.pokeInfoBox.get_visible():
                self.ui.pokeInfoBox.set_visible(True)
                self.ui.pokeInfoPaneLabel.set_visible(False)

            poke = self.session.query(model.PokemonType).filter_by(id=self.ui.pokemonTypeStore[selected[1]][0]).one()
                            
            self.ui.infoPaneImage.set_from_file('img/{0}.png'.format(str(self.ui.pokemonTypeStore[selected[1]][0])))

            self.ui.infoPaneNumber.set_text(str(self.ui.pokemonTypeStore[selected[1]][0]))
            self.ui.infoPaneName.set_text(self.ui.pokemonTypeStore[selected[1]][1])
            self.ui.infoPaneDescBuff.set_text(self.ui.pokemonTypeStore[selected[1]][2])

            poke.types

            try:
                self.ui.infoPaneType1.set_text(poke.types[0].name)
            except IndexError:
                self.ui.infoPaneType1.set_text("None")

            try:
                self.ui.infoPaneType2.set_text(poke.types[1].name)
            except IndexError:
                self.ui.infoPaneType2.set_text("None")

            
        except Exception as e:
            self.ui.pokeInfoBox.set_visible(False)
            self.ui.pokeInfoPaneLabel.set_visible(True)
            print e
        

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


    def populate_list(self):
        for p in self.session.query(model.PokemonType).order_by(model.PokemonType.id):
            print p.id, p.name, p.description
            self.ui.pokemonTypeStore.append([p.id, p.name, p.description])
        
    
    def __init__(self, ui, session):
        """
        """
        print "set up"
        self.session = session
        self.ui = UI(ui)
        
        self.ui.connect_signals(self)

        self.tmp_set_up_treeView()
        self.set_up_type_combobox()
        print self.typeList



    def start(self):
        """
        
        Arguments:
        - `self`:
        """
        self.ui.mainWin.show_all()
        gtk.main()


    def set_up_type_combobox(self):
        """
        
        Arguments:
        - `self`:
        """
        
        self.typeList = {}

        #Set up model
        for t in self.session.query(model.Type).order_by(model.Type.name):
            self.typeList[t.name] = t
            self.ui.typeStore.append([t.id, t.name])

        #Set up view
        renderer_text = gtk.CellRendererText()

        self.ui.newPokeType1.pack_start(renderer_text, True)
        self.ui.newPokeType1.add_attribute(renderer_text, "text", 1)

        self.ui.newPokeType2.pack_start(renderer_text, True)
        self.ui.newPokeType2.add_attribute(renderer_text, "text", 1)


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

        # make treeview searchable
        self.ui.pokemonTypeView.set_search_column(1)

        # Allow sorting on the column
        self.columnNumber.set_sort_column_id(0)

        # Allow drag and drop reordering of rows
        self.ui.pokemonTypeView.set_reorderable(True)


        

if __name__ == '__main__':
    #sqlite
    engine = sqla.create_engine('sqlite:///:pokemon.db', echo=True)
    Session = sessionmaker(bind=engine)
    model.Base.metadata.create_all(engine)
    session = Session()

    mine = MainWin('ui.xml', session)
    mine.populate_list()                
    mine.start()

    
    
