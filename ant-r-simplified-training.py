#! /usr/bin/env python
# Time-stamp: <2021-03-23 22:02:10 christophe@pallier.org>
# License: Creative Commons Attribution-ShareAlike CC BY-SA

""" Implementation of Posner's endogeneous attention cueing task (see https://en.wikipedia.org/wiki/Posner_cueing_task)

Note: This experiment is meant to be run on FullHD (1920x1080) resolution"""

import random
import pandas as pd
import numpy as np
from expyriment import design, control, stimuli

MAX_RESPONSE_DURATION = 2000
GREY = (80, 80, 80)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

exp = design.Experiment(name="ANT-R-task",
                        text_size=25,
                        background_colour=GREY,
                        foreground_colour=WHITE)
#control.set_develop_mode()
control.initialize(exp)


trials = pd.read_csv('training.csv')
#trials = trials.sample(frac=1)

cross = stimuli.FixCross(size=(30, 30),
                         colour=BLACK,
                         line_width=4)
cross.preload()

blankscreen = stimuli.BlankScreen(colour=GREY)

# arrows_cong_left = stimuli.Picture("arrows-cong-left.png", position=(+200, 0))
# arrows_cong_left.preload()

# arrows_cong_right = stimuli.Picture("arrows-cong-right.png", position=(+200, 0))
# arrows_cong_right.preload()

# arrows_incong_left = stimuli.Picture("arrows-incong-left.png", position=(+200, 0))
# arrows_incong_left.preload()

# arrows_incong_right = stimuli.Picture("arrows-incong-right.png", position=(+200, 0))
# arrows_incong_right.preload()

### arrows


fontfile = "freesans"

# →
# ←
# ← ← ← ← ←
# → → ← → →
# → → → → →
# ← ← → ← ←

arrows_cong_left = stimuli.TextLine("← ← ←", text_font=fontfile, text_size=50)
arrows_cong_right = stimuli.TextLine("→ → →", text_font=fontfile, text_size=50)
arrows_incong_left = stimuli.TextLine("→ ← →", text_font=fontfile, text_size=50)
arrows_incong_right = stimuli.TextLine("← → ←", text_font=fontfile, text_size=50)

arrows_cong_left.preload()
arrows_cong_right.preload()
arrows_incong_left.preload()
arrows_incong_right.preload()

w, h = arrows_incong_right.surface_size
w, h = w + 20, h + 20  # add margins

shift = w * 0.7

box_left = stimuli.Rectangle((w, h), colour=BLACK, line_width=3, position=( - shift, 0))
box_left.preload()

box_right = stimuli.Rectangle((w, h), colour=BLACK, line_width=3, position=( shift, 0))
box_right.preload()

cue_left = stimuli.Rectangle((w, h), colour=WHITE, line_width=3, position=( - shift, 0))
cue_left.preload()

cue_right = stimuli.Rectangle((w, h), colour=WHITE, line_width=3, position=( shift, 0))
cue_right.preload()

exp.add_data_variable_names(['congruency', 'side', 'respkey', 'RT'])
control.start(skip_ready_screen = True)

stimuli.TextScreen("Instructions",
    """Vous allez voir des triplets de flèches comme les suivants:

               ← ← ← 
               → ← → 
               → → → 
               ← → ← 

    Votre tâche sera de déterminer, le plus rapidement possible, la direction vers la quelle point la flèche centrale
    ("gauche"  sur les deux premières lignes ci-dessus, "droite" pour les deux dernières).
    
    Les flèches qui l'entourent n'ont pas d'importance, la seule à laquelle vous devez prêter attention est celle du milieu.

    Ces flèches s'afficheront dans des boites placées à la gauche ou à la droite d'une croix de fixation placée au centre de l'écran.
    Parfois , la couleur de ces boites changera un peu avant que les flèches apparaissent, pour vous permettre de vous mieux vous préparer à répondre.
    Quand une seule boite changera, cela indiquera la position *la plus probable*  ou apparaitront les flèches.
    Pour répondre le plus vite possible, il est bénéfique de porter votre attention vers l'endroit où se trouve ce rectangle.

    Vous indiquerez votre réponse en appuyant sur la touche 'S' si la flèche du milieu pointe vers la gauche, sur 'L' si la flèche pointe vers la droite.

    
    Très important:
    1. Il faut fixer en permanence la croix centrale et ne pas déplacer les yeux.
    2. Vous devez répondre rapidement tout en évitant les erreurs. Celles-ci sont néanmoins quasi inevitables. Si vous en faites, ne vous déconcentrez pas, et concentrez vous pour l'essai suivant.

    Placez vos index sur les touches 'S' (gauche) et 'L' (droite) puis appuyez sur la barre espace pour démarrer, 

    Bonne expérience !
    """, size=(1820, 1080), text_justification=0).present()

exp.keyboard.wait()
blankscreen.present()
exp.clock.wait(1000)

for trial in trials.itertuples(index=False):
    cross.present(clear=True, update=False)
    box_left.present(clear=False, update=False)
    box_right.present(clear=False, update=True)
    exp.clock.wait(3000 + random.uniform(0, 2000))

    print(trial)
    if trial.alerting == "dbl_cue":
        cross.present(clear=True, update=False)
        cue_right.present(clear=False, update=False)
        cue_left.present(clear=False, update=True)
    elif trial.alerting == "spatial_cue":    
        if trial.cue_left:
            cross.present(clear=True, update=False)
            box_right.present(clear=False, update=False)
            cue_left.present(clear=False, update=True)
        elif trial.cue_right:
            cross.present(clear=True, update=False)
            box_left.present(clear=False, update=False)
            cue_right.present(clear=False, update=True)

    exp.clock.wait(100)

    cross.present(clear=True, update=False)
    box_left.present(clear=False, update=False)
    box_right.present(clear=False, update=True)
    exp.clock.wait(400)  # 0, 400 or 800 in the original paper

    # present the target
    if trial.target_position == 'left':
        target_x = - shift
    if trial.target_position == 'right':
        target_x =  shift

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
        
    target.reposition((target_x, 0))
    cross.present(clear=True, update=False)
    box_left.present(clear=False, update=False)
    box_right.present(clear=False, update=False)
    target.present(clear=False, update=True)

    exp.clock.wait(500)  # FIXME: this is the time the target should stay on screen
    # but we should also be able to record response during this intervall 

    key, rt = exp.keyboard.wait(duration=MAX_RESPONSE_DURATION)
    exp.data.add([key, rt])

    cross.present(clear=True, update=False)
    box_left.present(clear=False, update=False)
    box_right.present(clear=False, update=False)

    # feedback

control.end()
