package ru.sergey.spark.test;
import org.apache.spark.api.java.JavaPairRDD;
import org.apache.spark.api.java.JavaSparkContext;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.SparkConf;
import org.apache.spark.broadcast.Broadcast;
import scala.Tuple2;

import java.io.Serializable;
import java.util.Arrays;
import java.util.Map;

public class App implements Serializable{
    public static void main(String[] args) throws Exception{
        SparkConf conf = new SparkConf().setAppName("app");
        JavaSparkContext sc = new JavaSparkContext(conf);
        JavaRDD<String> flights = sc.textFile("info.csv");
        JavaPairRDD<Tuple2<Integer, Integer>, FlightInfo> mapedFlights= flights.mapToPair(Utils.getFlightMapper());
        JavaPairRDD<Tuple2<Integer, Integer>, FlightInfo> reducedFlights = mapedFlights.reduceByKey(FlightInfo::add);

        JavaRDD<String> airports = sc.textFile("airports.csv");
        JavaPairRDD<Integer, String> mappedAirports = airports.mapToPair(Utils.getAirportMapper());
        final Broadcast<Map<Integer, String>> airportsBroadcasted = sc.broadcast(mappedAirports.collectAsMap());

        JavaRDD<String> resultFlights = reducedFlights.map(Utils.flightsToString(airportsBroadcasted));
        resultFlights.saveAsTextFile("result3");
        Arrays.stream(resultFlights.collect().toArray()).forEach(System.out::println);
    }
}
