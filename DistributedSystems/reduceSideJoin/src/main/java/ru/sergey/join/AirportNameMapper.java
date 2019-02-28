package ru.sergey.join;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.WritableComparable;
import org.apache.hadoop.mapreduce.Mapper;

import java.io.IOException;

public class AirportNameMapper extends Mapper<LongWritable, Text, CompositeKey, Text> {

    private static final int CODE_COLUMN = 1;
    private static final int AIRPORT_NAME_COLUMN = 3;

    @Override
    protected void map(LongWritable key, Text value, Mapper.Context context) throws IOException, InterruptedException {
        String line = value.toString();
        String words[] = line.split("[\"]");

        if(words.length == 1 ) {
            return;
        }

        int nmb = Integer.parseInt(words[CODE_COLUMN]);

        context.write(new CompositeKey(nmb,0),new Text(words[AIRPORT_NAME_COLUMN]));
    }
}
