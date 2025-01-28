from channels.middleware import BaseMiddleware
from rest_framework_simplejwt.tokens import AccessToken
from channels.db import database_sync_to_async


class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        token = self.get_token_from_scope(scope)
        
        if token != None:
            user_id = self.get_user_from_token(token) 
            if user_id:
                scope['user_id'] = user_id
            else:
                scope['error'] = 'Invalid token'

        if token == None:
            scope['error'] = 'Provide an auth token'    
    
        return await super().__call__(scope, receive, send)

    def get_token_from_scope(self, scope):
        try:
            headers = {
                k.decode('utf-8').lower(): v.decode('utf-8') 
                for k, v in dict(scope.get("headers", [])).items()
            }

            auth_header = headers.get('authorization', '')

            if not auth_header:
                return None

            parts = auth_header.split()
            if len(parts) != 2 or parts[0].lower() != 'bearer':
                return None

            token = parts[1]

            return token

        except Exception as e:
            return None
            
    def get_user_from_token(self, token):
            try:
                access_token = AccessToken(token)
                return access_token['user_id']
            except:
                return None