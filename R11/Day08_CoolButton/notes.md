
There's a button that does a redirect before sending you to the another webpage. 

How do you realize this while using the website on a browser? 

1. Hopefully, you're using Firefox and not Chrome.
   
2. Then, open up the developer tools with F12, and find the "Network" tab.

3. Press the gear icon to the right, and check `Persist Logs`.

4. Click the button on the webpage to make the request.

5. Check the rows on the "Network" tab on devtools:
   1. Click a row.
   2. On the pane that opens up to the right, switch from the "Headers" tab to the "Response" tab
   3. Toggle `raw` to on.
   4. As you click throw all the rows, you'll find the text `<!--ictf{f1ag_1n_th3_c0mm3nts!}-->`

6. Profit.


If you're not familiar with it already, you should really spend some time with the devtools.
It helps you easily check cookies, monitor and replay requests, find hints in the source,
edit the javascript that runs locally, and much more; all helpful while testing 
a web challenge for the first time on browser.
