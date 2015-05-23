#Jawfish

Jawfish is a tool designed to break into web applications.

Based on [Forced Evolution](https://github.com/soen-vanned/forced-evolution), it is self-modifying - finding exploits and updating its internal database accordingly.

[Check out the Github Page for this.](https://gingeleski.github.io/jawfish)

##Parts

**Target IP** - The server IP you are attacking. It is recommended to not use a hostname, as DNS lookups significantly slow the current version of Jawfish down. Example: 192.168.1.1

**Address** - The path URL to the vulnerable page. Example: /herp/derp/vuln.php

**Vulnerability** - This is the POST or GET variable that will be exploited.

**Method** - This can be either POST or GET, and defines the behavior of Jawfish as it communicates over HTTP POSTs and GETs.

**Goal Text** - The most important option to get correct, as it will define when an exploit string is deemed as working. Case is ignored. Examples: If you are attempting to bypass a login form, perhaps “Login Successful.” For command injection, an indicative server response like “Directory of.” For SQL injection, maybe “row in set.” Jawfish currently contains no capabilities for dumping databases or post-exploitation. You can take the exploit produced by Jawfish and feed it into a tool like sqlmap.

##End notes

This is the alpha of Jawfish. Backend hasn't been hooked to frontend.

Based on Soed Vanned’s [Forced Evolution](https://github.com/soen-vanned/forced-evolution).
