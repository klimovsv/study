package Lab7;

import Utils.FileReader;

public class Main {
    public static void main(String ...args){
        Compiler c = new Compiler();
        FileReader reader = new FileReader(args[0]);
        Scanner sc = c.getScanner(reader.readText());
        c.parse(sc.scan());
    }
}
