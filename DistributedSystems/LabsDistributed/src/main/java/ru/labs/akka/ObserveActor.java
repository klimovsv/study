package ru.labs.akka;

import akka.actor.*;
import akka.japi.pf.ReceiveBuilder;
import akka.routing.RoundRobinPool;

import java.util.ArrayList;

public class ObserveActor extends AbstractActor {
    private ArrayList<ActorRef> testers;
    private ActorRef storage;
    private ActorRef testPerformer;

    ObserveActor(){
        storage = getContext().actorOf(Props.create(StorageActor.class));
        testPerformer = getContext().actorOf(
                new RoundRobinPool(15).props(
                        Props.create(TestingActor.class,storage)
                ),
                "testingActor"
        );
    }

    @Override
    public Receive createReceive(){
        return ReceiveBuilder.create()
                .match(Package.class, pckg -> {
                    ArrayList<TestUnit> tests = pckg.getTests();
                    for(TestUnit test:tests){
                        testPerformer.tell(new TestPerformerInfo(
                                pckg.getJsScript(),
                                pckg.getFunctionName(),
                                pckg.getPackageId(),
                                test),ActorRef.noSender());
                    }
                })
                .match(Integer.class, id -> {
                    storage.forward(id,getContext());
                })
                .build();
    }
}
