This is a simple script to get email addresses from a Launchpad group.  First, it searches to see 
if the user has a Launchpad email address publicly visible.  Failing that, it will look for a GPG 
key on the account and use the email address located there.

Our sole purpose is to use these emails for running an election using the Condorcet Internet 
Voting Service (CIVS): http://www.cs.cornell.edu/andru/civs.html

The script requires a group name to search -- make sure this group matches the elligible pool of
voters that you want for the election.  For example:

  lp-election-helper ubuntumembers       # For Ubuntu Community Council
  lp-election-helper ubuntu-dev          # For Ubuntu Technical Board
  lp-election-helper ubuntu-irc-members  # For IRC Council


Note that it is possible for Launchpad users to have multiple email addresses associated with their
account -- in such a case, lp-election-helper will choose a "preferred" email address (such as the
one including @ubuntu.com), and, failing that, will default to the first one that Launchpad returns.

Be aware that, since it is possible for an account to have multiple email addresses, it is also 
possible for lp-election-helper to return a different result when run a second time if the user has
updated their account.  For this reason, it is recommended to limit running lp-election-helper to
only a single time at the start of an election to avoid possible double voting by members who have 
updated or changed their launchpad email address.
