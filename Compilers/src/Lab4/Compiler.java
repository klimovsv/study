package Lab4;

import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.TreeMap;

public class Compiler {
    private TreeMap<Position,Message> messages;
    private HashMap<String,Integer> nameCodes;
    private ArrayList<String> names;

    public Compiler() {
        messages = new TreeMap<>();
        nameCodes = new HashMap<>();
        names = new ArrayList<>();
    }

    public int addName(String name){
        if(nameCodes.containsKey(name)){
            return nameCodes.get(name);
        }else {
            int code = names.size();
            names.add(name);
            nameCodes.put(name,code);
            return code;
        }
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
