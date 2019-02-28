//package Lab4
//
//object Main {
//  object overload{
//    def push(el:Short, s:SuperStack[Short])(implicit num : Numeric[Short]) : SuperStack[Short] = {
//      if(s.empty()) new SuperStack[Short](s.len+1,(el,el,el)::s.lst)
//      else new SuperStack[Short](s.len+1,(el,num.max(el,s.lst.head._2),num.min(el,s.lst.head._3))::s.lst)
//    }
//
//    def push(el:Long, s:SuperStack[Long])(implicit num : Numeric[Long]) : SuperStack[Long] = {
//      if(s.empty()) new SuperStack[Long](s.len+1,(el,el,el)::s.lst)
//      else new SuperStack[Long](s.len+1,(el,num.max(el,s.lst.head._2),num.min(el,s.lst.head._3))::s.lst)
//    }
//
//
//    def push(el:Double, s:SuperStack[Double])(implicit num : Numeric[Double]) : SuperStack[Double] = {
//      if(s.empty()) new SuperStack[Double](s.len+1,(el,el,el)::s.lst)
//      else new SuperStack[Double](s.len+1,(el,num.max(el,s.lst.head._2),num.min(el,s.lst.head._3))::s.lst)
//    }
//
//    def push(el:Float, s:SuperStack[Float])(implicit num : Numeric[Float]) : SuperStack[Float] = {
//      if(s.empty()) new SuperStack[Float](s.len+1,(el,el,el)::s.lst)
//      else new SuperStack[Float](s.len+1,(el,num.max(el,s.lst.head._2),num.min(el,s.lst.head._3))::s.lst)
//    }
//
//    def push(el:Int, s:SuperStack[Int])(implicit num : Numeric[Int]) : SuperStack[Int] = {
//      if(s.empty()) new SuperStack[Int](s.len+1,(el,el,el)::s.lst)
//      else new SuperStack[Int](s.len+1,(el,num.max(el,s.lst.head._2),num.min(el,s.lst.head._3))::s.lst)
//    }
//
//    def push[T](el: T,s:SuperStack[T]) : SuperStack[T] = {
//      new SuperStack[T](s.len+1,(el,el,el)::s.lst)
//    }
//  }
//
//  object MinMax{
//    implicit class MinMaxStack[T](s: SuperStack[T])(implicit val num : Numeric[T]) {
//      def min(): T = s.lst.head._3
//      def max(): T = s.lst.head._2
//    }
//  }
//
//  def main(args: Array[String]): Unit = {
//    import MinMax._
//    var stack1 = new SuperStack[Int]
//    stack1 = stack1.push(0)
//    stack1 = stack1.push(3)
//    stack1 = stack1.push(2)
//    stack1 = stack1.push(1)
//    println(stack1.min())
//    println(stack1.max())
//    var stack = new SuperStack[Double]
//    stack = stack.push(0.0)
//    stack = stack.push(3.0)
//    stack = stack.push(2.0)
//    stack = stack.push(1.0)
//    println(stack.min())
//    println(stack.max())
//  }
//}
//
//class Facade[T]{
//  this() = new SuperStack[T,Handler[T]]()
//}
//
//import Main.MinMax._
//class SuperStack[T] (val len: Int, val lst : List[(T, T, T)])(implicit h : Handler[T]){
//  def push(el : T) : SuperStack[T] = el match {
//    case _:Int => Main.overload.push(el.asInstanceOf[Int],this.asInstanceOf[SuperStack[Int]]).asInstanceOf[SuperStack[T]]
//    case _:Float => Main.overload.push(el.asInstanceOf[Float],this.asInstanceOf[SuperStack[Float]]).asInstanceOf[SuperStack[T]]
//    case _:Double => Main.overload.push(el.asInstanceOf[Double],this.asInstanceOf[SuperStack[Double]]).asInstanceOf[SuperStack[T]]
//    case _:Long => Main.overload.push(el.asInstanceOf[Long],this.asInstanceOf[SuperStack[Long]]).asInstanceOf[SuperStack[T]]
//    case _:Short => Main.overload.push(el.asInstanceOf[Short],this.asInstanceOf[SuperStack[Short]]).asInstanceOf[SuperStack[T]]
//    case _ => Main.overload.push(el,this)
//  }
//  def this() = this(0,Nil)
//  def pop() : SuperStack[T] = if (empty()) this else new SuperStack[T](len - 1,lst.tail)
//  def head : T =  lst.head._1
//  def empty() : Boolean = len == 0
//}
//
//object Implicits {
//  implicit class HandlerExtenstion[T: Numeric](handler: Handler[T]) {
//    def min = ???
//    def max = ???
//  }
//
//  implicit class SuperStack2[T : Numeric](stack: SuperStack[T, OptimizedHandler[T]]) {
//    def boopa() = ???
//  }
//}
