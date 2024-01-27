from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import LimitOffsetPagination, CursorPagination


class WatchListPagination(PageNumberPagination):
    page_size = 5
    page_query_param = 'watchlist'
    page_size_query_param = '10'
    max_page_size = '20'
    last_page_strings = 'end'
    
    
class LimitOffSetPaganationAV(LimitOffsetPagination):
    default_limit = 2
    limit_query_param ='watchlist'
    max_limit = 1
    offet_query_param = 'start'
    
class WatchListCPagination(CursorPagination):
    page_size = 5
    ordering = 'created'
    cursor_query_param = 'record'