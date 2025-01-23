from app.composition import Composition
from app.utils import generate_sequence, save_json, load_json
from app.encoder import CompositionEncoder

from scamp._soundfont_host import get_soundfont_presets
from edopi import Scale

from app.interface import PSGInterface

import json

PRESETS = sorted([p.name for p in get_soundfont_presets()])
PROGRAM_NAME = "Sistema Composicional Parcimonioso"



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

def main():
    
    interface = PSGInterface(PROGRAM_NAME, PRESETS, "Purple")

    composition = None


    while not interface.window_closed():

        interface.read_window()

        if interface.cur_event == "GEN":

            valid = interface.validate_fields()

            if valid:

                interface.set_state_to_generating()
                composition = generate_piece(interface.cur_values)

        elif interface.cur_event == "PLAY":
            interface.run_and_set_event(lambda: composition.play_piece(100), "END_PLAY")
            interface.set_state_to_playing()
        
        elif interface.cur_event == "END_PLAY":
            interface.set_state_to_ready()
        

        elif interface.cur_event == "EXP_FILE" and interface.get_field('EXP_FILE') != '':
            filename = interface.get_field('EXP_FILE')

            if not filename.endswith('.xml'):
                filename += '.xml'
            
            composition.export_score(filename)
            save_json(f'{filename[:-4]}.json', composition, encoder = CompositionEncoder)
                
        

        elif interface.cur_event == "Salvar Parâmetros":
            filename = interface.set_state_to_saving_parameters()
            save_json(filename, interface.cur_values)

        elif interface.cur_event == "Carregar Parâmetros":
            filename = interface.set_state_to_loading_parameters()

            try:
                par_dict = load_json(filename)    
            except Exception as e:
                print(e)
                interface.show_popup('Um erro inesperado ocorreu.', 'ERRO')
            else:
                interface.update_window(par_dict)
                interface.show_popup('Carregamento concluído com sucesso!', 'SUCESSO')  

        
        elif interface.cur_event == "inst_names":
            interface.update_inst_names()
            


    interface.close_window()

