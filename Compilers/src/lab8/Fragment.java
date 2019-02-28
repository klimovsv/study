package Lab8;

public class Fragment {
    private Position start,follow;
    public Fragment(Position s , Position f){
        start = s;
        follow = f;
    }

    @Override
    public String toString() {
        return start.toString() + "-" + follow.toString();
    }
}
