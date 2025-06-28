"""
ClipTools clipboard manager and text processing tools
with a lines based GUI interface

Processing functions related to Jira links copied to clipboard.
After copying to your user folder, please customize for your case
with the BASE_LINK and TICKET_TEXT variables below.

You can add new functions as you like to this file, or create similar files
to your user folder.
Function naming: <action_group_name>_<action_name>(text)

Note:
 - File is using doctest to show the usage of all functions.
 - Unfortunately doctests are using fix company and project names,
   not the configured variable. If you want to run tests after customizing
   the file please change those as well.

"""

import re

from cliptools.modules.data_struct import register_function


# You can customize the Jira links that your company is using
# in these variables. In the example below my-company is the
# company name and XX, YY and ZZ are possible projects.
# Ticket length is 4-5 digit long.
BASE_LINK = "https://my-company.atlassian.net/browse/"
TICKET_TEXT = "(XX|YY|ZZ)-(\\d{4,5})"


# Regex patterns, no need to change these
TICKET_PATTERN = re.compile(TICKET_TEXT)
FULL_LINK_PATTERN = re.compile(BASE_LINK + TICKET_TEXT)


class JiraLink:
    """Class to define the possible Jira link transformations."""

    def __init__(self, text: str):
        text = text.strip()
        if TICKET_PATTERN.fullmatch(text):
            self.is_ticket = True
            self.ticket_number = text
            self.ticket_link = BASE_LINK + text
        elif FULL_LINK_PATTERN.fullmatch(text):
            self.is_ticket = True
            self.ticket_number = text[len(BASE_LINK) :]
            self.ticket_link = text
        else:
            self.is_ticket = False
            self.ticket_number = "NA"
            self.ticket_link = "NA"


@register_function
def jira_link(text):
    """
    Return Jira link from ticket number

    >>> jira_link('XX-12345')
    'https://my-company.atlassian.net/browse/XX-12345'
    """
    jl = JiraLink(text)
    if jl.is_ticket:
        return jl.ticket_link
    return text


@register_function
def jira_ticket(text):
    """
    Return ticket number from Jira link

    >>> jira_ticket('https://my-company.atlassian.net/browse/XX-12345')
    'XX-12345'
    """
    jl = JiraLink(text)
    if jl.is_ticket:
        return jl.ticket_number
    return text


@register_function
def jira_testpad(text):
    """
    Return TestPad link format from a ticket number or link

    TestPad (https://testpad.com/) is using a simple format to link tickets,
    that is 'ticket:XX-12345'.

    >>> jira_testpad('https://my-company.atlassian.net/browse/XX-12345')
    'ticket:XX-12345'
    """
    jl = JiraLink(text)
    if jl.is_ticket:
        return "ticket:" + jl.ticket_number
    return text


@register_function
def jira_md(text):
    """
    Return markdown link format from a ticket number or link

    >>> jira_md('https://my-company.atlassian.net/browse/XX-12345')
    '[XX-12345](https://my-company.atlassian.net/browse/XX-12345)'
    """
    jl = JiraLink(text)
    if jl.is_ticket:
        return f"[{jl.ticket_number}]({jl.ticket_link})"
    return text
