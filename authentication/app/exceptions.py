from fastapi.exceptions import HTTPException
from starlette import status


class InvalidTokenException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = f"Invalid token. "
        super().__init__(status_code=self.status_code, detail=self.detail)


class EmailAlreadyExists(HTTPException):
    def __init__(self):
        detail = "Email is already in use. Please try another email."
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class UsernameAlreadyExists(HTTPException):
    def __init__(self):
        detail = "Username is already in use. Please try another username."
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class UserNotFoundException(HTTPException):
    def __init__(self, user_id):
        self.user_id = user_id
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = f"User with ID {user_id} not found"
        super().__init__(status_code=self.status_code, detail=self.detail)


class ProductNotFoundException(HTTPException):
    def __init__(self, product_id):
        self.product_id = product_id
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = f"Product with ID {product_id} not found"
        super().__init__(status_code=self.status_code, detail=self.detail)


class OrderNotFoundException(HTTPException):
    def __init__(self, order_id):
        self.order_id = order_id
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = f"Order with ID {order_id} not found"
        super().__init__(status_code=self.status_code, detail=self.detail)


class MinimumOneProductRequiredException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = f"Order must contain at least one product."
        super().__init__(status_code=self.status_code, detail=self.detail)


class InvalidPriceValueException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = f"Price of the product must be greater than zero."
        super().__init__(status_code=self.status_code, detail=self.detail)


class PermissionDeniedException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = f"User does not have permission to perform this action. "
        super().__init__(status_code=self.status_code, detail=self.detail)


class UnauthorizedOrderAccessException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_403_FORBIDDEN
        self.detail = "You can only alter your own orders. "
        super().__init__(status_code=self.status_code, detail=self.detail)


class UnauthorizedProductAccessException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_403_FORBIDDEN
        self.detail = "You can only alter your own products. "
        super().__init__(status_code=self.status_code, detail=self.detail)
