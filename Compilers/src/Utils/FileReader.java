package Utils;

import java.io.*;
public class FileReader implements Reader {
    private BufferedReader reader;

    public FileReader(String fileName){
        try {
            File file = new File(fileName);
            reader = new BufferedReader(new InputStreamReader(new FileInputStream(file), "UTF8"));
        }catch (Exception e){
            e.printStackTrace();
        }
    }

    @Override
    public String readLine(){
        try {
            return reader.readLine();
        }catch (Exception e){
            return null;
        }
    }

    @Override
    public String readText(){
        try {
            StringBuilder res = new StringBuilder();
            String str;
            while((str = reader.readLine())!=null){
                res.append(str).append("\n");
            }
            return res.substring(0,res.length()-1);
        }catch (Exception e){
            e.printStackTrace();
            return null;
        }

    }
}
