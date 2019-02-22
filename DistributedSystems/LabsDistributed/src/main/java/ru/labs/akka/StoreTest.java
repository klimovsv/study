package ru.labs.akka;

public class StoreTest{
    private TestUnit testUnit;
    private boolean passed;
    private int packageId;
    private String result;


    public String info(){
        return testUnit.getTestName() + " params " + testUnit.getParams().toString() + " expected "
                + testUnit.getExpectedResult() + " result " + result + " passed " + passed;
    }

    StoreTest(TestUnit testUnit,boolean passed,String result,int id){
        this.passed = passed;
        this.testUnit = testUnit;
        this.result = result;
        this.packageId = id;
    }

    public void setTestUnit(TestUnit testUnit) {
        this.testUnit = testUnit;
    }

    public void setPassed(boolean passed) {
        this.passed = passed;
    }

    public void setPackageId(int packageId) {
        this.packageId = packageId;
    }

    public String getResult() {
        return result;
    }

    public void setResult(String result) {
        this.result = result;
    }

    public boolean isPassed() {
        return passed;
    }

    public TestUnit getTestUnit() {
        return testUnit;
    }

    public int getPackageId() {
        return packageId;
    }
}
