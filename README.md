# Complex Puzzle Solution Algorithm

_I implemented a made-up solution for a 
little game, its rules are documented below,
and made a terminal interface to help
show how the algorithm works and to make 
it accessible without reading through the code._

#################################<br>
1- **Game's Rules**              <br>
2- **The Algorithm**             <br>
3- **How to Use**                <br>
#################################<br>

======================================
## GAME'S RULES
======================================

The game consists of a hidden 4 slot password, each slot can consist of one of 4 symbols.
example: [ 0 1 3 3 ]
And 4 guesses as to what the password is.

For each guess, you get feedback on each slot:                               <br>
0 > Slot's guess is not correct AND does not exist in any of the other slots.<br>
1 > Slot's guess is correct but not in its current slot.                     <br>
2 > Slot's guess is correct in its current slot.                             <br>

Based on the feedback, you can come up with a more educated "next guess".

**_This program is an algorithm that solves this game with maximum 4 tries every single time._**

======================================
## THE ALGORITHM
======================================

It starts by initializing an array of "possible choices" for each slot.<br>
<pre>
[slot1] -> [0, 1, 2, 3]
[slot2] -> [0, 1, 2, 3]
[slot3] -> [0, 1, 2, 3]
[slot4] -> [0, 1, 2, 3]
</pre><br>
Firstly, it makes a totally random first guess. Then based on the feedback it does one of the following things on each slot:<br>
_If the slot's guess is wrong, it removes the guess from the possibilities array of all slots._
_If the slot's guess is right, it ignores the slot for the rest of the evaluation._
_If the slot's guess is right but not in the current slot, it removes the guess from the current slot's possibilities array
and for the next guess, uses this guess in the first slot with this number in its possibilities array._

_**I will hopefully upload an illustration for this process to make it a bit more clear.**_

======================================
## HOW TO USE
======================================

_I noticed that there is always a finite number of possible games so I made batch mode to try all those possibilities._
_Which, in my opinion, makes more sense since it tests all possible cases._

In the integrated interface, you can choose one of 4 modes:<br>
<pre>
BATCH : runs ALL the possible variations of games
CUSTOM: asks the user for a certain starting guess and a certain password to guess and runs a simulation
of the algorithm guess by guess. (used for testing a certain case)
DEBUG:  runs a singular game and moves through the algorithm guess by guess.
CHEAT:  tries to guess an unknown password and asks for the evaluation to be entered by the user.
</pre>

_The inputs use the regex filter **^[0-3]{4}$** if you are interested_
