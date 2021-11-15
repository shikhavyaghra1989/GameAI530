# GAME AI : Chain Reaction

## Group Members:
  1. [Rahul Dev E](https://github.com/rahuldeve)<br>
  2. [Shikha Vyaghra](https://github.com/shikhavyaghra1989)<br>
  3. [Jacob Celestine](https://github.com/jacobceles)<br>

## Goals:
<ol>
  <li>The goal of this project is to study the behaviour of an intelligent agent when the principles of collaboration and competition are added to a zero-sum board game.</li>
  <li>We try to apply a combination of cooperative and non-cooperative game theory by enforcing additional rules and restrictions.</li>
  <li>Multiple approaches such as Expectiminimax algorithm, Monte Carlo Tree Search algorithms, and Reinforcement Learning will be explored.</li>
</ol>

## Normal Rules:
<ol>
  <li>Players take turns to place orbs of their corresponding colours. A player can only place an orb in an empty cell or a cell which already contains coloured orbs of his own. When two or more orbs are placed in the same cell, they stack up.</li>
  <li>The critical mass of a cell is equal to the number of adjacent cells, i.e., 4 for usual cells, 3 for edge cells and 2 for corner cells.</li>
  <li>When a cell is loaded with orbs equal to its critical mass, the stack explodes. As a result of the explosion, all the orbs from the initial cell fly to adjacent cells. The explosions might result in overloading of an adjacent cell and the chain reaction of explosion continues until every cell is stable.</li>
  <li>When a red cell explodes and there are green cells around, the green cells are converted to red, and the other rules of explosions still follow. The same rule is applicable for other colours.</li>
</ol>

## Demo:
![Gameplay With Only Normal Rules](documents/demo_with_only_normal_rules.gif)

## Additional Rules & Restrictions:
<ol>
  <li>The game will be limited to a maximum of 4-players.</li>
  <li>The game board will be restricted to at most an 8x8 grid.</li>
  <li>During the start of the game, there exists special orbs, each of which can be controlled by any two randomly chosen players</li>
  <li>The special orbs, on interaction by a player, will randomly decay into the orbs of the players who can control it. This introduces a probabilistic element into the game, leading to unpredictable results</li>
  <li>Using the special orbs, two players can team up to dominate other players. On the other hand, each player has to take into account the possibility of their actions unduly being taken advantage of their partner due to random decays</li>
</ol>

## Status
- [x] Basic Game Framework
- [ ] Front-end
- [ ] Flask App
- [x] Expectiminimax
- [ ] Monte Carlo Tree Search
- [ ] Reinforcement Learning
- [ ] Gameplay Evaluation
- [ ] Final Report
