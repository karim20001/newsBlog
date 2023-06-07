from rest_framework import pagination

class AllArticlesPaginator(pagination.PageNumberPagination):
    page_size = 1
    page_size_query_param = "page_size"
    # page_query_param = "p"