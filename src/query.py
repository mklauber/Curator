"""Handles the parsing of a query string, and returning a SQL object representing a query."""
import shlex

import peewee
from models import File, Metadata

def parse(query):
    if query == "":
        return File.select()
    
    tokens = tokenize(query)
    result = _parse(iter(tokens))
    try:
        iter(result)
    except TypeError:
        result = File.select().join(Metadata, peewee.JOIN_LEFT_OUTER).where(result)
    return result

def tokenize(string):
    string = string.replace('(', ' ( ')
    string = string.replace(')', ' ) ')
    string = string.replace('!', ' NOT ')
    return shlex.split(string)


def _parse(iterator):
    output = None
    for token in iterator:
        if token == '(':
            output = _parse(iterator)
        elif token == ')':
            return output
        elif token.upper() == 'AND':
            output = AND(output, _parse(iterator))
        elif token.upper() == 'OR':
            output = OR(output, _parse(iterator))
        elif token.upper() == 'NOT':
            output = NOT(_parse(iterator))
        elif token.upper() == 'HAS':
            output = HAS(token, iterator.next())
        else:
            output = Token(token)
    return output


def AND(left, right):
    return (File.select().join(Metadata, peewee.JOIN_LEFT_OUTER).where(left) & File.select().join(Metadata, peewee.JOIN_LEFT_OUTER).where(right))

def OR(left, right):
    return (File.select().join(Metadata, peewee.JOIN_LEFT_OUTER).where(left) | File.select().join(Metadata, peewee.JOIN_LEFT_OUTER).where(right))


def NOT(token):
    return (~(File.id << File.select().join(Metadata, peewee.JOIN_LEFT_OUTER).where(token)))


def HAS(_, token):
    return (Metadata.field == token)


def Token(token):
    if ':' in token:
        field, value = token.split(':', 1)
    else:
        field, value = 'tag', token
    return ((Metadata.field == field) & (Metadata.value == value)) 

