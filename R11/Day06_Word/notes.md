
It's important to have correct tooling :) 

Turns out, if you open this using `Word.exe`, you'll get a document that explains the `Word` file format.
This is a good hint that the challenge is about digging into the raw data in the file.

There are a few ways to do this: 

1. Use the bash command `strings` on the file. The idea behind this command is that it looks inside
binary-ish files for consecutive human readable ASCII characters. 

   
2. Open this up in a (non-rich) text editor, like `vi` or `emacs` or `notepad` or my personal goto,
`notepad++`. Ctrl+F or the equivalent for "ictf", and you will find the flag.
   

3. Unzip the file (I use `7zip`), and find a file called `flag.txt`, containing the flag.