from rest_framework.pagination import CursorPagination


class DeliveryFeedPagination(CursorPagination):
    """Small pages, newest first; cursor keeps pages stable as deliveries arrive."""
    page_size = 25
    ordering = '-delivered_at'
