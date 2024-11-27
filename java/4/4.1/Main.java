import java.util.ArrayDeque;
import java.util.Deque;

public class Main {
    
    public static void main(String[] args) {
        String expression = "(1+2+3)(5-2)*3-5";
        
        if (isValidSyntax(expression)) {
            System.out.println("Выражение корректно.");
            System.out.println("Результат вычисления: " + evaluateExpression(expression));
        } else {
            System.out.println("Ошибка: некорректный синтаксис выражения.");
        }
    }

    public static boolean isValidSyntax(String expression) {
        Deque<Character> stack = new ArrayDeque<>();
        
        for (char c : expression.toCharArray()) {

            if (c == '(' || c == '{' || c == '[') {
                stack.push(c);
            } else if (c == ')' || c == '}' || c == ']') {
                if (stack.isEmpty()) {
                    return false;
                }
                char last = stack.pop();
                if (!isMatchingPair(last, c)) {
                    return false;
                }
            }
        }
        
        return stack.isEmpty();
    }

    private static boolean isMatchingPair(char open, char close) {
        return (open == '(' && close == ')') || (open == '{' && close == '}') || (open == '[' && close == ']');
    }

    public static int evaluateExpression(String expression) {
        expression = expression.replaceAll("\\s", "");
        return evaluateSimpleExpression(expression);
    }

    private static int evaluateSimpleExpression(String expression) {
        Deque<Integer> values = new ArrayDeque<>();
        Deque<Character> operators = new ArrayDeque<>();

        int i = 0;
        while (i < expression.length()) {
            char ch = expression.charAt(i);

            if (Character.isDigit(ch)) {
                int value = 0;
                while (i < expression.length() && Character.isDigit(expression.charAt(i))) {
                    value = value * 10 + (expression.charAt(i) - '0');
                    i++;
                }
                values.push(value);
            } else if (ch == '+' || ch == '-' || ch == '*') {
                while (!operators.isEmpty() && precedence(operators.peek()) >= precedence(ch)) {
                    values.push(applyOperator(operators.pop(), values.pop(), values.pop()));
                }
                operators.push(ch);
                i++;
            } else if (ch == '(' || ch == '{' || ch == '[') {
                operators.push(ch);
                i++;
            } else if (ch == ')' || ch == '}' || ch == ']') {
                while (operators.peek() != '(' && operators.peek() != '{' && operators.peek() != '[') {
                    values.push(applyOperator(operators.pop(), values.pop(), values.pop()));
                }
                operators.pop();
                i++;
                if (i < expression.length() && (expression.charAt(i) == '(' || expression.charAt(i) == '{' || expression.charAt(i) == '[')) {
                    operators.push('*');
                }
            } else {
                i++;
            }
        }

        while (!operators.isEmpty()) {
            values.push(applyOperator(operators.pop(), values.pop(), values.pop()));
        }

        return values.pop();
    }

    private static int applyOperator(char operator, int b, int a) {
        switch (operator) {
            case '+':
                return a + b;
            case '-':
                return a - b;
            case '*':
                return a * b;
            default:
                throw new IllegalArgumentException("Недопустимый оператор: " + operator);
        }
    }

    private static int precedence(char operator) {
        if (operator == '+' || operator == '-') {
            return 1;
        } else if (operator == '*') {
            return 2;
        }
        return -1;
    }
}
