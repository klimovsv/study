package ru.labs.storm;

import org.apache.storm.spout.SpoutOutputCollector;
import org.apache.storm.task.TopologyContext;
import org.apache.storm.topology.IRichSpout;
import org.apache.storm.topology.OutputFieldsDeclarer;
import org.apache.storm.topology.base.BaseRichSpout;
import org.apache.storm.tuple.Fields;
import org.apache.storm.tuple.Values;
import com.google.common.io.Files;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.nio.charset.Charset;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

public class LinesSpout extends BaseRichSpout implements IRichSpout {
    private ConcurrentHashMap<UUID,Values> map;
    public static final String SRC = "src";
    public static final String DEST = "dest";
    private SpoutOutputCollector spoutOutputCollector;
    private File destDir;
    private File srcDir;
    private File currFile;
    private STATE state;
    private BufferedReader reader;
    private int ackCount = 0;


    private enum STATE{
        WAITINGFILE,
        READING,
        WAITINGACKS,
        WAITTOMOVE
    }

    @Override
    public void open(Map map, TopologyContext topologyContext, SpoutOutputCollector spoutOutputCollector) {
        this.spoutOutputCollector = spoutOutputCollector;
        srcDir = new File((String)map.get(SRC));
        destDir = new File((String)map.get(DEST));
        state = STATE.WAITINGFILE;
        this.map = new ConcurrentHashMap<>();
    }

    @Override
    public void nextTuple(){
        try{
            if(state == STATE.WAITINGFILE){
                File[] files = srcDir.listFiles();
                if(files != null && files.length > 0){
                    currFile = files[0];
                    state = STATE.READING;
                    reader = new BufferedReader(new InputStreamReader(new FileInputStream(currFile), Charset.forName("utf-8")));
                }
            }
            String line = "";
            if(state == STATE.READING){
                line = reader.readLine();
                if(line != null){
                    ackCount++;
                    UUID msId = UUID.randomUUID();
                    Values tuple = new Values(line);
                    map.put(msId,tuple);
                    spoutOutputCollector.emit("lines",tuple,msId);
                }else {
                    state = STATE.WAITINGACKS;
                }
            }
            if(state == STATE.WAITINGACKS && ackCount == 0) {
                ackCount++;
                spoutOutputCollector.emit("sync", new Values("sync"),UUID.randomUUID());
                state = STATE.WAITTOMOVE;
            }
            if(state == STATE.WAITTOMOVE && ackCount == 0){
                File destFile = new File(destDir.getAbsolutePath()+"/"+currFile.getName());
                Files.move(currFile,destFile);
                state = STATE.WAITINGFILE;
            }
        }catch (Exception e){
            e.printStackTrace();
        }
    }

    @Override
    public void ack(Object msgId) {
        ackCount--;
        map.remove((UUID)msgId);
    }

    @Override
    public void fail(Object msgId){
        spoutOutputCollector.emit("lines",map.get((UUID) msgId),(UUID)msgId);
    }

    @Override
    public void declareOutputFields(OutputFieldsDeclarer outputFieldsDeclarer) {
        outputFieldsDeclarer.declareStream("lines",new Fields("line"));
        outputFieldsDeclarer.declareStream("sync",new Fields("command"));
    }
}
