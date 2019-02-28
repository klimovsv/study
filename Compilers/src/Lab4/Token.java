package Lab4;

abstract class Token {
    DomainTag tag;
    private Fragment frag;
    Token(DomainTag tag, Position s, Position f) {
        this.tag = tag;
        this.frag = new Fragment(s,f);
    }

    abstract String getAttr(Scanner sc);

    @Override
    public String toString() {
        return tag + " " + frag + ": ";
    }
}

class IdentToken extends Token {
    private int code;

    @Override
    String getAttr(Scanner sc) {
        return sc.getCompiler().getName(code);
    }

    IdentToken(Position s, Position f, int code) {
        super(DomainTag.IDENT, s, f);
        this.code = code;
    }
}

class NumberToken extends Token {
    private long value;

    @Override
    String getAttr(Scanner sc) {
        return ""+value;
    }
    NumberToken(Position s, Position f, long value) {
        super(DomainTag.NUMBER, s, f);
        this.value = value;
    }
}

class FloatNumberToken extends Token {
    private String value;

    @Override
    String getAttr(Scanner sc) {
        return value;
    }
    FloatNumberToken(Position s, Position f, String value) {
        super(DomainTag.FLOAT, s, f);
        this.value = value;
    }
}

class SpecToken extends Token{
    @Override
    String getAttr(Scanner sc) {
        return "";
    }
    SpecToken(DomainTag tag, Position s, Position f) {
        super(tag, s, f);
    }
}