//object Main {
//  def main(args: Array[String]): Unit = {
//
//  }
//}
//
//class Pos private ( val prog : String , val offs : Int , val line : Int , val col : Int ) {
//   def this(prog : String ) = this(prog , 0, 1, 1)
//   def ch = if ( offs == prog.length ) -1 else prog(offs).toInt
//   def inc = ch match {
//    case '\n' => new Pos ( prog , offs +1 , line +1 , 1)
//    case -1 => this
//    case _ => new Pos ( prog , offs +1 , line , col +1)
//   }
//   override def toString = "(" + line + " , " + col + ")"
//}
//
//object DomainTags extends Enumeration {
//   type Tag = Value
//   val WHITESPACE ,IDENT,NUMBER,RESERVED,COMMENT, END_OF_PROGRAM = Value
//}
// import DomainTags ._
//
// class Scanner {
//   def scan ( start : Pos ): ( Tag , Pos ) = sys.error (" syntax error at " + start )
// }
//
// class Token ( val start : Pos , scanner : Scanner ) {
//   val (tag, follow) = start.ch match {
//     case -1 => (END_OF_PROGRAM, start)
//     case _ => scanner.scan(start)
//   }
//
//   def image = start.prog.substring(start.offs, follow.offs)
//   def next = new Token(follow, scanner)
// }
//
//trait Whitespaces extends Scanner {
//   private def missWhitespace ( pos : Pos ): Pos = pos.ch match {
//    case ' ' => missWhitespace(pos.inc)
//    case '\t' => missWhitespace(pos.inc)
//    case '\n' => missWhitespace(pos.inc)
//    case _ => pos
//   }
//
//   override def scan ( start : Pos ) = {
//     val follow = missWhitespace(start)
//     if ( start != follow ) ( WHITESPACE , follow )
//     else super.scan(start)
//     }
//   }
//
////trait Identifiers extends Scanner{
////  private def skip(start : Pos) = {
////
////  }
////
////  override def scan ( start : Pos ) = {
////    val follow = skip(start)
////    if ( start != follow ) ( IDENT , follow )
////    else super.scan(start)
////  }
////}
////
//trait Numbers extends Scanner{
//  private def skip(start :Pos) :Pos = start.ch match {
//    case c if (c >= '0') && (c <= '9') => skip(start.inc)
//    case _ => start
//  }
//
//  private def skipMinus(start : Pos) = start.ch match {
//    case '-' => skip(start.inc)
//    case c if (c >= '0') && (c <= '9')=> skip(start)
//    case _ => start
//  }
//
//  override def scan ( start : Pos ) = {
//    val follow = skipMinus(start)
//    if ( start != follow ) ( NUMBER , follow )
//    else super.scan(start)
//  }
//}
//
//
//trait Comments extends Scanner{
//  private def skip(pos: Pos) : Pos = pos.ch match {
//    case -1 => pos
//    case '\n' => pos
//    case _ => skip(pos.inc)
//  }
//  private def skipMinus(start : Pos, next :Pos ,i :Int) : Pos= {
//    case (`start`, `next`, 2) => skip(next)
//    case (`start`, `next`, `i`) if (2 > i) && (next.ch == '-')=> skipMinus(start,next.inc,i+1)
//    case (`start`, `next`, `i`) => start
//  }
//
//  override def scan ( start : Pos ) = {
//    val follow = skipMinus(start,start,0)
//    if ( start != follow ) ( COMMENT , follow )
//    else super.scan(start)
//  }
//}
////
////trait Reserved extends Scanner{
////  private def skip(start : Pos) = {
////
////  }
////
////  override def scan ( start : Pos ) = {
////    val follow = skip(start)
////    if ( start != follow ) ( RESERVED , follow )
////    else super.scan(start)
////  }
////}