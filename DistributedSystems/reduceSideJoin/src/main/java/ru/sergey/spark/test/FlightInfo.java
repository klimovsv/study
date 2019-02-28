package ru.sergey.spark.test;

import java.io.Serializable;

class FlightInfo implements Serializable{
    private int maxDelay;
    private int nmbFlights;
    private int delayed;
    private int cancelled;

    FlightInfo(){}

    FlightInfo(int delay, int cancelled){
        this.maxDelay = delay;
        this.delayed = delay != 0 ? 1 : 0;
        this.cancelled = cancelled;
        this.nmbFlights = 1;
    }

    private FlightInfo(int delay, int cancelled, int delayedNmb, int flights){
        this.maxDelay = delay;
        this.cancelled = cancelled;
        this.delayed = delayedNmb;
        this.nmbFlights = flights;
    }

    FlightInfo add(FlightInfo flight){
        int newMaxDelay = maxDelay > flight.maxDelay ? maxDelay : flight.maxDelay;
        int newNmbFlights = nmbFlights + flight.nmbFlights;
        int newDelayed = delayed + flight.delayed;
        int newCancelled = cancelled + flight.cancelled;
        return new FlightInfo(newMaxDelay,newCancelled,newDelayed,newNmbFlights);
    }

    @Override
    public String toString() {
        return "\n\t percent of delayed : " + getPercentage(delayed,nmbFlights)
                + "\n\t percent of cancelled : " + getPercentage(cancelled,nmbFlights)
                + "\n\t max delay : " + maxDelay;
    }

    private int getPercentage(int nmb , int maxValue){
        return (int)(((float)nmb/maxValue) * 100);
    }
}
