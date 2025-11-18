# Parser mit recursive descent
from lexer import Lexer, Token

class ParseError(Exception):
    """Exception für Parser-Fehler"""
    pass

class Parser:
    def __init__(self, input_string: str):
        """Initialisiert den Parser mit einem Input-String"""
        self.lexer = Lexer(input_string)
        self.current_token = None
        self.advance()  # Lese das erste Token
    
    def advance(self):
        """Liest das nächste Token vom Lexer"""
        self.current_token = self.lexer.nextToken()
    
    def match(self, expected_type: str):
        """
        Prüft, ob das aktuelle Token vom erwarteten Typ ist.
        Bei Übereinstimmung wird zum nächsten Token weitergegangen.
        Andernfalls wird ein Fehler geworfen.
        """
        if self.current_token.type == expected_type:
            token = self.current_token
            self.advance()
            return token
        else:
            raise ParseError(
                f"Erwartetes Token: {expected_type}, "
                f"Tatsächliches Token: <{self.current_token.type}, {self.current_token.content}>"
            )
    
    def check(self, token_type):
        """
        Überprüft, ob der aktuelle Token vom angegebenen Typ ist
        """
        if self.current_token is None:
            return False
        return self.current_token.type == token_type
    
    # start: stmt*
    def parse_start(self):
        """
        Startregel der Grammatik: start -> stmt*
        """
        statements = []
        while not self.check("<EOF>"):
            # Überspringe Kommentare auf oberster Ebene
            if self.check("COMMENT"):
                self.advance()
                continue
            stmt = self.parse_stmt()
            statements.append(stmt)
        return {"type": "Program", "statements": statements}
    
    # stmt: literal | expr+
    def parse_stmt(self):
        """
        Statement-Regel: stmt -> literal | expr+
        """
        if self.check("LBRACKET"):
            # expr+
            expressions = []
            while self.check("LBRACKET"):
                expressions.append(self.parse_expr())
            if len(expressions) == 1:
                return expressions[0]
            return {"type": "ExpressionSequence", "expressions": expressions}
        else:
            # literal
            return self.parse_literal()
    
    # expr: '(' ((operator (literal | expr)+) | function | functioncall) COMMENT* ')'
    def parse_expr(self):
        """
        Expression-Regel: expr -> '(' ((operator (literal | expr)+) | function | functioncall) COMMENT* ')'
        """
        self.match("LBRACKET")
        
        # Schaue nach, was nach der Klammer kommt
        if self.check("COMP") or self.check("ARITH"):
            # operator (literal | expr)+
            op = self.parse_operator()
            operands = []
            while not self.check("RBRACKET") and not self.check("COMMENT"):
                if self.check("LBRACKET"):
                    operands.append(self.parse_expr())
                else:
                    operands.append(self.parse_literal())
            
            # Überspringe optionale Kommentare
            while self.check("COMMENT"):
                self.advance()
            
            self.match("RBRACKET")
            return {"type": "Operation", "operator": op, "operands": operands}
        
        elif self.check("ID"):
            # Könnte function oder functioncall sein
            # Schaue voraus: wenn nächstes Token '(' ist, dann function (defn ID ...)
            # Aber 'defn' ist ein spezielles ID
            if self.current_token.content == "defn":
                result = self.parse_function()
            elif self.current_token.content in ["def", "let"]:
                # Spezielle Formen (def, let)
                result = self.parse_special_form()
            else:
                # functioncall: ID (literal | expr)+
                result = self.parse_functioncall()
            
            # Überspringe optionale Kommentare
            while self.check("COMMENT"):
                self.advance()
            
            self.match("RBRACKET")
            return result
        
        else:
            raise ParseError(
                f"Erwartetes Token: COMP, ARITH oder ID am Anfang einer Expression, "
                f"Tatsächliches Token: <{self.current_token.type}, {self.current_token.content}>"
            )
    
    # operator: COMP | ARITH
    def parse_operator(self):
        """
        Operator-Regel: operator -> COMP | ARITH
        """
        if self.check("COMP"):
            return self.match("COMP").content
        elif self.check("ARITH"):
            return self.match("ARITH").content
        else:
            raise ParseError(
                f"Erwartetes Token: COMP oder ARITH, "
                f"Tatsächliches Token: <{self.current_token.type}, {self.current_token.content}>"
            )
    
    # literal: NUM | ID | BOOL | COMMENT | STRING
    def parse_literal(self):
        """
        Literal-Regel: literal -> NUM | ID | BOOL | COMMENT | STRING
        """
        if self.check("NUM"):
            token = self.match("NUM")
            return {"type": "Number", "value": int(token.content)}
        elif self.check("BOOL"):
            token = self.match("BOOL")
            return {"type": "Boolean", "value": token.content == "true"}
        elif self.check("STRING"):
            token = self.match("STRING")
            return {"type": "String", "value": token.content}
        elif self.check("ID"):
            token = self.match("ID")
            return {"type": "Identifier", "name": token.content}
        elif self.check("COMMENT"):
            token = self.match("COMMENT")
            return {"type": "Comment", "text": token.content}
        else:
            raise ParseError(
                f"Erwartetes Token: NUM, ID, BOOL, COMMENT oder STRING, "
                f"Tatsächliches Token: <{self.current_token.type}, {self.current_token.content}>"
            )
    
    # function: 'defn' ID '(' (ID)* ')' expr
    def parse_function(self):
        """
        Function-Definition-Regel: function -> 'defn' ID '(' (ID)* ')' expr
        """
        defn_token = self.match("ID")  # 'defn'
        if defn_token.content != "defn":
            raise ParseError(
                f"Erwartetes Token: 'defn', "
                f"Tatsächliches Token: <ID, {defn_token.content}>"
            )
        
        name = self.match("ID")
        self.match("LBRACKET")
        
        # Parameter sammeln
        parameters = []
        while self.check("ID"):
            param = self.match("ID")
            parameters.append(param.content)
        
        self.match("RBRACKET")
        
        # Function body
        body = self.parse_expr()
        
        return {
            "type": "FunctionDefinition",
            "name": name.content,
            "parameters": parameters,
            "body": body
        }
    
    # functioncall: ID (literal | expr)+
    def parse_functioncall(self):
        """
        Function-Call-Regel: functioncall -> ID (literal | expr)+
        """
        name = self.match("ID")
        
        arguments = []
        while not self.check("RBRACKET") and not self.check("COMMENT"):
            if self.check("LBRACKET"):
                arguments.append(self.parse_expr())
            else:
                arguments.append(self.parse_literal())
        
        return {
            "type": "FunctionCall",
            "name": name.content,
            "arguments": arguments
        }
    
    def parse_special_form(self):
        """
        Behandelt spezielle Forms wie 'def' und 'let'
        """
        keyword = self.match("ID")
        
        if keyword.content == "def":
            # (def name value)
            name = self.match("ID")
            if self.check("LBRACKET"):
                value = self.parse_expr()
            else:
                value = self.parse_literal()
            
            return {
                "type": "Definition",
                "name": name.content,
                "value": value
            }
        
        elif keyword.content == "let":
            # (let (bindings...) body)
            self.match("LBRACKET")
            
            # Bindings sammeln
            bindings = []
            while not self.check("RBRACKET"):
                if self.check("COMMENT"):
                    self.advance()
                    continue
                if not self.check("ID"):
                    break
                name = self.match("ID")
                
                # Überspringe Kommentare zwischen Name und Wert
                while self.check("COMMENT"):
                    self.advance()
                
                if self.check("LBRACKET"):
                    value = self.parse_expr()
                else:
                    value = self.parse_literal()
                bindings.append({"name": name.content, "value": value})
                
                # Überspringe Kommentare nach dem Wert
                while self.check("COMMENT"):
                    self.advance()
            
            self.match("RBRACKET")
            
            # Überspringe Kommentare vor dem Body
            while self.check("COMMENT"):
                self.advance()
            
            # Body
            body = self.parse_expr()
            
            return {
                "type": "Let",
                "bindings": bindings,
                "body": body
            }
        
        else:
            # Fallback: behandle als function call
            arguments = []
            while not self.check("RBRACKET") and not self.check("COMMENT"):
                if self.check("LBRACKET"):
                    arguments.append(self.parse_expr())
                else:
                    arguments.append(self.parse_literal())
            
            return {
                "type": "FunctionCall",
                "name": keyword.content,
                "arguments": arguments
            }
    
    def parse(self):
        """
        Hauptmethode zum Parsen des gesamten Programms
        """
        try:
            return self.parse_start()
        except ParseError as e:
            print(f"Parse-Fehler: {e}")
            raise


def pretty_print(ast, indent=0):
    """Hilfsfunktion zum schönen Ausgeben des AST"""
    prefix = "  " * indent
    if isinstance(ast, dict):
        print(f"{prefix}{ast.get('type', 'Unknown')}")
        for key, value in ast.items():
            if key != 'type':
                print(f"{prefix}  {key}:")
                if isinstance(value, list):
                    for item in value:
                        pretty_print(item, indent + 2)
                else:
                    pretty_print(value, indent + 2)
    elif isinstance(ast, list):
        for item in ast:
            pretty_print(item, indent)
    else:
        print(f"{prefix}{ast}")


if __name__ == "__main__":
    # Teste den Parser mit der test.txt Datei
    with open("Sheet04/test.txt", "r") as f:
        input_code = f.read()
    
    print("=== Input Code ===")
    print(input_code)
    print("\n=== Parsing ===")
    
    try:
        parser = Parser(input_code)
        ast = parser.parse()
        
        print("\n=== Abstract Syntax Tree ===")
        pretty_print(ast)
        
        print("\n=== Parse erfolgreich! ===")
    except ParseError as e:
        print(f"\n=== Parse-Fehler aufgetreten ===")
        print(f"Fehler: {e}")
    except Exception as e:
        print(f"\n=== Unerwarteter Fehler ===")
        print(f"Fehler: {e}")
        import traceback
        traceback.print_exc()