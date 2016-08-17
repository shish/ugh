ugh
===

A tinder client for people who think tinder is awful. This one will automatically reject anybody with an empty description, and show you the other people's descriptions, no photos, no names. If you match, you still need to use the regular mobile app to chat - this is *just* a tool for rejecting huge numbers of people in a small amount of time.

Requires Python 2.7, that should be all.

This is not user-friendly, *especially* not the setup process.


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

