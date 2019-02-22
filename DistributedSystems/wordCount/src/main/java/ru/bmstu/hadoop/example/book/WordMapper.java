package ru.bmstu.hadoop.example.book;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;



import java.io.IOException;

public class WordMapper extends Mapper<LongWritable, Text, Text, IntWritable> {
    @Override
    protected void map(LongWritable key, Text value, Mapper.Context context) throws IOException, InterruptedException {
        String[] words = value.toString().toLowerCase().replaceAll("[^a-zа-я]"," ").split("\\s");
        for (String word : words) {
            context.write(new Text(word), new IntWritable(1));
        }
    }
}