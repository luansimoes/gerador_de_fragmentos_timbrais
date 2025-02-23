from edopi import TonalSystem, Scale
from app.utils import play_part
from scamp import Session
from fractions import Fraction

import random as rd

HUNGARIAN_MINOR_SC = Scale(12, (2,1,3,1,1,3,1), tonic = 0, name="Hungarian Minor Scale")

class Composition:
    """
    A class to represent a musical composition.
    
    Attributes:
        chord_seq (list): Sequence of chords.
        rhythm_seq (list): Sequence of rhythms.
        scale (Scale): Musical scale used in the composition.
        beats (int): Number of beats per measure.
        n_timepoints (int or list): Number of timepoints per beat or a list of timepoints for each beat.
        base_pitches (list): List of base pitches for each instrument.
        inst_names (list): List of instrument names.
        inst_weights (list): List of weights for each instrument.
        name (str): Name of the composition.
        pars (dict): Dictionary of parameters for the composition.
        score (Score): The musical score of the composition.
    """

    def __init__(self, 
                chord_seq, 
                rhythm_seq, 
                scale = HUNGARIAN_MINOR_SC, 
                beats = 4,
                n_timepoints = 4,
                base_pitches = [60],
                inst_names = ['Piano'],
                inst_weights = [70, 30],
                name = '', 
                pars = dict()):
        """
        Initializes the Composition with the given parameters.
        
        Args:
            chord_seq (list): Sequence of chords.
            rhythm_seq (list): Sequence of rhythms.
            scale (Scale): Musical scale used in the composition.
            beats (int): Number of beats per measure.
            n_timepoints (int or list): Number of timepoints per beat or a list of timepoints for each beat.
            base_pitches (list): List of base pitches for each instrument.
            inst_names (list): List of instrument names.
            inst_weights (list): List of weights for each instrument.
            name (str): Name of the composition.
            pars (dict): Dictionary of parameters for the composition.
        """
        self.chord_seq = chord_seq
        self.rhythm_seq = rhythm_seq
        self.scale = scale
        self.beats = beats
        self.base_pitches = base_pitches
        self.inst_names = inst_names
        self.n_timepoints = n_timepoints
        self.inst_weights = inst_weights

        self.name = name
        self.pars = pars

        self.score = None
    

    def export_score(self, filename='test.xml'):
        """
        Exports the musical score to a MusicXML file.
        
        Args:
            filename (str): The name of the file to export the score to.
        """
        self.play_piece(advance = True)
        self.score.export_music_xml(filename)

    def play_piece(self, tempo = 100, advance = False):
        """
        Plays the entire piece using SCAMP.
        
        Args:
            tempo (int): The tempo of the piece.
            advance (bool): Whether to fast forward the session.
        """
        # EDOpi and Scamp
        edo = TonalSystem(self.scale.system_size)
        s = Session(tempo = tempo)

        # map index to parts or attack points
        parts = dict()
        for i,nm in enumerate(self.inst_names):
            parts[i+1] = {'inst' : s.new_part(nm), 'base_pitch' : self.base_pitches[i], 'events': []}

        tps = []
        if len(self.n_timepoints) != 1:
            for x in self.n_timepoints:
                for i in range(x):
                    tps.append(Fraction(1, x))
        else:
            tps = [Fraction(1, self.n_timepoints[0]) for _ in range(self.beats * self.n_timepoints[0])]
                
        attacks = {x+1 : sum([0] + tps[:x]) for x in range(len(tps))}

        # loop through each measure
        for voicing, rhythm in zip(self.chord_seq, self.rhythm_seq):
            # join events and organize by instrument
            sep_events = {p+1 : [] for p in range(len(self.inst_names))}
            for i,p in enumerate(voicing):
                if p in parts.keys():
                    sep_events[p].append((i, attacks[rhythm[i]]))
        
            # loop through each instrument
            for p, events in sep_events.items():
                if len(events) == 0:
                    parts[p]['events'].append(('R', self.beats))
                else:
                    events.sort(key=lambda x: x[1])
                    first_event = events[0]
                    parts[p]['events'].append(('R', first_event[1]))

                    cur_event = []

                    for i,e in enumerate(events):
                        # GRAVE: EDOPI não faz o SCALE.NEXT corretamente
                        pitch, offset = e
                        real_pitch = self.scale.next(parts[p]['base_pitch'], pitch)
                        real_midi_pitch = edo.midi_pitch(real_pitch)

                        cur_event.append(real_midi_pitch)

                        next_offset = self.beats if i == len(events)-1 else events[i+1][1]

                        if next_offset != offset:
                            # Change unit measure
                            time_interval = next_offset - offset
                            unit = Fraction(time_interval, sum(self.n_timepoints))
                            available_durs = [x*unit for x in range(1, int(time_interval/unit)+1)]

                            dur = rd.choice(available_durs)
                            rest = time_interval - dur

                            parts[p]['events'].append((cur_event, dur))

                            if rest != 0:
                                parts[p]['events'].append(('R', rest))

                            cur_event = []

        # playing music with scamp
        s.start_transcribing()

        if advance:
            s.fast_forward_in_beats(400)

        [s.fork(play_part, args=(parts[i],)) for i in parts.keys()]
        s.wait_for_children_to_finish()
        performance = s.stop_transcribing()
        self.score = performance.to_score(title = 'Parsimonious System')