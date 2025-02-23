from json import JSONEncoder

class CompositionEncoder(JSONEncoder):
    def default(self, obj):
        dic =  {'instruments' : obj.chord_seq,
                'timepoints' : obj.rhythm_seq}
        for key in obj.pars:
            dic[key] = obj.pars[key]
        
        return dic

        
