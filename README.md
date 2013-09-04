Forced Evolution

================

Version 2.0



INSTALL:
 The only file needed to run is fe.py


USAGE:
 WINDOWS:
  python fe.py <options>
 LINUX:
  ./fe.py <options>
 OSX
  ./fe.py <options>


TLDR;
example:
python fe.py TARGET='192.168.1.1' ADDR='vuln1/index.php' VULN_VAR='input' METHOD=get GOAL_TEXT='KEY_DATA'

NOTES:
 * Aside from fe.py, no other files are needed.  They are provided for development
   and clarity reasons
 * Forced Evolution is a self-modifying tool.  It will find successful exploits
   and update it's internal database accordingly
 * The OTHER_VARIABLES option is not required.  Everthing other option is
   required, though.
 * Bugs, problems, or feature reuqests please email me at soen.vanned [@] gmail.com


OPTIONS:
 TARGET
  The target option is the server IP that you are attacking.
  It is recommended to not use a hostname, as the dns lookups
  significantly slow forced evolution down.
 ADDR
  This is the path URL to the vulnerable page.
  example:. /herp/derp/vuln.php
 VULN_VAR
  This is the POST or GET variable that will be exploited
 METHOD
  This can either be POST or GET, this defines the behavior of
  forced evolution as it communicates over HTTP POSTs and GETs
 OTHER_VARS
  This is for inclusion of other variables needed to reach the
  potentially exploitable code, such as session variables.  The
  format for this is designed such that they can be copy/pasted
  out of a URL or post request, example: VAR1=DATA1&VAR2=DATA2
 GOAL_TEXT
  This is **The** most important option to get correct, as it
  will define when an exploit string is deemed as WORKING.
  General principles surrounding this:
   1.  Forced Evolution ignores case in GOAL_TEXT
   2.  If you are attempting to bypass a login form, use text
       that would indicate a successful login.
       example: "Login Successful".
   3.  If you are attempting to use command injection,
       figure out some sort of indicative response from the
       server that would indicate that you have command
       injection.  example: "Directory of" (for windows CMDi)
   4.  For SQL injection, determine what you would like
       to find in the database to determine if you have an
       injectable scenario.  example "row in set"
   5.  For SQL injection, forced evolution contains no
       capabilities (innately) for dumping databases or
       post exploitation, it is recommended to take the exploit
       produced by forced evolution and feed it into a
       post exploitation tool like sqlmap (a fantastic post-
       exploitation tool).

This tool is free.

If you want to embed this in a product that will be sold,
 please don't pay me, rather consider donating to the
 Electronic Frontier Foundation.
        - - - > https://www.eff.org/ < - - -

-soen

Contributors:
	Josh Hyde for contributing a safer database for use against less resilient targets
