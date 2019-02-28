package Lab8;

import java.util.ArrayList;
import java.util.HashSet;

public class Node {
    DomainTag tag;
    Token tok = null;
    ArrayList<Node> nodes = new ArrayList<>();



    Node(DomainTag tag){
        this.tag = tag;
    }

    Node(Token tok){
        this.tok = tok;
        this.tag = tok.tag;
    }

    void addNode(Node node){
        nodes.add(node);
    }

    void printTree(){this.printTree(0);}


    HashSet<String> getFirst(Compiler compiler){
        HashSet<String> set = new HashSet<>();
        if(tag == DomainTag.RULE){
            for(int i = 3 ; i < nodes.size() ; i++){
                set.addAll(nodes.get(i).getFirst(compiler));
            }

            return set;
        }else if(tag == DomainTag.E){
            int i = 0;
            while(true){
                Node node = nodes.get(i);

                if(node.tag == DomainTag.TERM){
                    set.add(node.tok.getAttr());
                }else if(node.tag == DomainTag.NTERM){
                    set.addAll(compiler.getFirsts().get(node.tok.getAttr()));
                }else if(node.tag == DomainTag.BRAC){
                    set.add("e");
                    set.addAll(node.nodes.get(0).getFirst(compiler));
                }else if(node.tag == DomainTag.PAREN){
                    set.addAll(node.nodes.get(0).getFirst(compiler));
                }

                if(set.contains("e") && i!= nodes.size() - 1){
                    set.remove("e");
                    i++;
                }else {
                    return set;
                }
            }
        } else if (tag == DomainTag.E1){
            nodes.forEach((node -> {
                set.addAll(node.getFirst(compiler));
            }));
        }
        return set;
    }


    void printTree(int recLvl){
        for(int i = 0 ; i < recLvl ; i++) System.out.print("-");
        if(tok!= null) System.out.println(tok);
        else System.out.println(tag);
        for(Node node:nodes){
            node.printTree(recLvl+1);
        }
//        nodes.forEach(Node::printTree);
    }
}
