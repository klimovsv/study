package ru.labs.storm;

import org.apache.storm.Config;
import org.apache.storm.LocalCluster;
import org.apache.storm.topology.TopologyBuilder;
import org.apache.storm.tuple.Fields;

public class Main {
    private static final String LINESGENERATOR = "files";
    private static final String SPLITTER = "splitter";
    private static final String COUNTER = "counter";


    static public void main(String... args){
        TopologyBuilder builder = new TopologyBuilder();
        builder.setSpout(LINESGENERATOR,new LinesSpout());
        builder.setBolt(SPLITTER,new SplitterBolt(),10)
                .shuffleGrouping(LINESGENERATOR,"lines");
        builder.setBolt(COUNTER,new CounterBolt(),10)
                .fieldsGrouping(SPLITTER,new Fields("word"))
                .allGrouping(LINESGENERATOR,"sync");
        Config config = new Config();
        config.put(LinesSpout.DEST,"destDir");
        config.put(LinesSpout.SRC,"srcDir");
        config.setDebug(false);
        config.put(Config.TOPOLOGY_MAX_SPOUT_PENDING,50);
        LocalCluster cluster = new LocalCluster();
        cluster.submitTopology("count",config,builder.createTopology());
    }
}
