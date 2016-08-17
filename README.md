ugh
===


Finding your User ID:
---------------------
go to your facebook profile ( https://www.facebook.com/me ) - the part after the `.com/` is your facebook user ID, stick that in `user_id.txt`


Finding your Auth Token:
------------------------
(This will need refreshing every hour or so)

Open firefox

Open developer tools (Cmd-Alt-I on OSX, Ctrl-Shift-I on others I think?)

Go to http://tinyurl.com/gon449r

Should say Tinder is already authenticated. Click ok, look in network tab for 'confirm', look at the 'response' tab for a big blob of code.

In that blob, find `access_token=....`, stick it in `user_token.txt`

Then run ugh.py

