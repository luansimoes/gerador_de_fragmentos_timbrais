from app.interface.parsGUIinterface import ParsGUIInterface
import PySimpleGUI as sg


# ------------------------------------------ LAYOUT --------------------------------------------------------
COLUMNS = {
        'inst_choice' :
            [
                [sg.Text("Escolha os instrumentos:", justification='left')],
                [sg.Listbox(values=[], select_mode='extended', key='inst_names', enable_events = True, size=(30, 20))],
            ],
        'inst_config' :
            [
                [sg.Text("Instrumentos Escolhidos:")],
                [sg.Text("", key="inst_text")],
                [sg.VPush()],
                [sg.Text("Oitavas base:", justification='left')],
                [sg.Input(size = (25,0), key = 'base_octaves')],
                [sg.VPush()],
                [sg.Text("Probabilidades:", justification='left')],
                [sg.Input(size = (25,0), key = 'inst_weights')],
                [sg.VPush()],
            ], 
        'pitch_config' :

            [
                [sg.Text("Tamanho do EDO:", justification='left')],
                [sg.Input('12', size = (25,0), key = 'edo_size')],
                [sg.VPush()],
                [sg.Text("Estrutura intervalar da escala:", justification='left')],
                [sg.Input('2 2 1 2 2 2 1', size = (25,0), key = 'interval_struct')],
                [sg.VPush()],
                [sg.Text("Tônica:", justification='left')],
                [sg.Input('0', size = (25,0), key = 'tonic')],
                [sg.VPush()],
                [sg.Text("N° de alturas (k):", justification='left')],
                [sg.Input('7', size = (25,0), key = 'k')],
                [sg.VPush()],
                [sg.Text("Critério de parcimônia (l):", justification='left')],
                [sg.Input('0', size = (25,0), key = 'l')]
            ],
        'rhythm_config' : 
            [
                [sg.Text("N° de módulos:", justification='left')],
                [sg.Input('16', size = (25,0), key = 'measures')],
                [sg.VPush()],
                [sg.Text("N° de beats por módulo:", justification='left')],
                [sg.Input('4', size = (25,0), key = 'beats')],
                [sg.VPush()],
                [sg.Text("Resolução por beat:", justification='left')],
                [sg.Input('4', size = (25,0), key = 'n_timepoints')],
                [sg.VPush()],
            ],
        }

LAYOUT = [
            [sg.Menu([['Arquivo', ['Carregar Parâmetros', 'Salvar Parâmetros']]])],
            [sg.Frame('', 
                [
                    [sg.Frame('', COLUMNS[key], size = (200, 350), key=key, border_width=2) for key in COLUMNS],
                    ], size=(900, 400), border_width=0, element_justification='c')
                ],
                [
                        sg.Push(), 
                        sg.Button("Gerar", key = 'GEN'), 
                        sg.Button("Reproduzir", key = 'PLAY', disabled = True),
                        sg.InputText("", key = 'EXP_FILE', enable_events = True, visible = False),
                        sg.FileSaveAs("Exportar", key = 'EXPORT', target = 'EXP_FILE', disabled = True),
                        sg.Push()
                ],
                [sg.Text('', size=(0, 1))],
                [sg.Push(), sg.Push(), sg.Button('Sair')],
                ]


#TODO: Reorganizar para funcionar novamente no programa
class PSGInterface(ParsGUIInterface):
    
    def __init__(self, program_name, sound_presets, theme="Purple"):
        super().__init__(program_name, sound_presets)
        sg.theme(theme)

    def create_window(self):
        window = sg.Window(self.program_name, LAYOUT, finalize = True)
        window['inst_names'].update(values=self.sound_presets)
        return window

    def window_closed(self):
        return self.window.was_closed() or self.cur_event=='Sair'
    
    def read_window(self):
        self.cur_event, self.cur_values = self.window.read()
    
    def set_state_to_generating(self):
        self.window['PLAY'].update( disabled = False )
        self.window['EXPORT'].update( disabled = False )

        self.window.refresh()
        self.show_popup('Peça finalizada com sucesso!', title = "Geração Concluída")

    def set_state_to_ready(self):
        self.window['PLAY'].update( disabled = False )
        self.window['EXPORT'].update( disabled = False )

    def set_state_to_saving_parameters(self):
        return sg.popup_get_file("Escolha o caminho no qual deseja salvar o arquivo", 
                                        save_as=True,
                                        file_types=(('JSON', '*.json'), ))
    
    def set_state_to_loading_parameters(self):
        return sg.popup_get_file("Escolha o arquivo que deseja carregar",
                                        file_types=(('JSON', '*.json'), ))
    
    def set_state_to_playing(self):
        self.window['PLAY'].update( disabled = True )
        self.window['EXPORT'].update( disabled = True )
    
    def show_popup(self, msg, title):
        sg.popup(msg, title=title)
    
    def run_and_set_event(self, audio_func, event_name):
        self.window.perform_long_operation(audio_func, event_name)

    def update_window(self, par_dict):
        for key in par_dict.keys():
            if key in self.window.AllKeysDict:
                if isinstance(self.window[key], sg.Input):
                    self.window[key].update(par_dict[key])
                elif isinstance(self.window[key], sg.Listbox):
                    lb = self.window[key]
                    lb.update(set_to_index = [lb.Values.index(x) for x in par_dict[key]])
                    self.window['inst_text'].update('\n'.join(par_dict[key]))

        self.window.refresh()

    def update_inst_names(self):
        if self.cur_values['inst_names']:
            self.window['inst_text'].update('\n'.join(self.cur_values['inst_names']))

            n_insts = len(self.cur_values['inst_names']) + 1
            self.window['base_octaves'].update(' '.join(['3']*(n_insts-1)))
            self.window['inst_weights'].update(' '.join([str(int(100/n_insts))]*n_insts))

    def get_field(self, field_name):
        return self.cur_values[field_name]
    
    def close_window(self):
        self.window.close()

    def external_bind(self, event, action):
        pass