import enum

class TokenType(enum.Enum):
    # Single-character tokens.
    LEFT_PAREN      = 1
    RIGHT_PAREN     = 2
    LEFT_BRACE      = 3
    RIGHT_BRACE     = 4
    COMMA           = 5
    DOT             = 6
    MINUS           = 7
    PLUS            = 8
    SEMICOLON       = 9 
    SLASH           = 10 
    STAR            = 11

    # One or two character tokens.
    BANG            = 100
    BANG_EQUAL      = 101
    EQUAL           = 102 
    EQUAL_EQUAL     = 103
    GREATER         = 104
    GREATER_EQUAL   = 105
    LESS            = 106
    LESS_EQUAL      = 107

    # Literals.
    IDENTIFIER      = 200
    STRING          = 201
    NUMBER          = 202

    # Keywords.
    AND             = 300
    CLASS           = 301
    ELSE            = 302
    FALSE           = 303
    FUN             = 304
    FOR             = 305
    IF              = 306
    NIL             = 307
    OR              = 308
    PRINT           = 309 
    RETURN          = 310
    SUPER           = 311
    THIS            = 312
    TRUE            = 313
    VAR             = 314
    WHILE           = 315


    EOF             = -1