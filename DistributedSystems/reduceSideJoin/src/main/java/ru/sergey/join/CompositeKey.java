package ru.sergey.join;

import org.apache.hadoop.io.WritableComparable;

import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;

public class CompositeKey implements WritableComparable<CompositeKey>{
    private Integer id;
    private Integer source;

    public Integer getId(){
        return id;
    }

    public CompositeKey(){}

    public CompositeKey(int id, int source){
        this.id = id;
        this.source = source;
    }

    @Override
    public String toString(){
        return (new StringBuilder().append(id).append('\t').append(source)).toString();
    }

    @Override
    public int hashCode(){
        return toString().hashCode();
    }

    @Override
    public int compareTo(CompositeKey o) {
        if (id.equals(o.id)){
            return id.compareTo(o.id);
        }else{
            return source.compareTo(o.source);
        }
    }

    @Override
    public boolean equals(Object obj) {
        if (!(obj instanceof CompositeKey)){
            return false;
        }

        CompositeKey key = (CompositeKey)obj;
        return source.equals(key.source) && id.equals(key.id);
    }

    @Override
    public void write(DataOutput dataOutput) throws IOException {
        dataOutput.writeInt(id);
        dataOutput.writeInt(source);
    }

    @Override
    public void readFields(DataInput dataInput) throws IOException {
        id = dataInput.readInt();
        source = dataInput.readInt();
    }
}
