//
//class Circle[T] (val x : T, val y: T ,val r : T)(implicit val num : Numeric[T]){
//  def inside[B : Numeric](other : Circle[B]) : Boolean= {
//    val r1 = num.toDouble(r)
//    val r2 = implicitly[Numeric[B]].toDouble(other.r)
//    val x1 = num.toDouble(x)
//    val x2 = implicitly[Numeric[B]].toDouble(other.x)
//    val y1 = num.toDouble(y)
//    val y2 = implicitly[Numeric[B]].toDouble(other.y)
//    Math.sqrt(Math.pow(x1-x2,2) + Math.pow(y1-y2,2)) + r1 <= r2
//  }
//}
//
//object Main {
//
//  trait Area[T]
//  object Area{
//    implicit class AreaCircle[T](circle: Circle[T])(implicit val a: Area[T],implicit val num : Numeric[T]) {
//      def area() : T = (Math.pow(num.toDouble(circle.r),2) * Math.PI).asInstanceOf[T]
//      def per() : T = (2 * Math.PI * num.toDouble(circle.r)).asInstanceOf[T]
//    }
//    implicit object float extends Area[Float]
//    implicit object double extends Area[Double]
//  }
//
////  def main(args: Array[String]): Unit = {
////        import Area._
////        val cint = new Circle[Int](0,0,1)
////        val cFloat = new Circle[Float](0,0,2)
////        println(cFloat.per())
////        println(cFloat.area())
////        println(cint.inside(cFloat))
////        println(cFloat.inside(cint))
////  }
//}