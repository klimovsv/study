package ru.sergey.spark.test;

import org.apache.spark.api.java.function.Function;
import org.apache.spark.api.java.function.PairFunction;
import org.apache.spark.broadcast.Broadcast;
import scala.Tuple2;

import java.util.Map;

class Utils {
    private static final int CODE_COLUMN = 1;
    private static final int AIRPORT_NAME_COLUMN = 3;
    private static final int CANCELLED_COLUMN = 19;
    private static final int DEST_AIRPORT_COLUMN = 14;
    private static final int DELAY_COLUMN = 18;
    private static final int ORIGIN_AIRPORT_COLUMN = 11;


    static PairFunction<String, Tuple2<Integer,Integer> , FlightInfo> getFlightMapper(){
        return  (line) -> {
            String words[] = line.split("[,]");

            String destAirport = words[DEST_AIRPORT_COLUMN];

            if (destAirport.compareTo("\"DEST_AIRPORT_ID\"") == 0) {
                return new Tuple2<>(new Tuple2<>(-1,-1),new FlightInfo());
            }

            String originAirport = words[ORIGIN_AIRPORT_COLUMN];
            String cancelled = words[CANCELLED_COLUMN];
            String delayNew = words[DELAY_COLUMN];

            int destAirportId = Integer.parseInt(destAirport);
            int originAirportId = Integer.parseInt(originAirport);

            return new Tuple2<>(new Tuple2<>(originAirportId , destAirportId),new FlightInfo(getDelay(delayNew) , parseToInt(cancelled)));
        };
    }

    private static int getDelay(String delay) {
        return delay.length() == 0 ? 0 : parseToInt(delay);
    }

    private static int parseToInt(String str){
        return (int) Double.parseDouble(str);
    }

    static PairFunction<String, Integer, String> getAirportMapper() {
        return (line) -> {

            String words[] = line.split("[\"]");

            if(words.length == 1 ) {
                return new Tuple2<>(-1,"default");
            }

            int nmb = Integer.parseInt(words[CODE_COLUMN]);

            return new Tuple2<>(nmb,words[AIRPORT_NAME_COLUMN]);
        };
    }

    static Function<Tuple2<Tuple2<Integer, Integer>, FlightInfo> , String> flightsToString(Broadcast<Map<Integer, String>> broadcast) {
        return (entry) -> {
            Map<Integer, String> airports = broadcast.value();
            String airportName = airports.get(entry._1()._2());
            FlightInfo info = entry._2();
            return airportName + info.toString();
        };
    }
}
