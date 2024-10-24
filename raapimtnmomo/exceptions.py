class MTNMoMoException(Exception):
    pass

class BadRequestException(MTNMoMoException):
    pass

class UnauthorizedException(MTNMoMoException):
    pass

class ConflictException(MTNMoMoException):
    pass

class InternalServerErrorException(MTNMoMoException):
    pass
