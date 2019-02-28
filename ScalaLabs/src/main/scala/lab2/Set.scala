package lab2


class Set private (lt:Point,rt:Point,ct:Point,rx:Double,circle:Boolean,inS:List[Set],notIn:List[Set]) {

  val notInSet: List[Set] = notIn
  val inSet: List[Set] = inS match {
    case Nil => this::Nil
    case set => set
  }

  val l: Point = lt
  val r: Point = rt
  val c: Point = ct
  val rad: Double = rx
  val circ: Boolean = circle

  def this(r:Double,c:Point) = this(new Point(),new Point(),c,r,true,Nil,Nil)
  def this(l:Point,r:Point) = this(l,r,new Point(),0,false,Nil,Nil)

  def in(p : Point) : Boolean = inSet.exists(set => inHelp(set,p)) && !notInSet.exists(set => inHelp(set, p))

  def inHelp(set:Set,p:Point) : Boolean= {
    if(set.circ){
      Math.pow(p.x - set.c.x,2) + Math.pow(p.y - set.c.y,2) - Math.pow(set.rad,2) <= 0
    }else{
      p <= set.r && p >= set.l
    }
  }

  def +(set: Set): Set = new Set(lt,rt,ct,rx,circle,set::inSet,notInSet)
  def -(set: Set): Set = new Set(lt,rt,ct,rx,circle,inSet,set::notInSet)
}
