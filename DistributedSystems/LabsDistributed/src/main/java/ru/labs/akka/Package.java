package ru.labs.akka;

import java.util.ArrayList;

public class Package {
    private int packageId;
    private String jsScript;
    private String functionName;
    private ArrayList<TestUnit> tests;


    public int getPackageId() {
        return packageId;
    }

    public void setPackageId(int packageId) {
        this.packageId = packageId;
    }

    public String getJsScript() {
        return jsScript;
    }

    public void setJsScript(String jsScript) {
        this.jsScript = jsScript;
    }

    public String getFunctionName() {
        return functionName;
    }

    public void setFunctionName(String functionName) {
        this.functionName = functionName;
    }

    public ArrayList<TestUnit> getTests() {
        return tests;
    }

    public void setTests(ArrayList<TestUnit> tests) {
        this.tests = tests;
    }
}
