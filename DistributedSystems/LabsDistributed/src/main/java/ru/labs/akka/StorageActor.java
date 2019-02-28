package ru.labs.akka;

import akka.actor.AbstractActor;
import akka.japi.pf.ReceiveBuilder;

import java.util.ArrayList;
import java.util.HashMap;

public class StorageActor extends AbstractActor{
    private final HashMap<Integer,ArrayList<StoreTest>> storage = new HashMap<>();


    private ArrayList<String> getTests(int packageId){
        ArrayList<StoreTest> tests = storage.get(packageId);
        ArrayList<String> res = new ArrayList<>();
        if(tests==null){
            res.add("nothing");
            //return "nothing";
            return res;
        }
        String result="packageid " + packageId +"";
        res.add(result);
        for (StoreTest test:tests){
            result += test.info();
            res.add(test.info());
        }
        return res;
        //return result;
    }

    @Override
    public Receive createReceive(){
        return ReceiveBuilder.create()
                .match(StoreTest.class,test -> {
                    System.out.println("starting storage " + test.getPackageId() + " " + test.getTestUnit().getTestName());
                    int id =test.getPackageId();
                    ArrayList<StoreTest> list = storage.get(id);
                    if(list==null){
                        list = new ArrayList<>();
                        storage.put(id,list);
                    }
                    list.add(test);
                    System.out.println("stored");
                })
                .match(Integer.class,id -> {
                    sender().tell(getTests(id),self());
                })
                .build();
    }
}
