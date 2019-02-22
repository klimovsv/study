package Lab8;

import java.util.ArrayList;

public class Scanner {
    String prog;
    private Compiler compiler;
    private Position cur;
    private ArrayList<Fragment> comments;

    public ArrayList<Fragment> getComments() {
        return comments;
    }

    public Scanner(String prog, Compiler compiler) {
        this.compiler = compiler;
        cur = new Position(prog);
        this.prog = prog;
        comments = new ArrayList<>();
    }

    public Compiler getCompiler() {
        return compiler;
    }

    public Token nextToken(){
        while (cur.getChar()!=-1){
//            System.out.println(cur.getChar());
            cur = cur.skipWhile(Character::isWhitespace);
            Position start = cur;
            switch (cur.getChar()){
                case '=' :
                    cur = cur.skip();
                    return new SpecToken(DomainTag.ASSIGN,start,cur,"=");
                case '$':
                    do{
                        cur = cur.skip();
                    }while (cur.isLetter());

                    String tok = prog.substring(start.skip().getIndex(),cur.getIndex());
                    switch (tok){
                        case "RULE":
                            return new SpecToken(DomainTag.RTOK,start,cur,"$RULE");
                        case "TERM":
                            return new SpecToken(DomainTag.TTOK,start,cur,"$TERM");
                        case "NTERM":
                            return new SpecToken(DomainTag.NTOK,start,cur,"$NTERM");
                        case "EPS":
                            return new SpecToken(DomainTag.EPS,start,cur,"$EPS");
                            default:
                                return new SpecToken(DomainTag.UNEXPECTED,start,cur,prog.substring(start.getIndex(),cur.getIndex()));
                    }
                case '(':
                    cur = cur.skip();
                    return new SpecToken(DomainTag.LPAREN,start,cur,"(");
                case ')':
                    cur = cur.skip();
                    return new SpecToken(DomainTag.RPAREN,start,cur,")");
                case '}':
                    cur = cur.skip();
                    return new SpecToken(DomainTag.RBRAC,start,cur,"}");
                    case '{':
                    cur = cur.skip();
                    return new SpecToken(DomainTag.LBRAC,start,cur,"{");
                    case '"':
                    cur = cur.skip();
                    if(cur.getChar()!= '\n' && cur.skip().getChar()=='"'){
                        cur = cur.skip().skip();
//                        System.out.println(2);
                        return new SpecToken(DomainTag.TERM,start,cur,prog.substring(start.getIndex(),cur.getIndex()));
                    }
//                    System.out.println(prog.substring(start.getIndex(),cur.getIndex()));
                    return new SpecToken(DomainTag.UNEXPECTED,start,cur,prog.substring(start.getIndex(),cur.getIndex()));
                case '|':
                    cur = cur.skip();
                    return new SpecToken(DomainTag.ALTER,start,cur,"|");
                    default:
                        while (cur.getChar() >= 'A' && cur.getChar() <= 'Z') cur = cur.skip();
                        if(cur.getIndex() - start.getIndex() == 1){
                            return new SpecToken(DomainTag.NTERM,start,cur,prog.substring(start.getIndex(),cur.getIndex()));
                        }
                        return new SpecToken(DomainTag.UNEXPECTED,start,cur = cur.skip(),prog.substring(start.getIndex(),cur.skip().getIndex()));
            }
        }
        return new SpecToken(DomainTag.END_OF_PROGRAMM,cur,cur,"EOF");
    }

    ArrayList<Token> scan(){
        ArrayList<Token> tokens = new ArrayList<>();
        Token tok;
        do {
            tok = this.nextToken();
            tokens.add(tok);
        }while (tok.tag!= DomainTag.END_OF_PROGRAMM);
        return tokens;
    }
}
