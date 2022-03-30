# Zelda Style RPG in pygame

* 2D Zelda Style RPG developed using pygame and tile graphics.
* Game was developed as part of [Clear Code Youtube Tutorial](https://www.youtube.com/watch?v=QU1pPzEGrqw&list=PLGUFtX0WQvIfc_tREtSfYcQpDju0YMg93&index=6&t=2678s&ab_channel=ClearCode). 

</img>
<img src = "docs/demo.gif", alt = "zelda demo", height = "350">

The code mostly follows the tutorial, however I did put my own flavour on it, such as:
  * Refactored methods to reduce code complexity, and follow clean code principles.
  * Refactored code structure, modulizing for a more organsied development.

Sections I implemmented not in the tutorial:
  * TitleMenuInterfaceBase, base class for title screen inheritance. the TitleScreenInterface, LevelCompleteInterface and GameOverInterface inherit this class.
  * Title Screen Menu:
    * Option to 'Play' or 'Quit' 
  * Leveling: 
    * Can set number of levels in settings.py. Enemy sprites will respawn and become increasing harder but reward more experience points.
    * Level Complete Interface: Option to 'Continue' or 'Quit' 
  * Game Over Menu:
    * Display 'Game Over' or 'You Won' deppending on the outcome
    * Options to 'Try Again' or 'Quit'

All game assets are stored in the "assets" folder and were sourced from [Clear Code Projects](https://github.com/clear-code-projects/Zelda) under a Creative Commons Zero (CC0) license.

# References: 
  * [YouTube Tutorial](https://www.youtube.com/watch?v=QU1pPzEGrqw&list=PLGUFtX0WQvIfc_tREtSfYcQpDju0YMg93&index=6&t=2678s&ab_channel=ClearCode)
  * [Starting Files](https://github.com/clear-code-projects/Zelda)
  * [Art assets and the soundtrack have been done by Pixel-boy and AAA](https://pixel-boy.itch.io/ninja-adventure-asset-pack)