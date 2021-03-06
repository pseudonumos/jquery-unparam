#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
from urllib import unquote_plus

def parse_key_pair(keyval):
    keyval_splitted = keyval.split('=', 1)
    if len(keyval_splitted) == 1:
        key, val = keyval_splitted[0], ''
    else:
        key, val = keyval_splitted
    if key == '':
        return {}
    
    groups = re.findall(r"\[.*?\]", key)
    groups_joined =  ''.join(groups)
    if key[-len(groups_joined):] == groups_joined:
        key = key[:-len(groups_joined)]
        for group in reversed(groups):
            # need to parse [] or [0] elements
            if group == '[]' or ''.join(i for i in group if not i.isdigit()) == '[]':
                val = [val]
            else:
                val = {group[1:-1]: val}
    return {key: val}

def merge_two_structs(s1, s2):
    if isinstance(s1, list) and \
        isinstance(s2, list):
        retval = []
        structs = []
        for v1 in s1:
            if isinstance(v1, list) or isinstance(v1, dict):
                structs.append(v1)
            else:
                retval.append(v1)
        for v2 in s2:
            if isinstance(v1, list) or isinstance(v1, dict):
                structs.append(v2)
            else:
                retval.append(v2)
        if structs:
            cstruct = structs.pop()
            for struct in structs[:]:
                cstruct = merge_two_structs(cstruct, struct)
            retval.append(cstruct)
        return retval

    if isinstance(s1, dict) and \
       isinstance(s2, dict):
        
        retval = s1.copy()
        for key, val in s2.iteritems():
            if retval.get(key) is None:
                retval[key] = val
            else:
                retval[key] = merge_two_structs(retval[key], val)
        return retval
    return s2

def merge_structs(structs):
    if len(structs) == 0:
        return None
    if len(structs) == 1:
        return structs[0]
    first, rest = structs[0], structs[1:]
    return merge_two_structs(first, merge_structs(rest))

def jquery_unparam_unquoted(jquery_params):
    pair_strings = jquery_params.split('&')
    key_pairs = [parse_key_pair(x) for x in pair_strings]
    return merge_structs(key_pairs)

def jquery_unparam(jquery_params):
    return jquery_unparam_unquoted(unquote_plus(jquery_params))

if __name__ == '__main__':
    pass
