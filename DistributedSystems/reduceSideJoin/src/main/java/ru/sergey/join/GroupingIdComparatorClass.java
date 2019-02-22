package ru.sergey.join;

import org.apache.hadoop.io.WritableComparable;
import org.apache.hadoop.io.WritableComparator;

public class GroupingIdComparatorClass extends WritableComparator {
    public GroupingIdComparatorClass(){
        super(CompositeKey.class,null,true);
    }

    @Override
    public int compare(WritableComparable a, WritableComparable b) {
        CompositeKey obj1 = (CompositeKey)a;
        CompositeKey obj2 = (CompositeKey)b;
        return obj1.getId().compareTo(obj2.getId());
    }
}
