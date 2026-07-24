from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.user_login_request import UserLoginRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps



class AdminSteps(BaseSteps):
    def create_user(self, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username='admin', password='123456'),
            Endpoint.ADMIN_CREATE_USER,
            ResponseSpecs.request_ok()
        ).post(create_user_request)

        self.created_obj.append(response) # добавляем данные в лист в креейт_обж
        return response

    def delete(self, user_id: int):
        CrudRequester(
            RequestSpecs.auth_headers(username='admin', password='123456'),
            Endpoint.ADMIN_DELETE_USER,
            ResponseSpecs.request_ok()
        ).delete(user_id)

    def create_invalid_user(self, create_user_request: CreateUserRequest):
        CrudRequester(
            RequestSpecs.auth_headers(username='admin', password='123456'),
            Endpoint.ADMIN_CREATE_USER,
            ResponseSpecs.request_bad()
        ).post(create_user_request)

    def user_login(self, user_login_request: UserLoginRequest):
        response = ValidateCrudRequester(
            RequestSpecs.unauth_headers(),
            Endpoint.USER_LOGIN,
            ResponseSpecs.request_ok()
        ).post(user_login_request)
        return response

    def user_login_missing_login(self, user_login_request: UserLoginRequest):
        response = CrudRequester(
            RequestSpecs.unauth_headers(),
            Endpoint.USER_LOGIN,
            ResponseSpecs.request_unauthorized()
        ).post(user_login_request)
        return response