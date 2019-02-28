package lab2
  object Main {
    def main(args: Array[String]): Unit = {
      val rectTop = new Set(new Point(-3,1),new Point(3,2))
      val rectBot = new Set(new Point(-3,-2),new Point(3,-1))
      val centCircle = new Set(2,new Point(0,0))
      val unionAll = rectBot+rectTop+centCircle
      val diffBot = unionAll - rectBot
      val diffTop = unionAll - rectTop
      val diffTopBot = diffBot - rectTop
      val diffCirc = unionAll - centCircle
      val p1 = new Point(-1,0)
      val p2 = new Point(0,1.5)
      val p3 = new Point(-2.5,1.5)

      println()
      println(unionAll)
      println(diffBot)
      println()

      println("printing for p1")
      println(s"unionall ${p1 in unionAll}")
      println(s"diffCirc ${p1 in diffCirc}")
      println(s"diffTop  ${p1 in diffTop}")
      println(s"diffBot  ${p1 in diffBot}")
      println(s"diffTopBot  ${p1 in diffTopBot}")



      println("printing for p2")
      println(s"unionall ${p2 in unionAll}")
      println(s"diffCirc ${p2 in diffCirc}")
      println(s"diffTop  ${p2 in diffTop}")
      println(s"diffBot  ${p2 in diffBot}")
      println(s"diffTopBot  ${p2 in diffTopBot}")


      println("printing for p3")
      println(s"unionall ${p3 in unionAll}")
      println(s"diffCirc ${p3 in diffCirc}")
      println(s"diffTop  ${p3 in diffTop}")
      println(s"diffBot  ${p3 in diffBot}")
      println(s"diffTopBot  ${p3 in diffTopBot}")


    }
  }

