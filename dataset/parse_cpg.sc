import scala.io.Source

@main def exec(cpgFile: String, functionList: String, outDir: String) = {
    importCpg(inputPath=cpgFile, projectName=cpgFile)
    run.ossdataflow
    val functions = Source.fromFile(functionList).getLines.toList
    for (function <- functions) {
        if (!(cpg.method(function).dotCpg14.l.isEmpty)) {
            cpg.method(function).dotCpg14.toJson |> (outDir + "/" + function + ".json")
        }
    }
}