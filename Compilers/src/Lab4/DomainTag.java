package Lab4;

import java.util.Arrays;

public enum DomainTag {
    END_OF_PROGRAMM (1),
    IDENT (2),
    NUMBER(3),
    CHAR(4),
    FLOAT(5);

    public int ind;
    DomainTag(int i){
        ind = i;
    }

    public boolean equals(DomainTag ...tags){
        return Arrays.stream(tags).anyMatch(t -> t.ind == ind);
    }
}
