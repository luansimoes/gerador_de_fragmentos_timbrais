from abc import ABC, abstractmethod

class ParsGUIInterface(ABC):
    '''Defines a general GUI interface for a parsimonious system.
    
    Attrs:
        - program_name : str
        - cur_event : Event
        - cur_values : dict
        - window : Window
    '''

    def __init__(self, program_name):
        self.program_name = program_name
        self.cur_event, self.cur_values = (-1, -1)
        self.window = self.create_window()
    
    def validate_fields(self):
        '''This method validates the fields in the composition form. 
        Returns True for a valid form, False otherwise.'''

        n_insts = len(self.get_field('inst_names')) + 1

        # FIELD VALIDATION: inst_names
        if n_insts == 1:
            self.show_popup("É necessário escolher ao menos um instrumento!", title = "Campo Inválido")
            return False

        # FIELD VALIDATION: base_octaves
        try:
            octaves = [int(x) for x in self.get_field('base_octaves').split()]
        except:
            self.show_popup("O campo \"Oitavas Base\" só admite valores numéricos.", title = "Campo Inválido")
            return False

        if len(octaves) != n_insts -1:
            self.show_popup("O campo \"Oitavas Base\" deve conter um valor para cada instrumento escolhido.", title="Campo Inválido")
            return False

        else:
            for o in octaves:
                if o < 0 or o > 9:
                    self.show_popup("Todos os valores no campo \"Oitavas Base\" devem estar entre 0 e 9.", title = "Campo Inválido")
                    return False


        # FIELD VALIDATION: inst_weights
        try:
            weights = [float(x) for x in self.get_field('inst_weights').split()]

        except Exception:
            self.show_popup("O campo \"Probabilidades\" deve conter valores numéricos.", title = "Campo Inválido")
            return False


        if len(weights) != n_insts:
            self.show_popup("O campo \"Probabilidades\" deve conter um valor para cada instrumento escolhido, com um valor adicional para as alturas que não serão tocadas.", title="Campo Inválido")
            return False

        else:
            for w in weights:
                if w <= 0:
                    self.show_popup("O campo \"Probabilidades\" só admite números positivos.", title = "Campo Inválido")
                    return False


        # FIELD VALIDATION: edo_size
        if not self.get_field('edo_size').isdigit() or int(self.get_field('edo_size')) == 0:
            self.show_popup("O campo \"Tamanho do EDO\" deve ser um inteiro positivo.", title = "Campo Inválido")
            return False


        # FIELD VALIDATION: interval_struct
        struct = [x for x in self.get_field('interval_struct').split()]

        s = 0
        for i in struct:
            if (not i.isnumeric()) or int(i) <= 0 :
                self.show_popup("O campo \"Estrutura Intervalar\" só admite números positivos.", title = "Campo Inválido")
                return False

            s += int(i)

        if s != int(self.get_field('edo_size')):
            self.show_popup("A estrutura intervalar deve somar o tamanho do EDO.", title = "Campo Inválido")
            return False


        # FIELD VALIDATION: tonic
        if not self.get_field('tonic').isnumeric():
            self.show_popup("O campo \"Tônica\" deve conter um número.", title = "Campo Inválido")
            return False


        # FIELD VALIDATION: k
        if (not self.get_field('k').isnumeric()) or int(self.get_field('k')) == 0:
            self.show_popup("O campo \"k\" só admite números inteiros positivos.", title = "Campo Inválido")
            return False


        # FIELD VALIDATION: l
        if (not self.get_field('l').isnumeric()) or int(self.get_field('l')) >= int(self.get_field('k')):
            self.show_popup("O campo \"l\" só admite números naturais menores ou iguais a \"k\".", title = "Campo Inválido")
            return False


        # FIELD VALIDATION: measures
        if (not self.get_field('measures').isnumeric()) or int(self.get_field('measures')) == 0:
            self.show_popup("O campo \"N° de módulos\" só admite números inteiros positivos.", title = "Campo Inválido")
            return False 


        # FIELD VALIDATION: beats
        if (not self.get_field('beats').isnumeric()) or int(self.get_field('beats')) == 0:
            self.show_popup("O campo \"Beats por módulo\" só admite números inteiros positivos.", title = "Campo Inválido")
            return False


        # FIELD VALIDATION: n_timepoints
        try:
            tp_per_beat = [int(x) for x in self.get_field('n_timepoints').split()]
        except:
            self.show_popup("O campo \"Resolução por beat\" só admite valores numéricos.", title = "Campo Inválido")
            return False


        if len(tp_per_beat) == 1 and int(self.get_field('beats')) != 1:
            if (not self.get_field('n_timepoints').isnumeric()) or int(self.get_field('n_timepoints')) == 0:
                self.show_popup("O campo \"Resolução por módulo\" só admite números inteiros positivos.", title = "Campo Inválido")
                return False

        elif len(tp_per_beat) == int(self.get_field('beats')):
            for n_tp in tp_per_beat:
                if n_tp < 1:
                    self.show_popup("Todos os valores no campo \"Resolução por beat\" devem ser positivos.", title = "Campo Inválido")
                    return False

        else:
            self.show_popup("Cada beat deve ter um valor de resolução definido.", title="Campo Inválido")
            return False



        return True


    
    @abstractmethod
    def create_window(self):
        pass

    @abstractmethod
    def window_closed(self):
        pass

    @abstractmethod
    def read_window(self):
        pass

    @abstractmethod
    def get_field(self, field_name):
        pass

    @abstractmethod
    def show_popup(self, msg, title):
        pass

    @abstractmethod
    def set_state_to_generating(self):
        pass

    @abstractmethod
    def set_state_to_playing(self):
        pass

    @abstractmethod
    def set_state_to_ready(self):
        pass

    @abstractmethod
    def set_state_to_exporting(self):
        pass

    @abstractmethod
    def set_state_to_saving_parameters(self):
        pass

    @abstractmethod
    def set_state_to_loading_parameters(self):
        pass

    @abstractmethod
    def update_inst_names(self):
        pass

    @abstractmethod
    def close_window(self):
        pass


