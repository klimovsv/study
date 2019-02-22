package Lab8;

public enum DomainTag {
    NTERM(true),
    NTOK(true),
    TTOK(true),
    TERM(true),
    RTOK(true),
    ASSIGN(true),
    ALTER(true),
    RBRAC(true),
    LBRAC(true),
    LPAREN(true),
    RPAREN(true),
    EPS(true),
    UNEXPECTED(true),
    END_OF_PROGRAMM(true),
    S(false),
    D(false),
    R(false),
    E(false),
    E1(false),
    BRAC(false),
    PAREN(false),
    RULE(false);

    private boolean isTerm;
    DomainTag(boolean isTerm){
        this.isTerm = isTerm;
    }

    public boolean isTerm() {
        return isTerm;
    }
}
