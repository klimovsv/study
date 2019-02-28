package Lab3
class Pos private ( val prog : String , val offs : Int , val line : Int , val col : Int ) {
  def this(prog : String ) = this(prog , 0, 1, 1)
  def ch = if ( offs == prog.length ) -1 else prog(offs).toInt
  def inc = ch match {
    case '\n' => new Pos ( prog , offs +1 , line +1 , 1)
    case -1 => this
    case _ => new Pos ( prog , offs +1 , line , col +1)
  }
  override def toString = "(" + line + " , " + col + ")"
}

object DomainTags extends Enumeration {
  type Tag = Value
  val WHITESPACE ,IDENT,NUMBER,RESERVED,COMMENT,SYNTAX_ERROR, END_OF_PROGRAM = Value
}
import DomainTags._

class Scanner {
  def scan ( start : Pos ): ( Tag , Pos ) = sys.error(" syntax error at " + start )
}

class Token ( val start : Pos , scanner : Scanner ) {
  val (tag, follow) = start.ch match {
    case -1 => (END_OF_PROGRAM, start)
    case _ => scanner.scan(start)
  }

  def image = start.prog.substring(start.offs, follow.offs)
  def next = new Token(follow, scanner)
}

trait Whitespaces extends Scanner {
  private def missWhitespace ( pos : Pos ): Pos = pos.ch match {
    case ' ' => missWhitespace(pos.inc)
    case '\t' => missWhitespace(pos.inc)
    case '\n' => missWhitespace(pos.inc)
    case _ => pos
  }

  override def scan ( start : Pos ) = {
    val follow = missWhitespace(start)
    if ( start != follow ) ( WHITESPACE , follow )
    else super.scan(start)
  }
}

trait Identifiers extends Scanner{
  val ifRes : String = "(if)"

  private def skip(cur : Pos):Pos = cur.ch match {
    case '(' => skip(cur.inc)
    case ')' => skip(cur.inc)
    case c if c >= 'a' && c<='z' || c>='A' && c<='Z' => skip(cur.inc)
    case _ => cur
  }

  override def scan ( start : Pos ) = {
    val follow  = skip(start)
    if (start != follow && ifRes == start.prog.substring(start.offs, follow.offs)) (RESERVED , follow)
    else if (start != follow) ( IDENT , follow )
    else super.scan(start)
  }
}

trait Numbers extends Scanner{
  val reserved : String = "()"

  private def skip(cur : Pos,start :Pos,parenNmb:Int):Pos = cur.ch match {
    case '(' => skip(cur.inc,start,parenNmb + 1)
    case ')' if parenNmb > 0 => skip(cur.inc,start,parenNmb - 1)
    case ')' => cur
    case c if (c >= '0') && (c <= '9')=> skip(cur.inc,start,parenNmb)
    case _ if parenNmb == 0 => cur
    case _ => start
  }

  override def scan ( start : Pos ) = {
    val follow = skip(start,start,0)
    if ( start != follow && reserved == start.prog.substring(start.offs,follow.offs)) ( RESERVED , follow )
    else if (start != follow) (NUMBER , follow)
    else super.scan(start)
  }
}

trait Comments extends Scanner{
  def q5(cur: Pos, start: Pos) = cur.ch match {
    case ')' => cur.inc
    case -1 => start
    case _ => q3(cur.inc,start)
  }

  def q3(cur: Pos, start: Pos): Pos = cur.ch match {
    case '*' => q5(cur.inc,start)
    case -1 => start
    case _ => q3(cur.inc,start)
  }

  def q2(cur: Pos, start: Pos) = cur.ch match {
    case '*' => q5(cur.inc,start)
    case -1 => start
    case _ => q3(cur.inc,start)
  }

  def q1(cur: Pos, start: Pos) = cur.ch match {
    case '*' => q2(cur.inc,start)
    case _ => start
  }

  def q0(cur: Pos, start: Pos) = cur.ch match {
    case '(' => q1(cur.inc,start)
    case _ => start
  }

  override def scan(start : Pos ) = {
    val follow = q0(start,start)
    if ( start != follow ) ( COMMENT , follow )
    else super.scan(start)
  }
}

trait SyntaxErr extends Scanner{
  private def skip(pos: Pos) : Pos = pos.ch match {
    case c if c==' ' || c=='\n' || c== -1 || c=='\t' => pos
    case _ => skip(pos.inc)
  }

  override def scan ( start : Pos ) = {
    val follow = skip(start)
    if ( start != follow ) ( SYNTAX_ERROR , follow )
    else super.scan(start)
  }
}