package Lab8;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;

public class State {
    private HashMap<String,Integer> firsts = new HashMap<>();

    State(HashMap<String,HashSet<String>> firsts){
        firsts.forEach((rule,set)-> this.firsts.put(rule,set.size()));
    }

    @Override
    public boolean equals(Object obj) {
        State newState = (State) obj;
        HashMap<String,Integer> newFirsts = newState.firsts;
        for(Map.Entry<String,Integer> entry : newFirsts.entrySet()){
            if(!entry.getValue().equals(firsts.get(entry.getKey()))) return false;
        }
        return true;
    }
}
