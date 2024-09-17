ANT-R task
=============

christophe@pallier.org

The repository <https://github.com/chrplr/Posner_attention_networks_taks> contains several Python scripts implementing variants of the ANT task.

`ant-r-classic.py` is a script implementing the ANT-R task described in Fan, J. et al (2009). 

![](ANT-R-task-Fan_et_al_2009.png)


The other scripts (`ant-v.py`, `posner-task-simplified.py`, ...) are simplified versions.

### Reference

Fan, J., Gu, X., Guise, K.G., Liu, X., Fossella, J., Wang, H., and Posner, M.I. (2009). Testing the behavioral interaction and integration of attentional networks. *Brain and Cognition* 70, 209–220. 10.1016/j.bandc.2009.02.002.



Installation
--------------

First, you need to install:

* Python3 (e.g. [miniconda](https://docs.conda.io/en/latest/miniconda.html)).
* the [expyriment.org](expyriment.org) module (see <https://docs.expyriment.org/Installation.html>). 
* [git](https://git-scm.com/download/)


Then, to install the ANT scripts on your computer, in a Terminal (e.g. Git Bash for Windows), type the follwing command line:

    git clone https://github.com/chrplr/Posner_attention_networks_task.git
	cd Posner_attention_networks_task


To run the experiment (one block of 72 trials), simply execute the following command in a terminal ("Anancoda Prompt" if running under Windows with Anaconda Python installed): 

    python ant-v.py
	
Results are saved in the subfolder `data`, in files named `ant-v_XX_aaaammddhhmm.xpd` where XX is the participant's number. 
	
License
--------

Attribution-ShareAlike: CC BY-SA 4.0

<https://creativecommons.org/licenses/by-sa/4.0/legalcode.txt>


Methods (from Fan et al., 2009)
------------------------------------

Stimuli consist of a row of five horizontal black arrows (one central target plus four flankers, two on each side), pointing leftward or rightward,against a gray background. A single arrow subtends 0.58° of visual angle and the contours of adjacent arrows are separated by 0.06° of visual angle, so that the target + flanker array subtends a total of 3.27° of visual angle. 



Participants’ task is to identify the direction of the center arrow by pressing a key with the index finger of the left hand for the left direction and a key with the index finger of the right hand for the right direction, while ignoring the spatial location (left or right) of the target relative to the fixation crosshair. Participants are instructed to make their response to the direction of the center target as quickly and accurately as possible. 

A cue, in the form of cue box flashing, may be shown before the target appears, which may or may not help the participants’ target detection depending on the cue conditions. There are three cue conditions in each run: 
* no-cue (no-cue box flashes before the target appears; 12 trials), 
* double-cue (both cue boxes flash before the target appears, so the cue is only temporally informative; 12 trials),
* spatial-cue (one cue box flashes before the target appears, so the cue is temporally and possibly spatially informative; 48 trials). 

RTs for the no- and double-cue conditions are used to assess the alerting benefit. 

To introduce the orienting component, a spatial cue and the subsequent stimulus are presented 4.69° left or right of a fixation crosshair continuously shown in the center of the screen. Participants have to shift attention from the fixation point to the target stimulus on each trial in order to determine the proper response. If attentional movements occur with a speed of about 8 ms/degree (Tsal, 1983), this visual angle should result in a cost of at least 37 ms. The validity of the spatial-cue is manipulated in order to measure the disengage and move operations (see (Posner et al., 1984). Specifically, 75% of the 48 spatial-cues (36 trials) are valid and 25% (12 trials) are invalid. The probability of valid cue is the sum of the individual conditions of no-cue, double-cue, and invalid cue. 
To introduce the conflict effect, the target (center arrow) is flanked on either side by two arrows of the same direction (congruent condition), or of the opposite direction (incongruent condition). To challenge the executive control function, double conflict that combines the flanker conflict effect (Eriksen & Eriksen, 1974) and the location conflict (Simon) effect (Simon & Berbaum, 1990) areintroduced. There are two flanker congruency (congruent, incongruent) and two location congruency (congruent, incongruent) conditions. 

For example, assume that the target is displayed on the right side of the fixation. If the center target points to right and the flankers point to right, this is the flanker congruent with location congruent condition. If the center target points to right and the flankers point to left, this is the flanker incongruent with location congruent condition. If the center target points to left and the flankers point to left, this is the flanker congruent with location incongruent condition. If the center target points to left and the flankers point to right side, this is the flanker incongruent with location incongruent condition. 

A fixation cross is visible at the center of the screen throughout the duration of the task. In each trial, depending on the condition, either a transient cue (brightening of the cue box surrounding the stimulus row) is presented for 100 ms (the cued conditions) or the stimulus display remains unchanged (the nocue condition). After a variable duration (either 0, 400, or 800 ms, mean = 400 ms), the target and flankers are presented and remain visible for 500 ms. Cue-to-target intervals are selected based on previous studies on normal participants and patients (Fan et al., 2002; Posner et al., 1984). The duration between the offset of the target and the onset of the next trial is varied systematically, approximating an exponential distribution ranging from 2000 to 12,000 ms and having a mean of 4000 ms (10 intervals from 2000 to 4250 ms with an increase step of 250 ms, then one 4750 ms interval and one 12,000 ms interval). The mean trial duration is 5000 ms. The response collection window closes 1700 ms after the onset of the target and flankers as used in our original study (Fan et al. 2002).

The experiment consists of 4 runs, each with 72 test trials. Across 2 runs consisting of a total of 144 trials: (1) The cue conditions are classified into six cue cells (one for no-cue, one for double-cue, one for invalid spatial-cue, and three for valid spatialcue) although there are only four cue types (no-cue, double-cue, invalid spatial-cue, valid spatial-cue). This is for counterbalancing purposes because the number of trials with valid cues is equal to the sum of the number of trials under the no-cue, invalid cue, and double-cue conditions. The order of the cue presentation is predetermined to ensure that each cue type is followed by every other cue type equally as often; (2) The order for 24 combinations of the 3 cue-to-target intervals (0, 400, and 800 ms) by 2 flanker congruencies (congruent, incongruent) by 2 target locations (left, right) by 2 target directions (left, right) is nested within each cue condition and is randomized; (3) Since the 12 intervals between target and next trial do not lend themselves to counterbalancing within 24 trials for each cue type, the 2 x 12 intervals are randomized within each cue type until the Spearman’s rank correlation between the 24 ranks (for the 24 combinations) x 6 cue types and 12 ranks (for 12 interval pairs) x 12 repetitions is less than .005. The 144 trials are evenly split into 2 runs with 72 trials and the same run duration in each. The same arrangement is repeated once resulting in 4 runs in total. The total duration for each run is 420 s. The total time required to complete this task is about 30 min.
