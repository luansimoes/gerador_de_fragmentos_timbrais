from json import JSONEncoder

class CompositionEncoder(JSONEncoder):
    def default(self, obj):
        return {'instruments' : obj.chord_seq,
                'timepoints' : obj.rhythm_seq,
                'pars' : obj.pars}

        
