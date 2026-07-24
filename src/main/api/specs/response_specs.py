from requests import Response
from http import HTTPStatus

# респонс приходит не сразу. чтобы можно было ...надо замыкание :(
# в итоге конфирм будет исполняться когдаполучим респонс
class ResponseSpecs:
    @staticmethod
    def request_ok(): # 200
        def confirm(response: Response): # а это как реализация. как только получим респонс - будем делать конфирм
            assert response.status_code == HTTPStatus.OK, response.text
        return confirm

    @staticmethod
    def request_created(): #201
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.CREATED, response.text
        return confirm

    @staticmethod
    def request_bad(): #400
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.BAD_REQUEST, response.text
        return confirm

    @staticmethod
    def request_unauthorized():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.UNAUTHORIZED, response.text
        return confirm

    @staticmethod
    def request_forbidden():  # 403
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.FORBIDDEN, response.text

        return confirm

    @staticmethod
    def request_not_found(): #404
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.NOT_FOUND, response.text
        return confirm

    @staticmethod
    def request_conflict():  # 409
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.CONFLICT, response.text
        return confirm

    @staticmethod
    def request_unprocessable_entity():  # 422
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, response.text
        return confirm