
This was a really interesting challenge!

First, we have a _huge_ file dump from the `.tar`, and it's hard to know where to start.

Pick a file name and try googling for it. The more unique the file sounds, the better your results
might be. I ended up going with `webappsstore.sqlite`, and we immediately find results related to 
`Mozilla`, and by extension, presumably Firefox.

After a bit more OSINT, we find that Firefox stores what it calls "profiles" on your computer.

Looking up the steps to 
[import/recover a profile](https://support.mozilla.org/en-US/kb/back-and-restore-information-firefox-profiles)
makes it so I can run Firefox with all of the challenge data loaded in :). 

After scrolling through the web history (and getting rickrolled), we find a Pastebin they visited
named "Inconspicuous". Clicking it brings us to the pastebin, and Firefox automatically fills out 
the password for us. We get the flag: `ictf{th3_f0x_0f_f1r3_s33s_a11}`
