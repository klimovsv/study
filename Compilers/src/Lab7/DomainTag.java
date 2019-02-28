package Lab7;

import java.util.Arrays;

public enum DomainTag {
    BLANK(true),
    END_OF_PROGRAMM (true),
    AXIOM(true) ,
    NTERM(true),
    TERM(true),
    NTERM_TOK(true),
    TERM_TOK(true),
    LINE(true),
    RULE(true),
    ASSIGN(true),
    EPS(true),
    UNEXPECTED(true),
    LS(false),
    RL(false),
    R(false),
    TAIL(false),
    LST(false),
    LST1(false),
    L(false),
    A(false),
    N(false),
    NLST(false),
    T(false),
    TLST(false),
    S(false);

    private boolean isTerm;
    DomainTag(boolean isTerm){
        this.isTerm = isTerm;
    }

    public boolean isTerm() {
        return isTerm;
    }
}
