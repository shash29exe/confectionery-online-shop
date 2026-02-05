import logging
import time

logger = logging.getLogger(__name__)


class RequestLogMiddleware:
    """
        Логирование каждого запроса, времени, пользователя
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        duration = round(time.time() - start_time, 3)
        user = request.user if request.user.is_authenticated else 'Аноним'

        logger.info(
            f'{request.method} {request.path} | статус: {response.status_code} | '
            f'пользователь: {user} | {duration}'
        )

        return response
