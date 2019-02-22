package com.spark;


import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaPairRDD;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;
import scala.Tuple2;

import java.util.ArrayList;
import java.util.Map;

import static java.lang.Double.parseDouble;
import static java.lang.Integer.parseInt;

public class App {
    public static void main(String []args) throws Exception {
        SparkConf conf= new SparkConf().setAppName("Lab4");
        JavaSparkContext sc = new JavaSparkContext(conf);
        JavaRDD<String> flights = sc.textFile("/flights.csv");
        JavaRDD<String> airports =sc.textFile("/airports.csv");
        JavaPairRDD<Integer, String> mapAirports=airports.mapToPair(App::airportMapper);
        JavaPairRDD<Integer, Integer> airportsPair=flights.mapToPair(App::flightsMapper);
        mapAirports.collect();
    }
    public static Tuple2<Map<Integer, Integer>, Map<Integer, Integer>> flightsMapper(String value) {
        String[] words=value.split("\"");
        if (words.length == 1) {
            return new Tuple2<>(null, null);
        } else return new Tuple2<>(parseInt(words[11]), parseInt(words[14]), (int)parseDouble(words[18]), (int)parseDouble(words[19]));
    }
    public static Tuple2<Integer,String> airportMapper(String value) {
        if (value != "Code,Description") {
            String[] words = value.split("\"");
            return new Tuple2<>(parseInt(words[1]), words[3]);
        } else return new Tuple2<>(null, null);
    }
}