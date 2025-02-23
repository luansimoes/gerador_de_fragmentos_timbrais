from app.interface.parsGUIinterface import ParsGUIInterface
#from parsGUIinterface import ParsGUIInterface
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter import messagebox

import threading

SP = 5

class TkInterface(ParsGUIInterface):

    def __init__(self, program_name, sound_presets):
        super().__init__(program_name, sound_presets)
        self.cur_music_thread = None

    @property
    def cur_values(self):
        return {name : self.get_field(name) for name in self.widget_vars}

    def create_window(self):
        root = ThemedTk(theme='itft1')
        root.resizable(FALSE, FALSE)
        root.title(self.program_name)
        root.option_add('*tearOff', FALSE)

        self.widget_vars = {}
        self.buttons = {}

        # Defining main frame
        outer_frame = ttk.Frame(root)
        outer_frame.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        menu = self.create_menu(root)

        column_frame = ttk.Frame(outer_frame, padding="24 8 24 8", width=900, height=400)
        column_frame.grid(column=0, row=2, sticky=(N, W, E, S))

        columns = self.create_columns(column_frame)

        button_frame = ttk.Frame(outer_frame, padding=f"0 {4*SP}")
        button_frame.grid(column=0, row=3, sticky=(N,S))
        button_row = self.create_button_row(button_frame, root)

        exit_frame = ttk.Frame(outer_frame, padding=f"0 {2*SP}")
        exit_frame.grid(column=0, row=4, sticky=(S, E))
        b = ttk.Button(exit_frame, text="Sair", command=root.destroy)
        b.grid(padx=2*SP)
        
        return root

    def create_menu(self, frame):
        menubar = Menu(frame)

        menu_file = Menu(menubar, tearoff = 0)
        menubar.add_cascade(menu=menu_file, label='Arquivo')
        menu_file.add_command(label='Salvar Parâmetros', command=lambda:self.window.event_generate("<<SAVE_PARS>>"))
        menu_file.add_command(label='Carregar Parâmetros', command=lambda:self.window.event_generate("<<LOAD_PARS>>"))

        frame.config(menu=menubar)

        return menubar

    def create_columns(self, root):
        c1 = ttk.Frame(root, padding=f"{SP} {SP} {2*SP} {2*SP}", width=300, height=350, borderwidth=2, relief=RIDGE)
        c2 = ttk.Frame(root, padding=f"{SP} {SP} {2*SP} {2*SP}", width=300, height=350, borderwidth=2, relief=RIDGE)
        c3 = ttk.Frame(root, padding=f"{SP} {SP} {2*SP} {2*SP}", width=300, height=350, borderwidth=2, relief=RIDGE)
        c4 = ttk.Frame(root, padding=f"{SP} {SP} {2*SP} {2*SP}", width=300, height=350, borderwidth=2, relief=RIDGE)

        c1.grid(column=0, row=0, sticky=(N, W, E, S), padx=12, pady=24)
        c2.grid(column=1, row=0, sticky=(N, W, E, S), padx=12, pady=24)
        c3.grid(column=2, row=0, sticky=(N, W, E, S), padx=12, pady=24)
        c4.grid(column=3, row=0, sticky=(N, W, E, S), padx=12, pady=24)

        c1.columnconfigure(1, weight=1)
        c2.columnconfigure(1, weight=1)
        c3.columnconfigure(1, weight=1)
        c4.columnconfigure(1, weight=1)

        c1.grid_propagate(0)
        c2.grid_propagate(0)
        c3.grid_propagate(0)
        c4.grid_propagate(0)

        self.create_inst_choice(c1)
        self.create_inst_config(c2)
        self.create_pitch_config(c3)
        self.create_rhythm_config(c4)

        return [c1, c2, c3, c4]

    def create_inst_choice(self, frame):
        ttk.Label(frame, text = "Escolha os instrumentos: ", font="TkFixedFont").grid(column=1, row=1, sticky=(N, W))

        self.widget_vars["inst_names"] = choicesvar = StringVar(value=self.sound_presets)
        lb = Listbox(frame, height=15, listvariable=self.widget_vars["inst_names"], selectmode="extended")
        lb.bind("<<ListboxSelect>>", lambda e: self.window.event_generate("<<INST_NAMES>>"))
        lb.grid(column=1, row=2, sticky=(W, N, E, S))
        self.list_box = lb

        scroll = ttk.Scrollbar(frame)
        scroll.grid(column=2, row=2, sticky=(N, S))

        lb.config(yscrollcommand = scroll.set)
        scroll.config(command = lb.yview)

        frame.rowconfigure(1, weight=1)

    def create_inst_config(self, frame):
        # First label
        ttk.Label(frame, text = "Instrumentos escolhidos: ", font="TkFixedFont").grid(column=1, row=1, sticky=(N, W))

        # Frame with instrument names
        list_frame = ttk.Frame(frame, height=35)
        list_frame.grid(column=1, row=2, sticky=(N, W, E, S))
        self.widget_vars["inst_text"] = StringVar(value = "")
        l1 = ttk.Label(list_frame, textvariable=self.widget_vars["inst_text"], padding=f"0 {SP} 0 {SP}")
        l1.grid(sticky=(N, W, E, S))
        list_frame.rowconfigure(1, weight=1)
        frame.rowconfigure(2, weight=1)
        list_frame.grid_propagate(0)

        # Second label
        l2 = ttk.Label(frame, text = "Oitavas base: ", font="TkFixedFont", padding=f"0 {2*SP} 0 {SP}")
        l2.grid(column=1, row=3, sticky=(N, W))
        self.widget_vars['base_octaves'] = StringVar()
        ttk.Entry(frame, textvariable=self.widget_vars['base_octaves'], justify='left').grid(column=1, row=4, sticky=(N, W, E))
        frame.rowconfigure(4, weight=1)

        # Third label
        l3 = ttk.Label(frame, text = "Probabilidades: ", font="TkFixedFont", padding=f"0 {2*SP} 0 {SP}")
        l3.grid(column=1, row=5, sticky=(N, W))
        self.widget_vars['inst_weights'] = StringVar()
        ttk.Entry(frame, textvariable=self.widget_vars['inst_weights'], justify='left').grid(column=1, row=6, sticky=(N, W, E))

    def create_pitch_config(self, frame):
        l1 = ttk.Label(frame, text = "Tamanho do EDO: ", font="TkFixedFont", padding=f"0 0 0 {SP}")
        l1.grid(column=1, row=1, sticky=(N, W))
        self.widget_vars['edo_size'] = StringVar(value="12")
        ttk.Entry(frame, textvariable=self.widget_vars['edo_size'], justify='left').grid(column=1, row=2, sticky=(N, W, E))
        frame.rowconfigure(2, weight=1)

        l2 = ttk.Label(frame, text = "Estrutura intervalar da escala: ", font="TkFixedFont", padding=f"0 {2*SP} 0 {SP}")
        l2.grid(column=1, row=3, sticky=(N, W))
        self.widget_vars['interval_struct'] = StringVar(value="2 2 1 2 2 2 1")
        ttk.Entry(frame, textvariable=self.widget_vars['interval_struct'], justify='left').grid(column=1, row=4, sticky=(N, W, E))
        frame.rowconfigure(4, weight=1)

        l3 = ttk.Label(frame, text = "Tônica: ", font="TkFixedFont", padding=f"0 {2*SP} 0 {SP}")
        l3.grid(column=1, row=5, sticky=(N, W))
        self.widget_vars['tonic'] = StringVar(value="0")
        ttk.Entry(frame, textvariable=self.widget_vars['tonic'], justify='left').grid(column=1, row=6, sticky=(N, W, E))
        frame.rowconfigure(6, weight=1)

        l4 = ttk.Label(frame, text = "N° de alturas (k): ", font="TkFixedFont", padding=f"0 {2*SP} 0 {SP}")
        l4.grid(column=1, row=7, sticky=(N, W))
        self.widget_vars['k'] = StringVar(value="7")
        ttk.Entry(frame, textvariable=self.widget_vars['k'], justify='left').grid(column=1, row=8, sticky=(N, W, E))
        frame.rowconfigure(8, weight=1)


        l5 = ttk.Label(frame, text = "Critério de Parcimônia (l): ", font="TkFixedFont", padding=f"0 {2*SP} 0 {SP}")
        l5.grid(column=1, row=9, sticky=(N, W))
        self.widget_vars['l'] = StringVar(value="0")
        ttk.Entry(frame, textvariable=self.widget_vars['l'], justify='left').grid(column=1, row=10, sticky=(N, W, E))

    def create_rhythm_config(self, frame):
        l1 = ttk.Label(frame, text = "Número de módulos: ", font="TkFixedFont", padding=f"0 0 0 {SP}")
        l1.grid(column=1, row=1, sticky=(N, W, E, S))
        self.widget_vars['measures'] = StringVar(value="16")
        ttk.Entry(frame, textvariable=self.widget_vars['measures'], justify='left').grid(column=1, row=2, sticky=(N, W, E))
        frame.rowconfigure(2, weight=1)


        l2 = ttk.Label(frame, text = "Número de beats por módulo: ", font="TkFixedFont", padding=f"0 {2*SP} 0 {SP}")
        l2.grid(column=1, row=3, sticky=(N, W, E, S))
        self.widget_vars['beats'] = StringVar(value="4")
        ttk.Entry(frame, textvariable=self.widget_vars['beats'], justify='left').grid(column=1, row=4, sticky=(N, W, E))
        frame.rowconfigure(4, weight=1)

        l3 = ttk.Label(frame, text = "Resolução por beat: ", font="TkFixedFont", padding=f"0 {2*SP} 0 {SP}")
        l3.grid(column=1, row=5, sticky=(N, W, E, S))
        self.widget_vars['n_timepoints'] = StringVar(value="4")
        ttk.Entry(frame, textvariable=self.widget_vars['n_timepoints'], justify='left').grid(column=1, row=6, sticky=(N, W, E))

    def create_button_row(self, parent, root):
        b1 = ttk.Button(parent, text="Gerar", command=lambda : self.window.event_generate("<<GEN>>"))
        b1.grid(column=1, row=2, padx=SP)

        b2 = ttk.Button(parent, text="Reproduzir", state="disabled", command=lambda : self.window.event_generate("<<PLAY>>"))
        b2.grid(column=2, row=2, padx=SP)

        b3 = ttk.Button(parent, text="Exportar", state="disabled", command=lambda : self.window.event_generate("<<EXP_FILE>>"))
        b3.grid(column=3, row=2, padx=SP)

        self.buttons["GEN"] = b1
        self.buttons["PLAY"] = b2
        self.buttons["EXP"] = b3
    
    def run_mainloop(self):
        self.window.mainloop()

    def window_closed(self):
        pass

    def read_window(self):
        pass
 
    def get_field(self, field_name):
        if field_name == "inst_names":
            names = eval(self.widget_vars["inst_names"].get())
            indices = self.list_box.curselection()
            
            return [names[i] for i in indices]
        return self.widget_vars[field_name].get()
    
    def get_exporting_filename(self):
        filename = filedialog.asksaveasfilename()
        if filename == "":
            filename = "minha_composicao.xml"
        elif not filename.endswith('.xml'):
            filename += '.xml'
        return filename
    
    def show_popup(self, msg, title):
        messagebox.showinfo(message=msg, title=title)
    
    def set_state_to_generating(self):
        self.buttons['PLAY']["state"] = "normal"
        self.buttons['EXP']["state"] = "normal"

        self.show_popup('Geração Concluída!', title="Aviso")
    
    def set_state_to_playing(self):
        self.buttons['PLAY']["state"] = "disabled"
        self.buttons['EXP']["state"] = "disabled"
    
    def set_state_to_ready(self):
        self.buttons['PLAY']["state"] = "normal"
        self.buttons['EXP']["state"] = "normal"
    
    def set_state_to_saving_parameters(self):
        filename = filedialog.asksaveasfilename(filetypes=(('JSON', '*.json'), ), title="Escolha o caminho no qual deseja salvar o arquivo")
        if filename == "":
            filename = "meus_parametros.json"
        elif not filename.endswith('.json'):
            filename += '.json'
        return filename
    
    def set_state_to_loading_parameters(self):
        filename = filedialog.askopenfilename(filetypes=(('JSON', '*.json'), ), title="Escolha o arquivo que deseja carregar")
        return filename
    
    def update_inst_names(self):
        inst_names = self.get_field("inst_names")
        self.widget_vars['inst_text'].set('\n'.join(inst_names))

        n_insts = len(inst_names) + 1
        self.widget_vars['base_octaves'].set(' '.join(['3']*(n_insts-1)))
        self.widget_vars['inst_weights'].set(' '.join([str(int(100/n_insts))]*n_insts))
    
    def update_window(self, par_dict):
        self.list_box.select_clear(0, len(self.sound_presets)-1)

        for par_name in par_dict:
            if par_name in self.widget_vars and par_name != "inst_names":
                self.widget_vars[par_name].set(par_dict[par_name])
        
        for ind in par_dict["inst_names"]:
            self.list_box.selection_set(self.sound_presets.index(ind))
    
    def run_and_set_event(self, audio_func, event_name):
        thread = threading.Thread(target=lambda:(audio_func(), self.window.event_generate(event_name)), daemon=True)
        thread.start()

    def close_window(self):
        pass

    def play(self, audio_func, event_name):
        self.run_and_set_event(audio_func, event_name)
        self.set_state_to_playing()

    def external_bind(self, event, action, *pars):
        self.window.bind(event, lambda e: action(*pars))


if __name__ == '__main__':
    interface = TkInterface("TESTE", list(range(40)))
    interface.external_bind("<<GEN>>", lambda a, b: print(a,b), 1, 2)
    interface.run_mainloop()
