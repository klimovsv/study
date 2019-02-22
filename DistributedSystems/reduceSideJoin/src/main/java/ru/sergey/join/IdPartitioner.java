package ru.sergey.join;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Partitioner;

public class IdPartitioner  extends Partitioner<CompositeKey, Text> {
    @Override
    public int getPartition(CompositeKey key, Text value,  int numReduceTasks) {
        return key.getId()  % numReduceTasks;
    }

}