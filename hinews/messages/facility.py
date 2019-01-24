"""Messages."""

from his import HIS_MESSAGE_FACILITY


__all__ = ['NEWS_MESSAGE']


NEWS_MESSAGE_DOMAIN = HIS_MESSAGE_FACILITY.domain('hinews')
NEWS_MESSAGE = NEWS_MESSAGE_DOMAIN.message
