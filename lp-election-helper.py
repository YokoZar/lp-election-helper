#!/usr/bin/python

# TODO: Add a cross-reference check for tech board (must be in both ubuntu-dev and ubuntumembers)
#       Technically we allow people to be ubuntu devs who have individual package upload rights
#       without obtaining full membership, however as of this writing no one falls under that.
# TODO: make this a command-line switch
search_group = "ubuntumembers" # For CC
#search_group = "ubuntu-dev"  # For Tech-board
#search_group = "ubuntu-irc-members" # For IRCC

# In principle we could replace this manual blacklist with a generic launchpad "nonvoter" group and
# then exclude members of that group from the output here, but at the moment it's just one account
blacklist = ["package-import@ubuntu.com"]

from launchpadlib.launchpad import Launchpad

from pyme.errors import GPGMEError
from pyme import core

import sys
import os

# crude hack to avoid old email addresses (like university accounts) that 
# might already be out of use
def find_preferred_domain(emails):
    for preferred_domain in [ "ubuntu.com", "canonical.com", "gmail.com" ]:
        for possible_email in emails:
            if preferred_domain in possible_email:
                return possible_email
    return emails[0]

def extract_mails_from_key(keyid, context):
    try:
        key = context.get_key(str(keyid), False)
    except GPGMEError:
        return "-"
    emails = set()
    for uid in key.uids:
        emails.add(uid.email)
    return find_preferred_domain(list(emails))

def get_email(person, context):
    try:
        email = person.preferred_email_address.email
        return email
    except ValueError:
        emails = [a.email for a in person.confirmed_email_addresses]
        if len(emails):
            email = find_preferred_domain(emails)
            if email:
                return email
        keys = [a for a in person.gpg_keys]
        for key in keys:
            email = extract_mails_from_key(key.keyid, context)
            if email:
                return email
    return "-"

def main():
    launchpad = Launchpad.login_with('mails', 'production', os.path.expanduser("~/.launchpadlib/cache/"))
    members = filter(lambda a: not a.is_team, launchpad.people[search_group].participants)
    context = core.Context()

    guessed_members = []
    print "#### Members with verified public email addresses ####"
    print
    for member in members:
        email = get_email(member, context)
        if email in blacklist:
            continue
        if email is not "-":
            # TODO: control output by command line switches
            print "%s <%s>" % (member.display_name, email)
            #print email
        else:
            # TODO: print a separate list of display names for nonexistant emails
            guessed_email = member.name + "@ubuntu.com" # Note that this isn't perfect and will miss some!
            guessed_members.append(guessed_email)
    print
    print "#### Members with no public email address, assuming email = launchpadid@ubuntu.com ####"
    print
    for guessed_member in guessed_members:
        print guessed_member

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print >> sys.stderr, "Aborted."
        sys.exit(1)

