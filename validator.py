class Validator:
    PARENTHESES_MAP = {
        '(':')',
        '{':'}',
        '[':']'
        }

    def is_valid_parentheses(self, expression):
        parentheses_stack=[]
        for char in expression:
            if char in self.PARENTHESES_MAP:
                parentheses_stack.append(char)
            elif len(parentheses_stack) == 0 or self.PARENTHESES_MAP[parentheses_stack.pop()] != char:
                return False
        return len(parentheses_stack) == 0

    def display_results(self, expression, validity):
        if validity:
            print expression, " : Valid parentheses expression."
        else:
            print expression, " : Invalid parentheses expression."

def main():
    invalid_expression = "(){}}"
    valid_expression = "(){}"
    validator = Validator()
    validator.display_results(invalid_expression, validator.is_valid_parentheses(invalid_expression))
    validator.display_results(valid_expression, validator.is_valid_parentheses(valid_expression))

if __name__=='__main__':
    main()
