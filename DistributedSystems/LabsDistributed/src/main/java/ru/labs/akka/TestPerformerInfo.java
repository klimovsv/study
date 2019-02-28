package ru.labs.akka;

public class TestPerformerInfo {
    String script;
    String funcName;
    int packageId;
    TestUnit testUnit;

    public TestPerformerInfo(String script, String funcName, int packageId, TestUnit testUnit) {
        this.script = script;
        this.funcName = funcName;
        this.packageId = packageId;
        this.testUnit = testUnit;
    }

    public String getScript() {
        return script;
    }

    public void setScript(String script) {
        this.script = script;
    }

    public String getFuncName() {
        return funcName;
    }

    public void setFuncName(String funcName) {
        this.funcName = funcName;
    }

    public int getPackageId() {
        return packageId;
    }

    public void setPackageId(int packageId) {
        this.packageId = packageId;
    }

    public TestUnit getTestUnit() {
        return testUnit;
    }

    public void setTestUnit(TestUnit testUnit) {
        this.testUnit = testUnit;
    }
}
