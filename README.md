# Watchful McGrupp

Watchful McGrupp is a simple Python script that ensures the files and folders 
in a directory have properly written descriptions. When there isn't a 
description, you receive an email from this service noting that you need to 
write one.

## Format
Assume you have a directory structured as follows:
```
alex@grange:~/federalistpapers$ ls
energetic_government        outline.txt      union_utility
insufficient_confederation  true_republican
```
and a descriptions file with the contents:
```
# outline.txt
Working outline of The Federalist Papers. Keep James and John in the loop on 
the project!

# union_utility
Here contains the drafts of issues 2-14, where we talk about foreign influence,
inter-state dissension, and domestic welfare.

# insufficient_confederation
Why is the Articles of Confederation insufficient to achieve these goals listed
in the union_utility section?
```

Watchful McGrupp will take the names of each of the items in the directory, and
look for a line in the descriptions file that begins with a hash and contains
that item's name. When it doesn't find, you receive an email that says:

> Watchful McGrupp notes that you're missing some explanations in your 
> /home/alex/federalistpapers/ folder.
> In particular, you are missing explanations for 'energetic_government' and 
> 'true_republican'.

## Configure

Most changes you'd want to make are in the configuration file. It's in a format
similar to Windows INI and it's intended to be read by Python's `ConfigParser` 
class. If the config file is insufficient, make a change and a pull request!

### Rename file

When you download the repo, it will contain a file called `config_sample`. Use
this to make your `config` file

### Tracked directory

The `tracked_directory` setting is the pathname of the directory that you want
to ensure has descriptions. Similarly, `tracking_file` is the file that 
contains those descriptions.

### Email login

Email login data is stored in the username and password entries. I recommend
making an application-specific password so you don't have your regular password
in plaintext.

### Email server
These settings [`smtp_server` and `smtp_port`] are used to connect to the SMTP
server. I use Gmail, and so the sample connects to Google.

### Wait time
Both `waiting_days` and `waiting_seconds` are passed to Python's `timedelta`
class. This determines the amount of time between emails that are sent.

## Cron

In order to run this script regularly, you need to specify it as a cron job on
your server or computer. This determines how often Watchful McGrupp checks the
directory, not how often you are emailed. I have it set to check every hour in
case I don't have my computer open at a particular time each day.

To add this to your cron tab, type
```
crontab -e
```
Use your favorite command line text editor to add this line:
```
0 * * * * python /path/to/watchful_mcgrupp/mcgrupp.py
```

Watchful McGrupp will be watching out for you!