"""Configuration parser."""

from configlib import loadcfg


__all__ = ['CONFIG']


CONFIG = loadcfg('hinews.conf')
