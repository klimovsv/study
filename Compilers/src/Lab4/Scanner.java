package Lab4;
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
            cur = cur.skipWhile(Character::isWhitespace);
            Position start = cur;
            switch (cur.getChar()){
                case '{':
                    if(cur.skip().getChar() !='-'){
                        compiler.addMessage(true,cur,"needs \'-\' character");
                    }

                    do {
                        do {
                            cur = cur.skip();
                        }while (cur.getChar()!= '-' && cur.getChar()!=-1);
                        cur = cur.skip();
                    }while (cur.getChar()!='}' && cur.getChar()!=-1);

                    if(cur.getChar() == -1){
                        compiler.addMessage(true,cur,"end of prog found \'}\' expected");
                    }
                    comments.add(new Fragment(start,cur.skip()));
                    cur = cur.skip();
                    break;
                case '-':
                    if (cur.skip().getChar() != '-'){
                        compiler.addMessage(true,cur,"needs \'-\' character");
                    }
                    cur = cur.skipWhile(ch -> ch != '\n' && ch != -1);
                    comments.add(new Fragment(start,cur));
                    cur = cur.skip();
                    break;
                default:
                    if (cur.isLetter()){
                        cur = cur.skipWhile(Character::isLetterOrDigit);
                        String name = prog.substring(start.getIndex(),cur.getIndex());
                        return new IdentToken(start,cur,compiler.addName(name));
                    }else if(cur.isDigit()){
                        //пропускаем все цифры
                        do {
                            cur = cur.skip();
                        }while (cur.isDigit());

                        //елси нет . или е , то целое число
                        if(cur.getChar()!='.' && cur.getChar()!='e' && cur.getChar()!='E' ){
                            if (!cur.isWhiteSpace()) compiler.addMessage(true,cur,"needs delimiter");
                            return new NumberToken(start,cur,Long.parseLong(prog.substring(start.getIndex(),cur.getIndex())));
                        }

                        //если встретили точку
                        if(cur.getChar()=='.'){
//                            пропускаем цифры
                            do {
                                cur = cur.skip();
                            }while (cur.isDigit());
                            //если встретили е
                            if(cur.getChar()=='e' || cur.getChar()=='E'){
                                //если после e нет цифр, то возвращаем без е
                                if(!cur.skip().isDigit()){
                                    if (!cur.isWhiteSpace()) compiler.addMessage(true,cur,"needs delimiter");
                                    return new FloatNumberToken(start,cur,prog.substring(start.getIndex(),cur.getIndex()));
                                }
                                do {
                                    cur = cur.skip();
                                }while (cur.isDigit());
                            }
                            if (!cur.isWhiteSpace()) compiler.addMessage(true,cur,"needs delimiter");
                            return new FloatNumberToken(start,cur,prog.substring(start.getIndex(),cur.getIndex()));

                        }else if((cur.getChar()=='e' || cur.getChar()=='E')){
                            //если после e нет цифр, то возвращаем без е
                            if(!cur.skip().isDigit()){
                                if (!cur.isWhiteSpace()) compiler.addMessage(true,cur,"needs delimiter");
                                return new NumberToken(start,cur,Long.parseLong(prog.substring(start.getIndex(),cur.getIndex())));
                            }
                            do {
                                cur = cur.skip();
                            }while (cur.isDigit());
                            if (!cur.isWhiteSpace()) compiler.addMessage(true,cur,"needs delimiter");
                            return new FloatNumberToken(start,cur,prog.substring(start.getIndex(),cur.getIndex()));
                        }
                    }
                    else if (cur.getChar() != -1){
                        compiler.addMessage(true,cur,"unexpected character");
                        cur = cur.skip();
                    }
                    break;
            }
        }
        return new SpecToken(DomainTag.END_OF_PROGRAMM,cur,cur);
    }

    public void scan(){
        System.out.println("PROGRAM:\n" + prog + "\nTOKENS:");
        Token tok;
        while ((tok = nextToken()).tag != DomainTag.END_OF_PROGRAMM){
            System.out.println(tok.toString() + " " + tok.getAttr(this));
        }
        System.out.println(tok +" " + tok.getAttr(this));
        System.out.println("COMMENTS:");
        comments.forEach(System.out::println);
        System.out.println("MESSAGES:");
        compiler.outputMessages();
    }
}
