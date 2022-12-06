from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict

class MyPageNumberPagination(PageNumberPagination):
    page_size = 2

    def get_paginated_response(self, data):
        return Response(OrderedDict([
             ('TotalCount', self.page.paginator.count),
             ('countItemsOnPage', self.page_size),
             ('CurrentPage', self.page.number),
             ('NextPage', self.get_next_link()),
             ('PreviousPage', self.get_previous_link()),
             ('Results', data)
         ]))