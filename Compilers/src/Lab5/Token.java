package Lab5;


class Token {
    DomainTag tag;
    private Fragment frag;
    private String value;

    Token(DomainTag tag, Position s, Position f,String value) {
        this.tag = tag;
        this.frag = new Fragment(s,f);
        this.value = value;
    }

    @Override
    public String toString() {
        return tag + " " + frag + ": " + value;
    }

    public DomainTag getTag() {
        return tag;
    }
}