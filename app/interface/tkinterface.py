#from app.interface.parsGUIinterface import ParsGUIInterface
from parsGUIinterface import ParsGUIInterface
from tkinter import *
from tkinter import ttk

SP = 5

class TkInterface(ParsGUIInterface):

    def __init__(self, program_name, sound_presets):
        super().__init__(program_name, sound_presets)
        self.window.mainloop()

    def create_window(self):
        root = Tk()
        root.title(self.program_name)

        self.widget_vars = {}

        # Defining main frame
        outer_frame = ttk.Frame(root)
        outer_frame.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        column_frame = ttk.Frame(outer_frame, padding="24 8 24 8", width=900, height=400)
        column_frame.grid(column=0, row=2, sticky=(N, W, E, S))

        columns = self.create_columns(column_frame)

        button_frame = ttk.Frame(outer_frame, padding=f"0 {4*SP}")
        button_frame.grid(column=0, row=3, sticky=(N,S))
        button_row = self.create_button_row(button_frame)

        exit_frame = ttk.Frame(outer_frame, padding=f"0 {2*SP}")
        exit_frame.grid(column=0, row=4, sticky=(S, E))
        b = ttk.Button(exit_frame, text="Sair")
        b.grid(padx=2*SP)
        
        return root

    def create_columns(self, root):
        columns = []
        for i in range(4):
            columns.append(ttk.Frame(root, padding="12 12 24 24", width=200, height=350, borderwidth=2))
            columns[i].grid(column=i, row=0, sticky=(N, W, E, S))

        self.create_inst_choice(columns[0])
        self.create_inst_config(columns[1])
        self.create_pitch_config(columns[2])
        self.create_rhythm_config(columns[3])

        return columns

    def create_inst_choice(self, frame):
        ttk.Label(frame, text = "Escolha os instrumentos: ", font="TkFixedFont").grid(column=1, row=1, sticky=(N, W))
        self.widget_vars["inst_names"] = choicesvar = StringVar(value=self.sound_presets)
        lb = Listbox(frame, width=25, height=15, listvariable=self.widget_vars["inst_names"])
        lb.grid(column=1, row=2, sticky=(W, N), pady=SP)


    def create_inst_config(self, frame):
        #First label
        ttk.Label(frame, text = "Instrumentos escolhidos: ", font="TkFixedFont").grid(column=1, row=1, sticky=(N, W))

        # Frame with instrument names
        list_frame = ttk.Frame(frame, height=400)
        list_frame.grid(column=1, row=2, sticky=(N, W, E, S))
        self.widget_vars["inst_text"] = l1 = ttk.Label(list_frame, text="", padding=f"0 {SP} 0 {SP}")
        l1.grid(sticky=(N, W, E, S))

        # Second label
        l2 = ttk.Label(frame, text = "Oitavas base: ", font="TkFixedFont", padding=f"0 {2*SP} 0 {SP}")
        l2.grid(column=1, row=3, sticky=(N, W))
        self.widget_vars['base_octaves'] = StringVar()
        ttk.Entry(frame, textvariable=self.widget_vars['base_octaves'], justify='left').grid(column=1, row=4, sticky=(N, W, E))

        # Third label
        l3 = ttk.Label(frame, text = "Probabilidades: ", font="TkFixedFont", padding=f"0 {2*SP} 0 {SP}")
        l3.grid(column=1, row=5, sticky=(N, W))
        self.widget_vars['inst_weights'] = StringVar()
        ttk.Entry(frame, textvariable=self.widget_vars['inst_weights'], justify='left').grid(column=1, row=6, sticky=(N, W, E))

    def create_pitch_config(self, frame):
        l1 = ttk.Label(frame, text = "Tamanho do EDO: ", font="TkFixedFont", padding=f"0 0 0 {SP}")
        l1.grid(column=1, row=1, sticky=(N, W))
        self.widget_vars['edo_size'] = StringVar()
        ttk.Entry(frame, textvariable=self.widget_vars['edo_size'], justify='left').grid(column=1, row=2, sticky=(N, W, E))

        l2 = ttk.Label(frame, text = "Estrutura intervalar da escala: ", font="TkFixedFont", padding=f"0 {2*SP} 0 {SP}")
        l2.grid(column=1, row=4, sticky=(N, W))
        self.widget_vars['interval_struct'] = StringVar()
        ttk.Entry(frame, textvariable=self.widget_vars['interval_struct'], justify='left').grid(column=1, row=5, sticky=(N, W, E))

        l3 = ttk.Label(frame, text = "Tônica: ", font="TkFixedFont", padding=f"0 {2*SP} 0 {SP}")
        l3.grid(column=1, row=7, sticky=(N, W))
        self.widget_vars['tonic'] = StringVar()
        ttk.Entry(frame, textvariable=self.widget_vars['tonic'], justify='left').grid(column=1, row=8, sticky=(N, W, E))

        l4 = ttk.Label(frame, text = "N° de alturas (k): ", font="TkFixedFont", padding=f"0 {2*SP} 0 {SP}")
        l4.grid(column=1, row=10, sticky=(N, W))
        self.widget_vars['k'] = StringVar()
        ttk.Entry(frame, textvariable=self.widget_vars['k'], justify='left').grid(column=1, row=11, sticky=(N, W, E))

        l5 = ttk.Label(frame, text = "Critério de Parcimônia (l): ", font="TkFixedFont", padding=f"0 {2*SP} 0 {SP}")
        l5.grid(column=1, row=13, sticky=(N, W))
        self.widget_vars['l'] = StringVar()
        ttk.Entry(frame, textvariable=self.widget_vars['l'], justify='left').grid(column=1, row=14, sticky=(N, W, E))

    def create_rhythm_config(self, frame):
        l1 = ttk.Label(frame, text = "Número de módulos: ", font="TkFixedFont", padding=f"0 0 0 {SP}")
        l1.grid(column=1, row=1, sticky=(N, W, E, S))
        self.widget_vars['measures'] = StringVar()
        ttk.Entry(frame, textvariable=self.widget_vars['measures'], justify='left').grid(column=1, row=2, sticky=(N, W, E))

        l2 = ttk.Label(frame, text = "Número de beats por módulo: ", font="TkFixedFont", padding=f"0 {2*SP} 0 {SP}")
        l2.grid(column=1, row=6, sticky=(N, W, E, S))
        self.widget_vars['beats'] = StringVar()
        ttk.Entry(frame, textvariable=self.widget_vars['beats'], justify='left').grid(column=1, row=7, sticky=(N, W, E))

        l3 = ttk.Label(frame, text = "Resolução por beat: ", font="TkFixedFont", padding=f"0 {2*SP} 0 {SP}")
        l3.grid(column=1, row=11, sticky=(N, W, E, S))
        self.widget_vars['n_timepoints'] = StringVar()
        ttk.Entry(frame, textvariable=self.widget_vars['n_timepoints'], justify='left').grid(column=1, row=12, sticky=(N, W, E))

    def create_button_row(self, root):
        b1 = ttk.Button(root, text="Gerar")
        b1.grid(column=1, row=2, padx=SP)

        b2 = ttk.Button(root, text="Reproduzir", state="disabled")
        b2.grid(column=2, row=2, padx=SP)

        b3 = ttk.Button(root, text="Exportar", state="disabled")
        b3.grid(column=3, row=2, padx=SP)


    
    def window_closed(self):
        pass

    
    def read_window(self):
        pass

    
    def get_field(self, field_name):
        pass

    
    def show_popup(self, msg, title):
        pass

    
    def set_state_to_generating(self):
        pass

    
    def set_state_to_playing(self):
        pass

    
    def set_state_to_ready(self):
        pass

    
    def set_state_to_saving_parameters(self):
        pass

    
    def set_state_to_loading_parameters(self):
        pass

    
    def update_inst_names(self):
        pass

    
    def update_window(self, par_dict):
        pass

    
    def run_and_set_event(self, audio_func, event_name):
        pass

    
    def close_window(self):
        pass


if __name__ == '__main__':
    TkInterface("TESTE", [])