package ru.sergey.join;

import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.Reducer;

import java.io.IOException;

public class JoinReducer extends Reducer<CompositeKey, Text, Text, Text> {
    @Override
    protected void reduce(CompositeKey key, Iterable<Text> values, Context context)throws IOException, InterruptedException{
        String airportName = "";
        int i = 0, sum = 0, min = Integer.MAX_VALUE, max = Integer.MIN_VALUE;

        for(Text v : values){
            if (i == 0 ){
                airportName = v.toString();
            }else{
                int delay = (int)Double.parseDouble(v.toString());
                sum += delay;
                if ( min > delay){
                    min = delay;
                }
                if ( max < delay){
                    max = delay;
                }
            }
            i++;
        }
        float avg = (float) sum / (i-1);
        if ( i > 1) {
            context.write(new Text(airportName),new Text(String.valueOf(min) + '\t' + max + '\t' + avg));
        }
    }
}