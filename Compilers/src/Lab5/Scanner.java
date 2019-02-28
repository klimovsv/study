package Lab5;


import java.util.ArrayList;

import static Lab5.DomainTag.*;

public class Scanner {
    String prog;
    private Compiler compiler;
    private Position cur;
    private ArrayList<Fragment> comments;
    private int state = 0;
    private ArrayList<ArrayList<Integer>> transfer = new ArrayList<>();

    private int[][] f = new int[][]{
            //         ws +  -1 (  )  *  num a  b  c  e  k  r  s else , undef
            new int[] {14,11,15,16,-1,-1,13, 5, 6, 1, 5, 5, 5, 5, 5,-1},//0
            new int[] {-1,-1,-1,-1,-1,-1, 5, 2, 5, 5, 5, 5, 5, 5, 5,-1},//1
            new int[] {-1,-1,-1,-1,-1,-1, 5, 5, 5, 5, 5, 5, 5, 3, 5,-1},//2
            new int[] {-1,-1,-1,-1,-1,-1, 5, 5, 5, 5, 4, 5, 5, 5, 5,-1},//3
            new int[] {-1,-1,-1,-1,-1,-1, 5, 5, 5, 5, 5, 5, 5, 5, 5,-1},//4
            new int[] {-1,-1,-1,-1,-1,-1, 5, 5, 5, 5, 5, 5, 5, 5, 5,-1},//5
            new int[] {-1,-1,-1,-1,-1,-1, 5, 5, 5, 5, 5, 5, 7, 5, 5,-1},//6
            new int[] {-1,-1,-1,-1,-1,-1, 5, 5, 5, 5, 8, 5, 5, 5, 5,-1},//7
            new int[] {-1,-1,-1,-1,-1,-1, 5, 9, 5, 5, 5, 5, 5, 5, 5,-1},//8
            new int[] {-1,-1,-1,-1,-1,-1, 5, 5, 5, 5, 5,10, 5, 5, 5,-1},//9
            new int[] {-1,-1,-1,-1,-1,-1, 5, 5, 5, 5, 5, 5, 5, 5, 5,-1},//10
            new int[] {-1,12,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1},//11
            new int[] {-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1},//12
            new int[] {-1,-1,-1,-1,-1,-1,13,-1,-1,-1,-1,-1,-1,-1,-1,-1},//13
            new int[] {14,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1},//14
            new int[] {-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1},//15
            new int[] {-1,-1,-1,-1,-1,17,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1},//16
            new int[] {19,19,-1,19,19,18,19,19,19,19,19,19,19,19,19,19},//17
            new int[] {19,19,-1,19,20,18,19,19,19,19,19,19,19,19,19,19},//18
            new int[] {19,19,-1,19,19,18,19,19,19,19,19,19,19,19,19,19},//19
            new int[] {-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1},//20
    };

    private DomainTag[] finalStates = new DomainTag[]{
            NOT_FINAL, //0
            IDENT, //1
            IDENT,//2
            IDENT,//3
            RESERVED,//4
            IDENT,//5
            IDENT,//6
            IDENT,//7
            IDENT,//8
            IDENT,//9
            RESERVED,//10
            OP,//11
            OP,//12
            NUMBER,//13
            WS,//14
            EOF,//15
            NOT_FINAL,//16
            NOT_FINAL,//17
            NOT_FINAL,//18
            NOT_FINAL,//19
            COMMENT //20
    };

    private int factorized(int c){
        if(c == '\n' || c =='\t' || c == ' ' || c == '\r') return 0; // ws
        if(c == '+') return 1; //+
        if(c == -1) return 2; //-1
        if(c == '(') return 3; //(
        if(c == ')') return 4; //)
        if(c == '*') return 5; //*
        if(c >= '0' && c <='9') return 6;//num
        if(c == 'a') return 7;//a
        if(c == 'b') return 8;//b
        if(c == 'c') return 9;//c
        if(c == 'e') return 10;//e
        if(c == 'k') return 11;//k
        if(c == 'r') return 12;//r
        if(c == 's') return 13;//s
        if(c == 'd' ||
                c >='f' && c <='j' ||
                c >='l' && c <='q' ||
                c >='t' && c <='z' ||
                c >='A' && c <='Z') return 14; //else
        return 15;
    }

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
        Position start = cur;
        while (true){
            Integer current = factorized(cur.getChar());
            int nextState = f[state][current];
            if(nextState == -1){
                if(finalStates[state] == NOT_FINAL){
                    if(state == 0 ) cur = cur.skip();
                    state = 0;
                    return new Token(UNEXPECTED_ERROR,start,cur,prog.substring(start.getIndex(),cur.getIndex()));
                }else{
                    DomainTag tag = finalStates[state];
                    state = 0;
                    return new Token(tag,start,cur,prog.substring(start.getIndex(),cur.getIndex()));
                }
            }else {
                state = nextState;
                cur = cur.skip();
            }
        }
    }

    public void scan(){
        System.out.println(prog);
        Token tok = nextToken();
        do{
            if(tok.tag != WS){
                System.out.println(tok);
            }
            tok = nextToken();
        }while (tok.tag != EOF);
    }
}
