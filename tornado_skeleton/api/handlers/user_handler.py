# coding: utf-8

from datetime import datetime

import ujson as json

from tornado_skeleton.models.user import User
from tornado_skeleton.helpers.error_code import ErrorCode
from tornado_skeleton.api.handlers.base_handler import BaseHandler


class UserHandler(BaseHandler):
    async def get(self, user_id):
        """
        Retrieve the user from a user ID.
        Return status:
            200 OK with the user in the body if successful
            404 Not Found if the user does not exist
        :param user_id: ID of the user to retrieve.
        :type user_id: str
        """
        user = User().get_users().get(user_id)
        if user:
            self.send_response({'user': user})
        else:
            return self.produce_error(ErrorCode.USER_NOT_FOUND, user=user_id)

    # async def post(self, user_id):
    #     """
    #     Deactivate the user by removing its tokens.
    #     The user is specified by a user id.
    #     Missing mandatory user attributes produce an error.
    #     Return a 403 Forbidden if the request does not have the permission.
    #     Return a 404 Not Found if the user or a body resource is not found.
    #     Return a 204 No Content if the user is deactivated.
    #
    #     :param user_id: The id of the user to deactivate.
    #     :type user_id: int
    #     """
    #     operation = self.get_argument('operation', None)
    #     if not operation:
    #         return self.produce_error(ErrorCode.MISSING_PARAMETER, parameter='operation')
    #
    #     if operation == 'deactivate':
    #         with self.make_session() as session:
    #             user = await as_future(session.query(User).filter(User.id == user_id).first)
    #             if not user:
    #                 return self.produce_error(ErrorCode.USER_NOT_FOUND, user=user_id)
    #             elif user.deactivation_date is not None and user.deactivation_date < datetime.now():
    #                 return self.produce_error(ErrorCode.USER_ALREADY_DEACTIVATED, user=user)
    #
    #             for token in list(user.tokens):
    #                 user.tokens.remove(token)
    #
    #             user.deactivation_date = datetime.now()
    #     else:
    #         return self.produce_error(ErrorCode.INVALID_USER_OPERATION, operation=operation)
    #
    #     return self.send_response(None, status=204)
    #
    # async def put(self, user_id):
    #     """
    #     Replace the user with the given body parameters.
    #     The user is specified by a user id.
    #     Missing mandatory user attributes produce an error.
    #     Missing optional user attributes are set to their default values.
    #     Return a 403 Forbidden if the request does not have the permission.
    #     Return a 404 Not Found if the user or a body resource is not found.
    #     Return a 422 Unprocessable Entity if a body parameter is missing or not processable.
    #     Return a 200 OK with the user in the body if the user is replaced.
    #
    #     :param user_id: The id of the user to delete.
    #     :type user_id: int
    #     """
    #     body = self.request.body
    #     email = body.get('email', None)
    #     password = body.get('password', None)
    #     name = body.get('name', None)
    #     metadata = body.get('metadata', None)
    #     roles = body.get('roles', [])
    #     permissions = body.get('permissions', [])
    #
    #     if not email:
    #         return self.produce_error(ErrorCode.MISSING_PARAMETER, parameter='email')
    #     if not password:
    #         return self.produce_error(ErrorCode.MISSING_PARAMETER, parameter='password')
    #
    #     if not validate_email(email):
    #         return self.produce_error(ErrorCode.USER_EMAIL_BAD_FORMAT, email=email)
    #
    #     if len(email) > User.EMAIL_MAX_LENGTH:
    #         return self.produce_error(ErrorCode.USER_EMAIL_TOO_LONG, max_length=User.EMAIL_MAX_LENGTH)
    #
    #     if name and len(name) > User.NAME_MAX_LENGTH:
    #         return self.produce_error(ErrorCode.USER_NAME_TOO_LONG, max_length=User.NAME_MAX_LENGTH)
    #
    #     if metadata and not isinstance(metadata, dict):
    #         return self.produce_error(ErrorCode.WRONG_PARAMETER_TYPE, parameter='metadata', type='dict')
    #
    #     if not isinstance(roles, list) or not all(isinstance(role, int) for role in roles):
    #         return self.produce_error(ErrorCode.WRONG_PARAMETER_TYPE, parameter='roles', type='list(int)')
    #
    #     if not isinstance(permissions, list) or not all(isinstance(permission, int) for permission in permissions):
    #         return self.produce_error(ErrorCode.WRONG_PARAMETER_TYPE, parameter='permissions', type='list(int)')
    #
    #     password = password.encode()
    #
    #     with self.make_session() as session:
    #         user = await as_future(session.query(User).filter(User.id == user_id).first)
    #         if not user:
    #             return self.produce_error(ErrorCode.USER_NOT_FOUND, user=user_id)
    #
    #         if roles:
    #             roles_id_list = set(roles)
    #             roles = await as_future(session.query(Role).filter(Role.id.in_(roles_id_list)).all)
    #             if not roles or len(roles) != len(roles_id_list):
    #                 return self.produce_error(ErrorCode.ROLES_NOT_FOUND)
    #
    #         if permissions:
    #             permissions_id_list = set(permissions)
    #             permissions = await as_future(session.query(Permission).filter(Permission.id.in_(permissions_id_list)).all)
    #             if not permissions or len(permissions) != len(permissions_id_list):
    #                 return self.produce_error(ErrorCode.PERMISSIONS_NOT_FOUND)
    #
    #         user.email = email
    #         user.password = bcrypt.hashpw(password, bcrypt.gensalt())
    #         user.name = name
    #         user.meta_data = json.dumps(metadata) if metadata else None
    #         user.roles = roles
    #         user.permissions = permissions
    #
    #         session.commit()
    #         session.refresh(user)
    #
    #         self.send_response({
    #             'user': user.dict()
    #         })
    #
    # async def delete(self, user_id):
    #     """
    #     Delete the user specified by a user id.
    #     Return a 403 Forbidden if the request does not have the permission.
    #     Return a 404 Not Found if the user does not exist.
    #     Return a 204 No Content if the user is deleted.
    #
    #     :param user_id: The id of the user to delete.
    #     :type user_id: int
    #     """
    #     with self.make_session() as session:
    #         whoami = await as_future(session.query(User).filter(User.id == self.current_token['user_id']).first)
    #         if not whoami:
    #             return self.produce_error(ErrorCode.USER_NOT_FOUND, user='corresponding to the given token')
    #
    #         user_id = int(user_id)
    #         if whoami.id == user_id:
    #             return self.produce_error(ErrorCode.USER_CANNOT_DELETE_SELF)
    #
    #         user = await as_future(session.query(User).filter(User.id == user_id).first)
    #         if not user:
    #             return self.produce_error(ErrorCode.USER_NOT_FOUND, user=user_id)
    #         session.delete(user)
    #
    #     self.send_response(None, status=204)
