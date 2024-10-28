# Chekers & MinMax algorith with alpha-beta pruning 

In this project I was practicing implementation of the min max algorithm with alpha-beta pruning within the checkers game. 

## Game outline 

The board is 8x8 where b and r are basic chips and the B and R are "Kings" 
Game represents all the orignial features of checkers with all **multijumping** logic and creation of **Kings** with one following simplification: 
- If a player can take opponent's chip it has to do

### Output 

The output file will print out the board after every move the AI makes

## Running the code

Attached a few test cases that could be run to see how the program works. 
To run the program run: 

```
python3 checkers_starter.py --inputfile checkers1.txt --outputfile output.txt
```


## Further improvements 
- The states could be stored in a queue where the states with better heuristic would be prefered to maximise pruning
- State caching
- Remove simplification rule stated above -> reduces performance 
