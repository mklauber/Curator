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
        elif token.upper() == 'UNTAGGED':
            output = UNTAGGED()
        else:
            output = Token(token)
    print output
    return output


def AND(left, right):
    if type(left) == peewee.Expression:
        left = File.select().join(Metadata, peewee.JOIN_LEFT_OUTER).where(left)
    if type(right) == peewee.Expression:
        right = File.select().join(Metadata, peewee.JOIN_LEFT_OUTER).where(right)
    return (left & right)


def OR(left, right):
    if type(left) == peewee.Expression:
        left = File.select().join(Metadata, peewee.JOIN_LEFT_OUTER).where(left)
    if type(right) == peewee.Expression:
        right = File.select().join(Metadata, peewee.JOIN_LEFT_OUTER).where(right)
    return (left | right)


def NOT(token):
    if token == peewee.Expression:
        token = File.select().join(Metadata, peewee.JOIN_LEFT_OUTER).where(token)
    return File.select().where(~(File.id << token))


def HAS(_, token):
    return (Metadata.field == token)


def UNTAGGED():
    return File.select().where(File.id.not_in(Metadata.select(Metadata.file).where(Metadata.field != 'import-time')))


def Token(token):
    if ':' in token:
        field, value = token.split(':', 1)
    else:
        field, value = 'tag', token
    return ((Metadata.field == field) & (Metadata.value == value)) 

