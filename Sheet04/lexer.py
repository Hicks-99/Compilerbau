import string
# Aus Text input wird Tokenstream :daumen_hoch:
# Welche Lexer-Regeln haben wir? 

#NUM     : [0-9]+ ;
#BOOL    : 'true' | 'false';
#STRING  : ["]~["]*["];
#ID      : [a-z][a-zA-Z]* ;
#COMP    : [=<>];
#ARITH   : [+\-*/];
#WS      : [ \t\n]+ -> skip;
#COMMENT : ';;' ~[\n]*;
char = ''

class Token: 
    def __init__(self, type:str, content:str):
        self.type = type
        self.content = content

    def __str__(self):
        return f"<{self.type}, {self.content}>"
    
    def __repr__(self) -> str:
        return f"<{self.type}, {self.content}>"

class Lexer: 
    def __init__(self, string): 
        self.string = string
        self.peek = ' '

    def nextToken(self):
        while self.peek != "<EOF>":
            match(self.peek):  
                case ' ' | '\t' | '\n': #WS
                    self.consume() 
                case _ if self.peek in string.digits: #NUM
                    return self.digits()
                case _ if self.peek in string.ascii_lowercase: #ID, BOOL
                    return self.idOrBool()
                case '"': #STRING
                    return self.stringerama()
                case "=" | "<" | ">": #COMP
                    tmp = self.peek
                    self.consume()
                    return Token("COMP", tmp)
                case "+" | "-" | "*" | "/": #ARITH
                    tmp = self.peek
                    self.consume()
                    return Token("ARITH", tmp)
                case ";" : #COMMENT
                    return self.comment()
                case '(':
                    self.consume()
                    return Token("LBRACKET", "(")
                case ')': 
                    self.consume()
                    return Token("RBRACKET", ")")
                case _: 
                    raise SyntaxError(f'Invalid Character {self.peek}')
            
            #print(char)
        return Token("<EOF>", "<EOF>")

    def consume(self):
        try: 
            self.peek = self.string[0]
            self.string = self.string[1:]
        except IndexError: 
            self.peek="<EOF>"

    def idOrBool(self): 
        buffer = ''
        while(True): 
            buffer += self.peek
            self.consume()
            if self.peek not in string.ascii_letters:
                break
        if buffer in ['true', 'false']:
            return Token("BOOL", buffer)
        return Token("ID", buffer) 
    
    def digits(self):
        buffer = ''
        while(True): 
            buffer += self.peek
            self.consume()
            if self.peek not in string.digits:
                return Token("NUM", buffer)
            
    def stringerama(self):
        buffer = ''
        while(True): 
            buffer += self.peek
            self.consume()
            if self.peek == '"':
                buffer+=self.peek
                self.consume()
                return Token("STRING", buffer)
            if self.peek == '<EOF>':
                raise EOFError
    
    def comment(self):
        buffer = ''
        full_comment = False
        while(True): 
            buffer += self.peek
            self.consume()
            #print(self.peek)
            if self.peek == ';':
                full_comment = True
            if full_comment and self.peek == "\n":
                break
            if self.peek == "<EOF>":
                break
        return Token("COMMENT", buffer)

if __name__ == "__main__":
    tokens = []
    with open("Sheet04/test.txt", "r") as f:
        mylex = Lexer(f.read())
        while True: 
            tokens.append(mylex.nextToken())
            if tokens[-1].type == "<EOF>":
                break
        print(tokens)
        print("\n")
        print([i.content for i in tokens])