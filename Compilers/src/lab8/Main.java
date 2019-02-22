package Lab8;

import Utils.FileReader;

public class Main {
    public static void main(String ...args){
        Compiler c = new Compiler();
        FileReader reader = new FileReader(args[0]);
        c.getScanner(reader.readText());
        try {
            c.parse();
        }catch (TokenException e){
            System.out.println(e.getMessage());
        }
    }
}
