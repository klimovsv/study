package ru.labs.storm;

import org.apache.storm.task.OutputCollector;
import org.apache.storm.task.TopologyContext;
import org.apache.storm.topology.OutputFieldsDeclarer;
import org.apache.storm.topology.base.BaseRichBolt;
import org.apache.storm.tuple.Tuple;

import java.util.HashMap;
import java.util.Map;

public class CounterBolt extends BaseRichBolt {
    private HashMap<String,Integer> dictionary;
    private OutputCollector outputCollector;

    @Override
    public void prepare(Map map, TopologyContext topologyContext, OutputCollector outputCollector) {
        dictionary = new HashMap<>();
        this.outputCollector = outputCollector;
    }

    @Override
    public void execute(Tuple tuple) {
        if(tuple.getSourceStreamId().equals("sync")){
            printWords();
            dictionary.clear();
            outputCollector.ack(tuple);
        }else{
            String word = (String) tuple.getValue(0);
            dictionary.merge(word, 1, (a, b) -> a + b);
            outputCollector.ack(tuple);
        }
    }

    private void printWords(){
        dictionary.forEach((key, value) -> System.out.println(key + ": " + value));
    }

    @Override
    public void declareOutputFields(OutputFieldsDeclarer outputFieldsDeclarer) {
    }
}
