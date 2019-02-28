package Lab8;

public class TokenException extends Exception {
    TokenException(Token tok){
        super("syntax error : " + tok.toString());
    }
}
