#! /usr/bin/env python
# Time-stamp: <2021-03-23 22:02:10 christophe@pallier.org>
# License: Creative Commons BY-SA-NC

""" Implementation of Posner's endogeneous attention cueing task (see https://en.wikipedia.org/wiki/Posner_cueing_task)

Note: This experiment is meant to be run on FullHD (1920x1080) resolution"""

import random
import pandas as pd
import pygame
from expyriment import design, control, stimuli, misc

MAX_RESPONSE_DURATION = 1700
GREY = (80, 80, 80)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

LEFT_RESPONSE_KEY = misc.constants.K_f
LEFT_RESPONSE_KEY_CHAR = 'F'
RIGHT_RESPONSE_KEY = misc.constants.K_j
RIGHT_RESPONSE_KEY_CHAR = 'J'

INSTRUCTIONS_FRENCH = """Vous allez voir des séquences de flèches comme les suivantes :

< < < < <
> > < < <
> > > > >
< < > > >

Votre tâche sera de déterminer, le plus rapidement possible, la direction vers laquelle pointe la flèche centrale
("gauche"  sur les deux premières lignes ci-dessus, "droite" pour les deux dernières).
    
Les flèches qui l'entourent n'ont pas d'importance, la seule à laquelle vous devez prêter attention est celle du milieu.

Ces flèches s'afficheront dans une "boîte" placée au dessus ou en dessous d'une croix de fixation placée au centre de l'écran.
Parfois , la couleur de ce boîtes changera un peu avant que les flèches apparaissent, pour vous permettre de vous mieux vous préparer à répondre.
Quand une seule boîte changera, cela indiquera la position *la plus probable*  où apparaitront les flèches.

Vous indiquerez votre réponse en appuyant sur la touche '{LEFT_RESPONSE_KEY_CHAR' si la flèche du milieu pointe vers la gauche, sur '{RIGHT_RESPONSE_KEY_CHAR}' si la flèche pointe vers la droite.
   
Très important:
    1. Il faut fixer en permanence la croix centrale et ne pas déplacer les yeux.
    2. Vous devez répondre rapidement tout en évitant les erreurs. Celles-ci sont néanmoins quasi inevitables. Si vous en faites, ne vous déconcentrez pas, et concentrez vous pour l'essai suivant.

Placez vos index sur les touches '{LEFT_RESPONSE_KEY_CHAR}' (gauche) et '{RIGHT_RESPONSE_KEY_CHAR}' (droite) puis appuyez sur la barre espace pour démarrer,

Bonne expérience !
"""

##################################################################
trials = pd.read_csv('trials-vertical.csv')
trials = trials.sample(frac=1)

##################################################################
exp = design.Experiment(name="ANT-R-task",
                        text_size=25,
                        background_colour=GREY,
                        foreground_colour=WHITE)
# control.set_develop_mode()
control.initialize(exp)

##################################################################
blankscreen = stimuli.BlankScreen(colour=GREY)

cross_black = stimuli.FixCross(size=(30, 30),
                         colour=BLACK,
                         line_width=4)
cross.preload()

cross_green = stimuli.FixCross(size=(30, 30),
                             colour=GREEN,
                             line_width=4)
cross_yes.preload()

cross_red = stimuli.FixCross(size=(30, 30),
                            colour=RED,
                            line_width=4)
cross_no.preload()

fixation_crosses = dict(neutral=cross_black, yes=cross_green, no=cross_red) 

# arrows_cong_left = stimuli.Picture("arrows-cong-left.png", position=(+200, 0))
# arrows_cong_left.preload()

# arrows_cong_right = stimuli.Picture("arrows-cong-right.png", position=(+200, 0))
# arrows_cong_right.preload()

# arrows_incong_left = stimuli.Picture("arrows-incong-left.png", position=(+200, 0))
# arrows_incong_left.preload()

# arrows_incong_right = stimuli.Picture("arrows-incong-right.png", position=(+200, 0))
# arrows_incong_right.preload()

### target stimuli
# fontfile = "freemono"
fontfile = "freesans"
# →
# ←
# arrows_cong_left = stimuli.TextLine("← ← ← ← ←", text_font=fontfile, text_size=50)
# arrows_cong_right = stimuli.TextLine("→ → → → →", text_font=fontfile, text_size=50)
# arrows_incong_left = stimuli.TextLine("→ → ← → →", text_font=fontfile, text_size=50)
# arrows_incong_right = stimuli.TextLine("← ← → ← ←", text_font=fontfile, text_size=50)

arrows_cong_left = stimuli.TextLine(" < < < < < ", text_font=fontfile, text_size=50)
arrows_cong_right = stimuli.TextLine(" > > > > > ", text_font=fontfile, text_size=50)
arrows_incong_left = stimuli.TextLine(" > > < > > ", text_font=fontfile, text_size=50)
arrows_incong_right = stimuli.TextLine(" < < > < < ", text_font=fontfile, text_size=50)

arrows_cong_left.preload()
arrows_cong_right.preload()
arrows_incong_left.preload()
arrows_incong_right.preload()

# Frames
w, h = arrows_incong_right.surface_size
w, h = w + 20, h + 20  # add margins

shift = h * 1

box_down = stimuli.Rectangle((w, h), colour=BLACK, line_width=3, position=(0, -shift))
box_up = stimuli.Rectangle((w, h), colour=BLACK, line_width=3, position=(0, shift))
cue_down = stimuli.Rectangle((w, h), colour=WHITE, line_width=3, position=(0, -shift, 0))
cue_up = stimuli.Rectangle((w, h), colour=WHITE, line_width=3, position=(0, shift, 0))

box_down.preload()
box_up.preload()
cue_down.preload()
cue_up.preload()


def display_frames(color, top, down):
    

def default_screen():
    cross.present(clear=True, update=False)
    box_down.present(clear=False, update=False)
    box_up.present(clear=False, update=True)


exp.add_data_variable_names(['Arrow_direction', 'Flanker_congruency', 'Alterting',
                             'Cue_validity', 'Cue_up', 'Cue_down', 'Target_position',
                             'Response_key', 'Reaction_Time'])

#####################################################################
control.start(skip_ready_screen=True)

stimuli.TextScreen("Instructions", INSTRUCTIONS_FRENCH,
                   size=(1820, 1080), text_justification=0).present()
exp.keyboard.wait()
blankscreen.present()
exp.clock.wait(1000)
    
for trial in trials.itertuples(index=False):
    default_screen()
    exp.clock.wait(1500 + random.uniform(0, 2000))

    if trial.alerting == "dbl_cue":
        cross.present(clear=True, update=False)
        cue_up.present(clear=False, update=False)
        cue_down.present(clear=False, update=True)
    elif trial.alerting == "spatial_cue":
        if trial.cue_down:
            cross.present(clear=True, update=False)
            box_up.present(clear=False, update=False)
            cue_down.present(clear=False, update=True)
        elif trial.cue_up:
            cross.present(clear=True, update=False)
            box_down.present(clear=False, update=False)
            cue_up.present(clear=False, update=True)

    exp.clock.wait(100)
    default_screen()
    exp.clock.wait(400)  # 0, 400 or 800 in the original paper

    # select target
    if trial.arrow_direction == 'left':
        if trial.flanker_congruency == 'cong':
            target = arrows_cong_left
        else:
            target = arrows_incong_left
    else:
        if trial.flanker_congruency == 'cong':
            target = arrows_cong_right
        else:
            target = arrows_incong_right

    # display target
    if trial.target_position == 'down':
        target_pos = (0, - shift)
    if trial.target_position == 'up':
        target_pos = (0, shift)

    target.reposition(target_pos)
    default_screen()
    target.present(clear=False, update=True)
    exp.clock.wait(200)
    default_screen()
   
    key, rt = exp.keyboard.wait(duration=MAX_RESPONSE_DURATION)
    exp.data.add([key, rt])

    # feedback
    if (key == LEFT_RESPONSE_KEY and trial.arrow_direction == 'left') or \
       (key == RIGHT_RESPONSE_KEY and trial.arrow_direction == 'right'):
        cross_yes.present(clear=True)
        box_down.present(clear=False, update=False)
        box_up.present(clear=False, update=False)
    else:
        cross_no.present(clear=True)
        box_down.present(clear=False, update=False)
        box_up.present(clear=False, update=False)

    exp.clock.wait(500)
   
control.end()
