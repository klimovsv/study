package Lab3;

import Utils.FileReader;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Lexer {
    private static final String ident = "([a-zA-Z][a-zA-Z0-9]*)";
    private static final String variable = "([ste]([.][a-zA-Z0-9]+|[0-9a-zA-Z](?=([^0-9a-zA-Z]))))";
    private static final String pattern = "(?<VAR>"+variable+")|(?<IDENT>"+ident+")";
    private static final Pattern p = Pattern.compile(pattern);

    public static void main(String... args){
        FileReader reader = new FileReader(args[0]);
        int lineNmb = 1;
        String str;
        try {
            while ((str = reader.readLine())!=null){
                match(str,lineNmb);
                lineNmb++;
            }
        }catch (Exception e){
            e.printStackTrace();
        }
    }

    private static int skipWhile(int pos,String text){
        while(pos < text.length() && text.substring(pos,pos+1).matches("\\s")) {
            pos++;
        }
        return pos;
    }

    public static void match(String text,int stringNmb)
    {
        int pos = 0;
        Matcher m = p.matcher(text);
        pos = skipWhile(pos,text);
        while(m.find(pos)){
            if (m.start()!=pos) {
                System.out.printf("syntax error(%d,%d)\n", stringNmb, pos + 1);
            }

            if(m.group("IDENT") != null){
                System.out.println("IDENT ( " + stringNmb + "," + (m.start()+1) + " ) : " + m.group("IDENT"));
            }else{
                System.out.println("VAR ( " + stringNmb + "," + (m.start()+1) + " ) : " + m.group("VAR"));
            }

            pos = m.end();
            pos = skipWhile(pos,text);
        }
        if(pos != text.length()){
            System.out.printf("syntax error(%d,%d)\n", stringNmb,pos+1 );
        }
    }
}
