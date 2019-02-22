import Main.Handler
import Main.Handler.{numPush, push}

object Main {
  trait Handler[T]{
    def push(el : T,s : SuperStack[T]): SuperStack[T]
  }
   object Handler{

     class numPush[T]()(implicit num: Numeric[T]) extends Handler[T]{
       def push(el: T,s:SuperStack[T]): SuperStack[T] = {
         if(s.empty()) new SuperStack[T](s.len+1,(el,el,el)::s.lst)(this)
         else new SuperStack[T](s.len+1,(el,num.max(el,s.lst.head._2),num.min(el,s.lst.head._3))::s.lst)(this)
       }
     }

     class push[T]() extends Handler[T]{
       def push(el: T,s:SuperStack[T]): SuperStack[T] = {
         if(s.empty()) new SuperStack[T](s.len+1,(el,el,el)::s.lst)(this)
         else new SuperStack[T](s.len+1,(el,el,el)::s.lst)(this)
       }
     }

     implicit def pushToNumPush[T](p: push[T])(implicit num: Numeric[T]): numPush[T] = new numPush[T]()(num)
   }



  object MinMax{
    implicit class MinMaxStack[T](s: SuperStack[T])(implicit val num : Numeric[T]) {
      def min(): T = s.lst.head._3
      def max(): T = s.lst.head._2
    }
  }

  def main(args: Array[String]): Unit = {
    import MinMax._
    import Main.Handler.push
    var stack = new SuperStack[Int](0,Nil)(new numPush[Int])
    stack = stack.push(0)
    stack = stack.push(3)
    stack = stack.push(2)
    stack = stack.push(1)
    println(stack.min())
    println(stack.max())
//    stack = stack.push("ab")
//    println(stack.head)
  }
}

class SuperStack[T] (val len: Int, val lst : List[(T, T, T)])(implicit val handler : Handler[T]){
//  def this() = this(0,Nil)(new numPush[T])
  def push(el : T) : SuperStack[T] = handler.push(el,this)
  def pop() : SuperStack[T] = if (empty()) this else new SuperStack[T](len - 1,lst.tail)
  def head : T =  lst.head._1
  def empty() : Boolean = len == 0
}
