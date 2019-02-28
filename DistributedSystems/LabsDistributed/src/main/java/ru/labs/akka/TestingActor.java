package ru.labs.akka;

import akka.actor.AbstractActor;
import akka.actor.ActorRef;
import akka.japi.pf.ReceiveBuilder;

import javax.script.Invocable;
import javax.script.ScriptEngine;
import javax.script.ScriptEngineManager;
import java.util.ArrayList;


public class TestingActor extends AbstractActor {
    private ActorRef storage;

    TestingActor(ActorRef storage){
        this.storage = storage;
    }

    @Override
    public AbstractActor.Receive createReceive(){
        return ReceiveBuilder.create()
                .match(TestPerformerInfo.class, test -> {
                    ScriptEngine engine = new ScriptEngineManager().getEngineByName("nashorn");
                    engine.eval(test.getScript());
                    Invocable invocable = (Invocable) engine;
                    String result = invocable.invokeFunction(test.getFuncName(),test.getTestUnit().getParams().toArray()).toString();
                    boolean passed = result.compareTo(test.getTestUnit().getExpectedResult()) == 0;
                    storage.tell(new StoreTest(test.getTestUnit(),passed,result,test.getPackageId()),ActorRef.noSender());
                })
                .build();
    }
}
