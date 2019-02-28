package ru.labs.akka;

import akka.NotUsed;
import akka.actor.Actor;
import akka.actor.ActorRef;
import akka.actor.ActorSystem;
import akka.actor.Props;
import akka.http.javadsl.ConnectHttp;
import akka.http.javadsl.Http;
import akka.http.javadsl.ServerBinding;
import akka.http.javadsl.marshallers.jackson.Jackson;
import akka.http.javadsl.model.HttpRequest;
import akka.http.javadsl.model.HttpResponse;
import akka.http.javadsl.server.AllDirectives;
import akka.http.javadsl.server.Route;
import akka.pattern.Patterns;
import akka.stream.ActorMaterializer;
import akka.stream.javadsl.Flow;
import akka.util.Timeout;
import scala.concurrent.Future;
import scala.concurrent.duration.Duration;

import java.util.concurrent.CompletionStage;

public class Main extends AllDirectives{
    public static void main(String... args) throws Exception{
        ActorSystem system = ActorSystem.create("TestintApp");
        ActorRef observer = system.actorOf(Props.create(ObserveActor.class));
        final Http http = Http.get(system);
        final ActorMaterializer materialize = ActorMaterializer.create(system);
        Main main = new Main();
        final Flow<HttpRequest, HttpResponse, NotUsed> routeFlow = main.route(observer).flow(system, materialize);
        final CompletionStage<ServerBinding> binding = http.bindAndHandle(routeFlow,
                ConnectHttp.toHost("localhost", 8080), materialize);

        System.out.println("Server online at http://localhost:8080/ \n Press RETURN to stop...");
        System.in.read();
        binding
                .thenCompose(ServerBinding::unbind)
                .thenAccept(unbound -> system.terminate());
    }

    private Route route(ActorRef observer){
        return route(
                path("post",() ->
                        post(()->
                            entity(Jackson.unmarshaller(Package.class), pckg ->{
                                observer.tell(pckg, ActorRef.noSender());
                                return complete("posting tests");
                            }))
                        ),
                path("get",()->
                        get(() -> parameter("packageId",(packageId) -> {
                            int id = Integer.parseInt(packageId);
                            Timeout timeout = new Timeout(Duration.create(5, "seconds"));
                            Future<Object> future = Patterns.ask(observer, id , timeout);
                            return completeOKWithFuture(future, Jackson.marshaller());
                        })))
        );
    }
}
