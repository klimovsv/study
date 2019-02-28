package Lab8;

import java.util.function.IntPredicate;

public class Position implements Comparable<Position>{
    private String text;
    private int line,col,index;

    public Position(String text) {
        this(text, 0, 1, 1);
    }

    private Position(String text, int index, int line, int col) {
        this.text = text;
        this.index = index;
        this.line = line;
        this.col = col;
    }

    @Override
    public int compareTo(Position o) {
        return Integer.compare(index, o.index);
    }

    public int getChar() {
        return !endText() ? text.codePointAt(index) : -1;
    }

    public boolean satisfies(IntPredicate p) {
        return p.test(getChar());
    }

    public String sub(Position pos){
        return text.substring(index,pos.getIndex());
    }

    public int getIndex() {
        return index;
    }

    public Position skip() {
        int c = getChar();
        switch (c) {
            case -1:
                return this;
            case '\n':
                return new Position(text, index+1, line+1, 1);
            default:
                return new Position(text, index + (c > 0xFFFF ? 2 : 1), line, col+1);
        }
    }

    private boolean endText(){
        return index == text.length();
    }

    public boolean isWhiteSpace(){
        return !endText() && satisfies(Character::isWhitespace);
    }

    public boolean isLetter(){
        return !endText() && satisfies(Character::isLetter);
    }

    public boolean isLetterOrDigit(){
        return !endText() && satisfies(Character::isLetterOrDigit);
    }

    public boolean isDigit(){
        return !endText() && satisfies(Character::isDigit);
    }

    public Position skipWhile(IntPredicate p) {
        Position pos = this;
        while (pos.satisfies(p)) pos = pos.skip();
        return pos;
    }

    public String toString() {
        return String.format("(%d, %d)", line, col);
    }

}
