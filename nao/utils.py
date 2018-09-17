

import re


def recursive_update(base, other):
    """
    Recursively upadtes base with other. Both should be
    dictionary-like mapping types. 

    Returns None as modifies base in place

    This is a module level function and can be used for
    any dictionary like objects including dict, odict
    and naodict

    TODO: check __instancecheck__ for naodict metaclass
    """
    for key, value in other.items():
        if key in base and dictlike(base[key], value):
            recursive_update(base[key], value)
        else:
            base[key] = value



# TODO move to _compat.py with od_backport
# TODO remove od_backport

def dictlike(*candidates):
    """checking"""
    for c in candidates:
        if not isinstance(c, (dict,)): return False
    return True


def listlike(*candidates):
    """checking"""
    for c in candidates:
        if not isinstance(c, (list,)): return False
    return True


####################
# padding strings
def padded(string, spaces=4):

    return '\n'.join([' '*spaces+l for l in string.split('\n')])

        

u1reg = re.compile('((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))')
u2reg1 = re.compile('(.)([A-Z][a-z]+)')
u2reg2 = re.compile('(a-z0-9])([A-Z])')

def underscore(text, method='single_reg'):
    """
    Largely based on Stack Overflow.
    Two methods are only implemented out of curiosity.

    Converts `CamelCase` or `camelCase` to under_score style.
    Able to handle `camelAndHTTPResponse` as `camel_and_http_response`.
    Avoids multiple underscores, so `under_Score` remains `under_score`
    does not become `under__score`.
    """

    if method == 'single_reg':
        return u1reg.sub(r'_\1', text).lower().replace('__', '_')

    if method == 'double_reg':
        temp = u2reg1.sub(r'\1_\2', text)
        return u2reg2.sub(r'\1_\2', temp).lower().replace('__', '_')

    raise ValueError("Method not recognized: {}".format(method))


def flatten(d, parent_key='', sep='.'):
    """
    FROM http://stackoverflow.com/questions/6027558/flatten-nested-python-dictionaries-compressing-keys
    """
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def unflatten(d):
    """
    TODO implement
    """




# TIMING CONTEXTMANAGER AND DECORATOR
def benchmark(arg):

    # normal use returns a context manager
    if not callable(arg):
        return Benchmark(str(arg))

    # decorator use: wrapped into a benchmark context
    func = arg
    @functools.wraps(func)
    def wrapper(*args, **kwds):
        with Benchmark('FUNC ' + func.__name__):
            return func(*args, **kwds)

    return wrapper

class Benchmark(object):
    """
    Based on something similar found long time ago on the internet
    """
    def __init__(self, name):
        self._name = name
        self._time = None

    def __enter__(self):
        self._begin = time.time()
        log.info("Benchmark <{}> started ...".format(self._name))

    def __exit__(self, exc_type, exc_value, traceback):
        self._time = time.time()-self._begin
        log.info("Benchmark <{}> finished in: {}".format(self._name, self.time))
        return False

    @property
    def time(self, raw=False):
        if time is None:
            raise ValueError('Not run yet')

        return self._time if raw else self.format_time(self._time)
    

    @staticmethod
    def format_time(seconds):
        """
        TODO use `babel.dates.format_timedelta` with
        `datetime.timedelta(seconds=...)`

        """
        t = []
        
        if seconds > 60*60:
            hours, seconds = divmod(seconds, 60*60)
            t.append("{:.0f}h".format(hours))
        
        if seconds > 60:
            mins, seconds = divmod(seconds, 60)
            t.append("{:.0f}m".format(mins))

        t.append("{:.3f}s".format(seconds))

        return ' '.join(t)


def obj2xml(obj, level=1):
    """
    recursively transform an object structure to an
    XML structure to be able to view

    to_yaml is more sane!!!
    but need serialization rule for 
    non-standard python objects!
    """
    if isinstance(obj, list):

        return '\n'.join([obj2xml(i, level+1) for i in obj])

    ats = []
    for a in obj.__dict__:
        if not a.startswith('_'):
            val = getattr(obj, a)
            ats.append('{}<attr name="{}">{}{}</attr>'.format(
                "\t"*level,
                a, 
                obj2xml(val, level+1) if isinstance(val, list) else val,
                '\n'+"\t"*level if isinstance(val, list) else '',
            ))

    return '\n{}<obj type="{}">\n{}\n{}</obj>'.format(
        "\t"*(level-1),
        type(obj),
        '\n'.join(ats),
        "\t"*(level-1),
    )





