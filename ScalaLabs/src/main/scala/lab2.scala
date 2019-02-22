
//object Main {
//  def main(args: Array[String]): Unit = {
//    val foo = new Num(2.7,5.4)
//    val foo1 = new Num(3.6, 1.1)
//    val sum = foo + foo1
//    val mul = foo * 3
//    println("num1: " + foo.toString+", num2: "+foo1.toString + "\nsum: " + sum.toString)
//    println("foo < fool : " + (foo < foo1))
//  }
//}
class Num(ax:Double, kx:Double) {
  val a: Double = ax
  val k: Double = kx
  def +(n: Num): Num ={
    new Num(this.a+n.a, this.k+n.k)
  }
  def *(c: Double): Num ={
    new Num( c * this.a, c * this.k)
  }
  def <(num: Num): Boolean = {
    this.a < num.a || ((this.a == num.a) && (this.k < num.k))
  }
  override def toString: String = s"$a + ${k}δ"
}

