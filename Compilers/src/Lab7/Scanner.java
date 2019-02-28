package Lab7;

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
            while (cur.isWhiteSpace()){
                if(cur.getChar()=='\n') break;
                else cur = cur.skip();
            }
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
                        case "AXIOM" :
                            return new SpecToken(DomainTag.AXIOM,start,cur,"$AXIOM");
                        case "RULE":
                            return new SpecToken(DomainTag.RULE,start,cur,"$RULE");
                        case "TERM":
                            return new SpecToken(DomainTag.TERM_TOK,start,cur,"$TERM");
                        case "NTERM":
                            return new SpecToken(DomainTag.NTERM_TOK,start,cur,"$NTERM");
                        case "EPS":
                            return new SpecToken(DomainTag.EPS,start,cur,"$EPS");
                            default:
                                return new SpecToken(DomainTag.UNEXPECTED,start,cur,"UNEXPECTED");
                    }
                case '"':
                    cur = cur.skip();
                    if(cur.getChar()!= '\n' && cur.skip().getChar()=='"'){
                        cur = cur.skip().skip();
                        return new SpecToken(DomainTag.TERM,start,cur,prog.substring(start.getIndex(),cur.getIndex()));
                    }
                    return new SpecToken(DomainTag.UNEXPECTED,start,cur,"UNEXPECTED");
                case '\n':
                    cur = cur.skip();
                    return new SpecToken(DomainTag.LINE,start,cur,"\n");
                    default:
                        while (cur.isLetter()) cur = cur.skip();

                        if (cur.getIndex()!=start.getIndex()) {
                            if (cur.getChar() == '\'') cur = cur.skip();
                            if (cur.getIndex()-start.getIndex() <= 2) return new SpecToken(DomainTag.NTERM,start,cur,prog.substring(start.getIndex(),cur.getIndex()));
                        }

                        return new SpecToken(DomainTag.UNEXPECTED,start,cur,"UNEXPECTED");
            }
        }
        return new SpecToken(DomainTag.END_OF_PROGRAMM,cur,cur,"EOF");
    }

    public ArrayList<Token> scan(){

        ArrayList<Token> tokens = new ArrayList<>();
        Token tok;
        do {
            tok = nextToken();
            tokens.add(tok);
            if(tok.tag == DomainTag.UNEXPECTED){
                System.out.println("Syntax error " + tok);
                return null;
            }
        }while (tok.tag!= DomainTag.END_OF_PROGRAMM);

        tokens.forEach(System.out::println);
        return tokens;

//        System.out.println("PROGRAM:\n" + prog + "\nTOKENS:");
//        Token tok;
//        while ((tok = nextToken()).tag != DomainTag.END_OF_PROGRAMM){
//            System.out.println(tok.toString() + " " + tok.getAttr(this));
//        }
//        System.out.println(tok +" " + tok.getAttr(this));
//        System.out.println("COMMENTS:");
//        comments.forEach(System.out::println);
//        System.out.println("MESSAGES:");
//        compiler.outputMessages();
    }
}
