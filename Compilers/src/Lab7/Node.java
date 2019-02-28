package Lab7;

import java.util.ArrayList;

public class Node {
    private boolean leaf;
    private Node parent;
    private DomainTag tag;
    private Token token;
    private int level;
    private ArrayList<Node> childs = new ArrayList<>();

    Node(DomainTag tag){
        parent = this;
        level = 0;
        this.tag = tag;
    }

    void print(){
        for(int i = 0 ; i < level ; i++){
            System.out.print("-");
        }
        if(isLeaf()){
            System.out.println(token);
        }
        else{
            System.out.println(tag);
            for(int i = childs.size()-1 ; i>=0 ; i--){
                childs.get(i).print();
            }
        }
    }

    void addNode(Node node){
        childs.add(node);
    }

    Node(Node parent,DomainTag tag,boolean leaf){
        this.parent = parent;
        this.tag = tag;
        this.leaf = leaf;
        level = parent.level + 1;
    }

    void setToken(Token tok){
        token = tok;
    }


    public boolean isLeaf(){
        return leaf;
    }

    public boolean isRoot(){
        return parent == this;
    }
}
