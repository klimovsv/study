package ru.sergey.join;


import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.MultipleInputs;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;


public class App {
    public static void main(String[] args) throws Exception{
        if (args.length != 3) {
            System.err.println("Usage: <input path> <input path 2> <output path>");
            System.exit(-1);
        }
        Job job = Job.getInstance();
        job.setJarByClass(App.class);
        job.setJobName("JoinJob sort");
        MultipleInputs.addInputPath(job, new Path(args[0]), TextInputFormat.class, AirportNameMapper.class);
        MultipleInputs.addInputPath(job, new Path(args[1]), TextInputFormat.class, DelayMapper.class);

        FileOutputFormat.setOutputPath(job, new Path(args[2]));
        job.setPartitionerClass(IdPartitioner.class);
        job.setGroupingComparatorClass(GroupingIdComparatorClass.class);
        job.setReducerClass(JoinReducer.class);
        job.setMapOutputKeyClass(CompositeKey.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);
        job.setNumReduceTasks(2);
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
