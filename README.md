# AlphaChess_Zero attempt

This was supposed to be an approximation of the famous AlphaZero algorithm applied to Chess but in the end was really just an attempt due to the high computational ressources needed to get this to run.

This repo now just contains:
- conversion of the board to an appropriate input representation (18 x 8 x 8) --> One plane for each piece type for each player + some constant planes indicating the number of moves played so far and who is playing next.
- neural net architecture --> Approximation of the architecuture used in the paper. I only used 5 residual layers but you could easily scale this up. Also I omitted the policy head as I did not plan on using it.
- approximation of the self play algorithm which generates the samples for the neural net training but as I already stated without using a policy head.

TODO:
1. neural net training from generated samples
2. evaluation by pitting neural nets against each other
3. frontend + possibility to play against trained nets

In the future I want to try the following in order to make this runnable with limited hardware ressources:
1. Implement the algorithm for a simpler game, which would mean fewer average number of moves per game + fewer legal moves per game position. (In chess this corresponds to approximately 40 and 25, respectively.)
2. Use a computationally less expensive algorithm for chess. The bulk of the computation comes from the monte carlo tree search during self play. So this should be left out. One idea would be to just pretrain a value neural net from expert games and then use this value net to derive a policy from a given state completely without MCTS.

In the unlikely case that anyone wants to build off of this skeleton I included an requirements.txt file so you can easily recreate the virtual environment I used.
