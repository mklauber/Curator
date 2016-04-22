"""Handles the parsing of a query string, and returning a SQL object representing a query."""
import shlex


from models import File, Metadata

def parse(query):
    if query == "":
        return File.select()
    
    tokens = tokenize(query)
    result = _parse(iter(tokens))
    try:
        iter(result)
    except TypeError:
        result = File.select().join(Metadata).where(result)
    print result
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
        elif token == 'AND':
            output = AND(output, _parse(iterator))
        elif token == 'OR':
            output = OR(output, _parse(iterator))
        elif token == 'NOT':
            output = NOT(_parse(iterator))
        else:
            output = Token(token)
    return output


def AND(left, right):
    return (File.select().join(Metadata).where(left) & File.select().join(Metadata).where(right))

def OR(left, right):
    return (File.select().join(Metadata).where(left) | File.select().join(Metadata).where(right))


def NOT(token):
    return (~(File.id << File.select().join(Metadata).where(token)))


def Token(token):
    if ':' in token:
        field, value = token.split(':')
    else:
        field, value = 'tag', token
    return ((Metadata.field == field) & (Metadata.value == value)) 

