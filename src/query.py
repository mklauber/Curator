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
    return output


def AND(left, right):
    return (left & right)


def OR(left, right):
    return (left | right)


def NOT(token):
    return set(File.select().where(File.id.not_in([f.id for f in token])))


def HAS(_, token):
    return set(File.select().join(Metadata, peewee.JOIN_LEFT_OUTER).where(Metadata.field == token))


def UNTAGGED():
    tagged_files = Metadata.select(Metadata.file).where(Metadata.field != 'import-time')
    return set(File.select().where(File.id.not_in(tagged_files)))


def Token(token):
    if ':' in token:
        field, value = token.split(':', 1)
    else:
        field, value = 'tag', token
    files = File.select().join(Metadata, peewee.JOIN_LEFT_OUTER)
    return set(files.where((Metadata.field == field) & (Metadata.value == value)))
