package ru.labs.akka;

import java.util.ArrayList;

public class TestUnit {
    private String testName;
    private String expectedResult;
    private ArrayList<Integer> params;

    public String getTestName() {
        return testName;
    }

    public void setTestName(String testName) {
        this.testName = testName;
    }

    public String getExpectedResult() {
        return expectedResult;
    }

    public void setExpectedResult(String expectedResult) {
        this.expectedResult = expectedResult;
    }

    public ArrayList<Integer> getParams() {
        return params;
    }

    public void setParams(ArrayList<Integer> params) {
        this.params = params;
    }
}
