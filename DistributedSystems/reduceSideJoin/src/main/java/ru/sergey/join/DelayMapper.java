package ru.sergey.join;

import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import java.io.IOException;

public class DelayMapper extends Mapper<LongWritable, Text, CompositeKey, Text> {


    private static final int CANCELLED_COLUMN = 19;
    private static final int DEST_AIRPORT_COLUMN = 14;
    private static final int DELAY_COLUMN = 18;

    @Override
    protected void map(LongWritable key, Text value, Mapper.Context context) throws IOException, InterruptedException {
        String line = value.toString();
        String words[] = line.split("[,]");

        String airportId = words[DEST_AIRPORT_COLUMN];
        if (airportId.compareTo("\"DEST_AIRPORT_ID\"") == 0) {
            return;
        }

        String cancelled = words[CANCELLED_COLUMN];
        String delayNew = words[DELAY_COLUMN];
        int nmb = Integer.parseInt(airportId);

        if(checkCancellationAndDelay(delayNew,cancelled)) {
            return;
        }

        context.write(new CompositeKey(nmb,1),new Text(delayNew));
    }

    private boolean checkCancellationAndDelay(String delay,String cancel){
        return (parse(cancel) == 1  || delay.length() == 0 || parse(delay) == 0 );
    }

    private int parse(String str){
        return (int) Double.parseDouble(str);
    }
}
