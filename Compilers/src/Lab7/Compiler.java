package Lab7;

import javax.sound.sampled.Line;
import java.lang.reflect.Array;
import java.util.*;

import static Lab7.DomainTag.*;

//import static Lab7.DomainTag.LS;

public class Compiler {
    private TreeMap<Position, Message> messages;
    private HashMap<String,Integer> nameCodes;
    private ArrayList<String> names;

    private HashMap<DomainTag,HashMap<DomainTag,ArrayList<DomainTag>>> table = new HashMap<>();

    public Compiler() {
        messages = new TreeMap<>();
        nameCodes = new HashMap<>();
        names = new ArrayList<>();
        fillTable();
    }

    private void fillTable(){
        HashMap<DomainTag,ArrayList<DomainTag>> lstLS = new HashMap<>();
        lstLS.put(LINE,new ArrayList<>(){{add(LINE);add(LS);}});
        lstLS.put(END_OF_PROGRAMM,new ArrayList<>(){{add(BLANK);}});
        table.put(LS,lstLS);

        HashMap<DomainTag,ArrayList<DomainTag>> lstRL = new HashMap<>();
        lstRL.put(LINE,new ArrayList<>(){{add(BLANK);}});
        lstRL.put(RULE,new ArrayList<>(){{add(R);add(RL);}});
        lstRL.put(END_OF_PROGRAMM,new ArrayList<>(){{add(BLANK);}});
        table.put(RL,lstRL);

        HashMap<DomainTag,ArrayList<DomainTag>> lstR = new HashMap<>();
        lstR.put(RULE,new ArrayList<>(){{add(RULE);add(NTERM);add(ASSIGN);add(LST);add(L);add(TAIL);}});
        table.put(R,lstR);

        HashMap<DomainTag,ArrayList<DomainTag>> lstTail = new HashMap<>();
        lstTail.put(END_OF_PROGRAMM,new ArrayList<>(){{add(BLANK);}});
        lstTail.put(RULE,new ArrayList<>(){{add(BLANK);}});
        lstTail.put(LINE,new ArrayList<>(){{add(BLANK);}});
        lstTail.put(NTERM,new ArrayList<>(){{add(LST);add(L);add(TAIL);}});
        lstTail.put(TERM,new ArrayList<>(){{add(LST);add(L);add(TAIL);}});
        lstTail.put(EPS,new ArrayList<>(){{add(LST);add(L);add(TAIL);}});
        table.put(TAIL,lstTail);

        HashMap<DomainTag,ArrayList<DomainTag>> lstLST = new HashMap<>();
        lstLST.put(NTERM,new ArrayList<>(){{add(NTERM);add(LST1);}});
        lstLST.put(TERM,new ArrayList<>(){{add(TERM);add(LST1);}});
        lstLST.put(EPS,new ArrayList<>(){{add(EPS);}});
        table.put(LST,lstLST);

        HashMap<DomainTag,ArrayList<DomainTag>> lstLST1 = new HashMap<>();
        lstLST1.put(NTERM,new ArrayList<>(){{add(NTERM);add(LST1);}});
        lstLST1.put(TERM,new ArrayList<>(){{add(TERM);add(LST1);}});
        lstLST1.put(LINE,new ArrayList<>(){{add(BLANK);}});
        lstLST1.put(END_OF_PROGRAMM,new ArrayList<>(){{add(BLANK);}});
        table.put(LST1,lstLST1);

        HashMap<DomainTag,ArrayList<DomainTag>> lstL = new HashMap<>();
        lstL.put(LINE,new ArrayList<>(){{add(LINE);}});
        lstL.put(END_OF_PROGRAMM,new ArrayList<>(){{add(END_OF_PROGRAMM);}});
        table.put(L,lstL);

        HashMap<DomainTag,ArrayList<DomainTag>> lstA = new HashMap<>();
        lstA.put(AXIOM,new ArrayList<>(){{add(AXIOM);add(NTERM);add(L);}});
        table.put(A,lstA);

        HashMap<DomainTag,ArrayList<DomainTag>> lstN = new HashMap<>();
        lstN.put(NTERM_TOK,new ArrayList<>(){{add(NTERM_TOK);add(NTERM);add(NLST);add(L);}});
        table.put(N,lstN);

        HashMap<DomainTag,ArrayList<DomainTag>> lstNLST = new HashMap<>();
        lstNLST.put(NTERM,new ArrayList<>(){{add(NTERM);add(NLST);}});
        lstNLST.put(LINE,new ArrayList<>(){{add(BLANK);}});
        lstNLST.put(END_OF_PROGRAMM,new ArrayList<>(){{add(BLANK);}});
        table.put(NLST,lstNLST);

        HashMap<DomainTag,ArrayList<DomainTag>> lstT = new HashMap<>();
        lstT.put(TERM_TOK,new ArrayList<>(){{add(TERM_TOK);add(TERM);add(TLST);add(L);}});
        table.put(T,lstT);

        HashMap<DomainTag,ArrayList<DomainTag>> lstTLST = new HashMap<>();
        lstTLST.put(TERM,new ArrayList<>(){{add(TERM);add(TLST);}});
        lstTLST.put(LINE,new ArrayList<>(){{add(BLANK);}});
        lstTLST.put(END_OF_PROGRAMM,new ArrayList<>(){{add(BLANK);}});
        table.put(TLST,lstTLST);

        HashMap<DomainTag,ArrayList<DomainTag>> lstS = new HashMap<>();
        lstS.put(AXIOM,new ArrayList<>(){{add(A);add(N);add(T);add(L);add(R);add(RL);add(LS);add(L);}});
        table.put(S,lstS);
    }

//    public int addName(String name){
//        if(nameCodes.containsKey(name)){
//            return nameCodes.get(name);
//        }else {
//            int code = names.size();
//            names.add(name);
//            nameCodes.put(name,code);
//            return code;
//        }
//    }

    void printResult(ArrayList<ArrayList<DomainTag>> result){
        result.forEach((chain) -> {
            System.out.print(chain.get(0) + " -> ");

            StringBuilder resStr = new StringBuilder();
            for(int i = 1 ; i < chain.size();i++){
                resStr.append(chain.get(i)).append(" ");
            }

            System.out.println(resStr);
        });
    }

    void parse(ArrayList<Token> toks){
        if(toks == null) return;
        ArrayList<ArrayList<DomainTag>> result = new ArrayList<>();
        Iterator<Token> tokens = toks.iterator();
        Stack<DomainTag> stack = new Stack<>();
        Stack<Node> nodes = new Stack<>();
        Node root = new Node(S);
        nodes.push(root);
        stack.push(S);
        Token a = tokens.next();

        do{
            DomainTag x = stack.peek();
            Node n = nodes.peek();
            if(x.isTerm()){
                if(x == a.tag){
                    stack.pop();
                    nodes.pop();
                    n.setToken(a);
                    if(tokens.hasNext()) a = tokens.next();
                }else {
                    System.out.println("Syntax error " + a);
                    return;
                }
            }else{
                if(table.get(x).containsKey(a.tag)){
                        stack.pop();
                        nodes.pop();
                        ArrayList<DomainTag> rule = table.get(x).get(a.tag);
                        if(rule.get(0) != BLANK){
                            for(int i = rule.size() - 1 ; i>=0 ; i--){
                                stack.push(rule.get(i));
                                System.out.print(rule.get(i)+" ");
                            }
                            System.out.println();
                            for (int i = rule.size() - 1 ; i>=0 ; i--) {
                                Node newNode;
                                DomainTag r = rule.get(i);
                                if(r.isTerm()) newNode = new Node(n, r,true);
                                else newNode = new Node(n,r,false);
                                nodes.push(newNode);
                                n.addNode(newNode);
                            }
                        }
                }else {
                    System.out.println("Syntax error " + a);
                    return;
                }
            }
        }while (!stack.empty());
        root.print();
    }

    public String getName(int code){
        return names.get(code);
    }

    public void addMessage(boolean isErr, Position c , String text){
        messages.put(c,new Message(isErr,text));
    }

    public void outputMessages(){
        messages.forEach((p,msg) -> {
            System.out.print(msg.isError ? "Error" : "Warning");
            System.out.print(" " + p + " ");
            System.out.println(msg.text);
        });
    }

    public Scanner getScanner(String prog){
        return new Scanner(prog,this);
    }
}
