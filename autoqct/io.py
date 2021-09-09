# -*- coding: utf-8 -*-

"""IO functions for molecules."""

__all__ = [ 'read_xdr' ]

from .xdrfile import xdrfile

def read_xdr(filename):
    xdr = xdrfile(filename)
    return [frame.x.copy() for frame in xdr]
