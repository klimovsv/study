package Lab3

object Main{
  def main(args: Array[String]): Unit = {
    var t = new Token(
      new Pos("(if) () (ifa) (1)) ()()(()12)(443(43))     ) (*dwadadadwafrsfsrgs\nji12791hnja .,aca/*)  *** (*hik"),
      new Scanner
        with SyntaxErr
        with Identifiers
        with Numbers
        with Comments
        with Whitespaces
    )
    while (t.tag != DomainTags.END_OF_PROGRAM) {
      println(t.tag.toString + " " + t.start + "-" + t.follow + ": " + t.image)
      t = t.next
    }
  }
}