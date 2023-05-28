import PySimpleGUI as sg

from app.composition import Composition
from app.utils import generate_sequence, save_json, load_json
from app.encoder import CompositionEncoder

from scamp._soundfont_host import get_soundfont_presets
from edopi import Scale

import json

sg.theme('Purple')

PRESETS = sorted([p.name for p in get_soundfont_presets()])
PROGRAM_NAME = "Sistema Composicional Parcimonioso"



# ------------------------------------------ LAYOUT --------------------------------------------------------
columns = {
    'inst_choice' :
        [
            [sg.Text("Escolha os instrumentos:", justification='left')],
            [sg.Listbox(values=PRESETS, select_mode='extended', key='inst_names', enable_events = True, size=(30, 20))],
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

layout = [
            [sg.Menu([['Arquivo', ['Carregar Parâmetros', 'Salvar Parâmetros']]])],
            [sg.Frame('', 
                [
                    [sg.Frame('', columns[key], size = (200, 350), key=key, border_width=2) for key in columns.keys()],
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



# ------------------------------------------ GENERATION ----------------------------------------------------
def generate_piece(fields):
    edo_size = int(fields['edo_size'])
    interval_struct = tuple(int(x) for x in fields['interval_struct'].split())
    tonic = int(fields['tonic'])

    scale = Scale(edo_size, interval_struct, tonic)
    beats = int(fields['beats'])
    base_octaves = [int(x) for x in fields['base_octaves'].split()]
    base_pitches = [(x*edo_size) + tonic for x in base_octaves]
    inst_weights = [float(x) for x in fields['inst_weights'].split()]

    inst_names = fields['inst_names']
    measures = int(fields['measures'])
    k = int(fields['k'])
    l = int(fields['l'])

    n_timepoints = [int(x) for x in fields['n_timepoints'].split()]

    n_tps = beats*n_timepoints[0] if len(n_timepoints) == 1 else sum(n_timepoints)

    chord_seq = generate_sequence(len(inst_names)+1, k, l, measures, inst_weights)
    rhythm_seq = generate_sequence(n_tps, k, l, measures)

    return Composition(chord_seq, 
                    rhythm_seq, 
                    scale = scale, 
                    beats = beats,
                    n_timepoints = n_timepoints,
                    inst_names = inst_names, 
                    base_pitches = base_pitches,
                    inst_weights = inst_weights,
                    pars = fields)


# ------------------------------------------ VALIDATION ----------------------------------------------------
def validate_fields(values):

    n_insts = len(values['inst_names']) + 1

    # FIELD VALIDATION: inst_names
    if n_insts == 1:
        sg.popup("É necessário escolher ao menos um instrumento!", title = "Campo Inválido")
        return False

    # FIELD VALIDATION: base_octaves
    try:
        octaves = [int(x) for x in values['base_octaves'].split()]
    except:
        sg.popup("O campo \"Oitavas Base\" só admite valores numéricos.", title = "Campo Inválido")
        return False

    if len(octaves) != n_insts -1:
        sg.popup("O campo \"Oitavas Base\" deve conter um valor para cada instrumento escolhido.", title="Campo Inválido")
        return False

    else:
        for o in octaves:
            if o < 0 or o > 9:
                sg.popup("Todos os valores no campo \"Oitavas Base\" devem estar entre 0 e 9.", title = "Campo Inválido")
                return False
    

    # FIELD VALIDATION: inst_weights
    try:
        weights = [float(x) for x in values['inst_weights'].split()]

    except Exception:
        sg.popup("O campo \"Probabilidades\" deve conter valores numéricos.", title = "Campo Inválido")
        return False


    if len(weights) != n_insts:
        sg.popup("O campo \"Probabilidades\" deve conter um valor para cada instrumento escolhido, com um valor adicional para as alturas que não serão tocadas.", title="Campo Inválido")
        return False

    else:
        for w in weights:
            if w <= 0:
                sg.popup("O campo \"Probabilidades\" só admite números positivos.", title = "Campo Inválido")
                return False
    

    # FIELD VALIDATION: edo_size
    if not values['edo_size'].isdigit() or int(values['edo_size']) == 0:
        sg.popup("O campo \"Tamanho do EDO\" deve ser um inteiro positivo.", title = "Campo Inválido")
        return False
    

    # FIELD VALIDATION: interval_struct
    struct = [x for x in values['interval_struct'].split()]
    
    s = 0
    for i in struct:
        if (not i.isnumeric()) or int(i) <= 0 :
            sg.popup("O campo \"Estrutura Intervalar\" só admite números positivos.", title = "Campo Inválido")
            return False
        
        s += int(i)
    
    if s != int(values['edo_size']):
        sg.popup("A estrutura intervalar deve somar o tamanho do EDO.", title = "Campo Inválido")
        return False
    

    # FIELD VALIDATION: tonic
    if not values['tonic'].isnumeric():
        sg.popup("O campo \"Tônica\" deve conter um número.", title = "Campo Inválido")
        return False
    

    # FIELD VALIDATION: k
    if (not values['k'].isnumeric()) or int(values['k']) == 0:
        sg.popup("O campo \"k\" só admite números inteiros positivos.", title = "Campo Inválido")
        return False

    
    # FIELD VALIDATION: l
    if (not values['l'].isnumeric()) or int(values['l']) >= int(values['k']):
        sg.popup("O campo \"l\" só admite números naturais menores ou iguais a \"k\".", title = "Campo Inválido")
        return False

    
    # FIELD VALIDATION: measures
    if (not values['measures'].isnumeric()) or int(values['measures']) == 0:
        sg.popup("O campo \"N° de módulos\" só admite números inteiros positivos.", title = "Campo Inválido")
        return False 
    

    # FIELD VALIDATION: beats
    if (not values['beats'].isnumeric()) or int(values['beats']) == 0:
        sg.popup("O campo \"Beats por módulo\" só admite números inteiros positivos.", title = "Campo Inválido")
        return False


    # FIELD VALIDATION: n_timepoints
    try:
        tp_per_beat = [int(x) for x in values['n_timepoints'].split()]
    except:
        sg.popup("O campo \"Resolução por beat\" só admite valores numéricos.", title = "Campo Inválido")
        return False


    if len(tp_per_beat) == 1 and int(values['beats']) != 1:
        if (not values['n_timepoints'].isnumeric()) or int(values['n_timepoints']) == 0:
            sg.popup("O campo \"Resolução por módulo\" só admite números inteiros positivos.", title = "Campo Inválido")
            return False
    
    elif len(tp_per_beat) == int(values['beats']):
        for n_tp in tp_per_beat:
            if n_tp < 1:
                sg.popup("Todos os valores no campo \"Resolução por beat\" devem ser positivos.", title = "Campo Inválido")
                return False
    
    else:
        sg.popup("Cada beat deve ter um valor de resolução definido.", title="Campo Inválido")
        return False
        


    return True


def load_pars(filename, window):
    try:
        par_dict = load_json(filename)
        print(par_dict)
        for key in par_dict.keys():
            if key in window.AllKeysDict:
                if isinstance(window[key], sg.Input):
                    window[key].update(par_dict[key])
                elif isinstance(window[key], sg.Listbox):
                    lb = window[key]
                    lb.update(set_to_index = [lb.Values.index(x) for x in par_dict[key]])
                    window['inst_text'].update(', '.join(par_dict[key]))
        
        sg.popup('Carregamento concluído com sucesso!')

    except Exception as e:
        print(e)
        sg.popup('Um erro inesperado ocorreu.')


def main():

    window = sg.Window(PROGRAM_NAME, layout, finalize = True)
    event, values = (-1, -1)

    composition = None


    while event not in [sg.WIN_CLOSED, "Sair"]:

        event, values = window.read()

        if event == "GEN":

            valid = validate_fields(values)

            if valid:

                composition = generate_piece(values)
                
                window['PLAY'].update( disabled = False )
                window['EXPORT'].update( disabled = False )

                window.refresh()
                sg.popup('Peça finalizada com sucesso!', title = "Geração Concluída")

        elif event == "PLAY":
            window.perform_long_operation(lambda: composition.play_piece(100), "END_PLAY")
            window['PLAY'].update( disabled = True )
            window['EXPORT'].update( disabled = True )
        
        elif event == "END_PLAY":
            window['PLAY'].update( disabled = False )
            window['EXPORT'].update( disabled = False )
        

        elif event == "EXP_FILE" and values['EXP_FILE'] != '':
            filename = values['EXP_FILE']

            if not filename.endswith('.xml'):
                sg.popup('Filename should end with .xml')
            else:
                composition.export_score(filename)
                save_json(f'{filename[:-4]}.json', composition, encoder = CompositionEncoder)
                
        

        elif event == "Salvar Parâmetros":
            filename = sg.popup_get_file("Escolha o caminho no qual deseja salvar o arquivo", 
                                        save_as=True,
                                        file_types=(('JSON', '*.json'), ))
            save_json(filename, values)

        elif event == "Carregar Parâmetros":
            filename = sg.popup_get_file("Escolha o arquivo que deseja carregar",
                                        file_types=(('JSON', '*.json'), ))
            
            load_pars(filename, window)
            window.refresh()
            

        
        elif event == "inst_names":
            if values['inst_names']:
                window['inst_text'].update(', '.join(values['inst_names']))

                n_insts = len(values['inst_names']) + 1
                window['base_octaves'].update(' '.join(['3']*(n_insts-1)))
                window['inst_weights'].update(' '.join([str(int(100/n_insts))]*n_insts))


    window.close()