package Lab8;
import java.util.*;
import static Lab8.DomainTag.*;

public class Compiler {
    private Scanner sc;

    private ArrayList<Token> tokens;
    private Token tok;
    private HashMap<String,ArrayList<RuleFragment>> rules = new HashMap<>();
    private HashMap<String,HashSet<String>> firsts = new HashMap<>();
    private HashMap<String,Node> ruleNodes = new HashMap<>();
    private String currRule;
    private int tokPos;

    public Compiler() {
        tokPos = -1;
    }

    public HashMap<String, HashSet<String>> getFirsts() {
        return firsts;
    }

    public HashMap<String, Node> getRuleNodes() {
        return ruleNodes;
    }

    //first(S) = first(D) = Ntok,Ttok
    //first(R) = Rtok
    //first(E) = first(E1) = {,(,N,T

    // Ntok ::= $NTERM
    // Ttok ::= $TERM
    // N ::= [A-Z]
    // T ::= "."

    // S ::= D R
    // D ::= (Ntok N N* | Ttok T T*)+
    // R ::= (RULE)+
    // RULE ::= Rtok N Assign E ("|" E)*
    // E ::= ( BRAC | PAREN  | (N|T))+
    // E1 ::= E ("|" E)*
    // BRAC ::= "{" E "}"
    // PAREN ::= "(" E1 ")"

    Token next(){
        tokPos++;
        if(tokPos < tokens.size()){
            return tokens.get(tokPos);
        }else {
            tokPos--;
            return tokens.get(tokens.size()-1);
        }
    }

    void parse() throws TokenException{
        tokens = sc.scan();
        tokPos = -1;
        tok = next();
        Node root = parseS();
        if(tok.tag != END_OF_PROGRAMM) tokenError();

        root.printTree();

        generateFirsts();
        printFirsts();
        printRules();
    }

    Node parseS() throws TokenException{
        Node n = new Node(S);
        n.addNode(parseD());
        n.addNode(parseR());
        return n;
    }

    void tokenError() throws TokenException{
        throw new TokenException(tok);
    }

    Node parseBrac()throws TokenException{
        Node node = new Node(BRAC);
        tok = next();
        node.addNode(parseE());
        if(tok.tag == RBRAC){
            tok = next();
        }else {
            tokenError();
        }
        return node;
    }

    Node parseParen()throws TokenException{
        Node node = new Node(PAREN);
        tok = next();
        node.addNode(parseE1());
        if(tok.tag == RPAREN){
            tok = next();
        }else {
            tokenError();
        }
        return node;
    }

    Node parseD()throws TokenException{
        Node node = new Node(D);
        do{
            if(tok.tag == NTOK){
                node.addNode(new Node(tok));
                tok = next();
                if(tok.tag == NTERM){
                    node.addNode(new Node(tok));
                    tok = next();
                }else {
                    tokenError();
                }
                while (tok.tag == NTERM){
                    node.addNode(new Node(tok));
                    tok = next();
                }
            }else if (tok.tag == TTOK){
                node.addNode(new Node(tok));
                tok = next();
                if(tok.tag == TERM){
                    node.addNode(new Node(tok));
                    tok = next();
                }else {
                    tokenError();
                }
                while (tok.tag == TERM){
                    node.addNode(new Node(tok));
                    tok = next();
                }
            }else{
                tokenError();
            }
        }while (tok.tag == NTOK || tok.tag == TTOK);
        return node;
    }

    Node parseRule()throws TokenException{
        Node node = new Node(RULE);
        int start;
        node.addNode(new Node(tok));
        tok = next();
        if(tok.tag == NTERM){
            node.addNode(new Node(tok));
            currRule = tok.getAttr();
            initRule(tok.getAttr());
            tok = next();
            ruleNodes.put(currRule,node);
        }else {
            tokenError();
        }
        if(tok.tag == ASSIGN){
            node.addNode(new Node(tok));
            tok = next();
        }else {
            tokenError();
        }
        start = tokPos;
        node.addNode(parseE());
        rules.get(currRule).add(new RuleFragment(tokens,start,tokPos));
        while (tok.tag == ALTER){
            tok = next();
            start = tokPos;
            node.addNode(parseE());
            rules.get(currRule).add(new RuleFragment(tokens,start,tokPos));
        }
        return node;
    }

    Node parseR()throws TokenException{
        Node node = new Node(R);
        do{
            if(tok.tag == RTOK){
                node.addNode(parseRule());
            }else {
                tokenError();
            }
        }while (tok.tag == RTOK);
        return node;
    }

    Node parseE()throws TokenException{
        Node node = new Node(E);
        do{
            if(tok.tag == LBRAC){
                node.addNode(parseBrac());
            }else if(tok.tag == LPAREN){
                node.addNode(parseParen());
            }else if(tok.tag == TERM || tok.tag == NTERM){
                node.addNode(new Node(tok));
                tok = next();
            }else {
                tokenError();
            }
        } while (tok.tag == TERM || tok.tag == NTERM || tok.tag == LPAREN || tok.tag == LBRAC);
        return node;
    }

    Node parseE1()throws TokenException{
        Node node = new Node(E1);
        node.addNode(parseE());
        while (tok.tag == ALTER){
            tok = next();
            node.addNode(parseE());
        }
        return node;
    }


    void generateFirsts(){
        State currState = new State(firsts);
        State newState = currState;
        do{
            currState = newState;

            ruleNodes.forEach((s, node) -> {
                firsts.get(s).addAll(node.getFirst(this));
            });

            newState = new State(firsts);
        }while (!currState.equals(newState));
    }

//    HashSet<String> getFirst(RuleFragment fragment){
//        HashSet<String> firsts = new HashSet<>();
//        ArrayList<Token> fragmentTokens = fragment.getTokens();
//        Token startToken = fragmentTokens.get(0);
//        if(startToken.tag == TERM){
//            firsts.add(startToken.getAttr());
//            return firsts;
//        }else if(startToken.tag == NTERM){
//            if(this.firsts.get(startToken.getAttr()).contains("e") && fragmentTokens.size() > 1){
//                HashSet<String> set = (HashSet<String>) this.firsts.get(startToken.getAttr()).clone();
//                set.remove("e");
//                firsts.addAll(set);
//                firsts.addAll(getFirst(new RuleFragment(tokens,fragment.start + 1, fragment.end)));
//            }else{
//                firsts.addAll(this.firsts.get(startToken.getAttr()));
//            }
//            return firsts;
//        }else if(startToken.tag == LBRAC){
//            int newEnd = skipBrac(fragment);
//            if(newEnd == fragment.end) {
//                firsts.add("e");
//            }else {
//                firsts.addAll(getFirst(new RuleFragment(tokens,newEnd,fragment.end)));
//            }
//            firsts.addAll(getFirst(new RuleFragment(tokens,fragment.start + 1, newEnd - 1)));
//            return firsts;
//        }else if(startToken.tag == LPAREN){
//            int newEnd = skipParen(fragment);
//            ArrayList<RuleFragment> fragments = extractFragments(new RuleFragment(tokens,fragment.start + 1,newEnd - 1));
//            for(RuleFragment fragment1 : fragments){
//                firsts.addAll(getFirst(fragment1));
//            }
//            if(firsts.contains("e") && newEnd != fragment.end){
//                firsts.remove("e");
//                firsts.addAll(getFirst(new RuleFragment(tokens,newEnd,fragment.end)));
//            }
//            return firsts;
//        }
//        return firsts;
//    }

    void printRules(){
        System.out.println("rules");
        rules.forEach((rule,list) ->{
            System.out.print(rule +" ::= ");
            StringBuilder rules = new StringBuilder();
            for (RuleFragment ruleFragment: list){
                rules.append("| ");
                rules.append(ruleFragment);
            }
            System.out.println(rules.substring(1));
        });
    }

    void printFirsts(){
        System.out.println("first for nterms");
        firsts.forEach((rule,set) ->{
            System.out.print(rule + " : ");
            set.forEach((s) -> System.out.print(s+", "));
            System.out.println();
        });
        System.out.println();
    }

    void initRule(String rule){
        rules.put(rule,new ArrayList<>());
        firsts.put(rule,new HashSet<>());
    }



    public Scanner getScanner(String prog){
        sc = new Scanner(prog,this);
        return sc;
    }
}
