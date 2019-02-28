package Lab7;

abstract class Token {
    DomainTag tag;
    private Fragment frag;
    Token(DomainTag tag, Position s, Position f) {
        this.tag = tag;
        this.frag = new Fragment(s,f);
    }

    abstract String getAttr();

    @Override
    public String toString() {
        return tag + " " + frag + ": " + getAttr();
    }

    public boolean isTerm(){
        return tag.isTerm();
    }

    public DomainTag getTag() {
        return tag;
    }
}

class SpecToken extends Token {
    private String value;
    @Override
    String getAttr() {
        return value;
    }
    SpecToken(DomainTag tag, Position s, Position f,String value) {
        super(tag, s, f);
        this.value = value;
    }
}