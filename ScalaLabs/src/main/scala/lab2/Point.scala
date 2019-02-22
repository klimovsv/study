package lab2
class Point(xs:Double,ys:Double){
  val x: Double = xs
  val y: Double = ys
  def this() = this(0,0)
  def in(set:Set): Boolean = set in this
  def <(p:Point): Boolean = this.x < p.x && this.y < p.y
  def <=(p:Point): Boolean = this < p || this == p
  def ==(p:Point): Boolean = this.x == p.x && this.y == p.y
  def >=(p:Point): Boolean = this > p || this == p
  def >(p: Point): Boolean = this.x > p.x && this.y > p.y

  override def toString: String = s"x: $x y: $y"
}
