package Lab8;

import java.util.ArrayList;

public class RuleFragment {
    int start,end;
    ArrayList<Token> tokens;

    RuleFragment(ArrayList<Token> tokens,int start,int end){
        this.end = end;
        this.start = start;
        this.tokens = tokens;
    }

    ArrayList<Token> getTokens(){
        return new ArrayList<>(tokens.subList(start,end));
    }

    @Override
    public String toString() {
        StringBuilder res = new StringBuilder();
        for(Token token : getTokens()){
            res.append(" ");
            res.append(token.getAttr());
        }
        return res.substring(1);
    }
}
