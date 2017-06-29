## Important

Note to use this demo we need to write our output to a rib file then render the fib file as python can't execute the RunProgram directly.

```
clang++ -std=c++11  spiral.cpp -o spiral; ./procedural.py ; render spiral.rib
```