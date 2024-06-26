from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "size"
    max_page_size = 100
    allow_empty_first_page = True
