
import sbt._
import Keys._

object Root extends Build {

  lazy val root = Project(
    id = "root",
    base = file("."),
    aggregate = Seq(clustering)
  )

  lazy val clustering = Project(
    id = "clustering",
    base = file("clustering")
  )

}
