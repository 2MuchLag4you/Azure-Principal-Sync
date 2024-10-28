"""This module contains custom exceptions for Azure Principal Synchronization."""

class InvalidToken(Exception):
    """Invalid Token Exception"""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class InvalidPrincipal(Exception):
    """Invalid Principal Exception"""	
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class InvalidGroup(Exception):
    """Invalid Group Exception"""	
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class InvalidPermission(Exception):
    """Invalid Permission Exception"""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
                