#!/bin/bash
cat <<DOC
  Way too difficult for what it is
  It should've been possible to just gdb it into jmping to the path and printing the flag
  Also, this would've been solved by Angr in ~~a heartbeat~~ 5 hours
  A~Z: It must be due to the multiple threads (I had to debug by finding a breakpoint that triggered only on thread #1 and from here find the actual main function)
DOC
./gofish < <(echo -e 'Go Fish!\nDo you have any flags?')
echo ''
