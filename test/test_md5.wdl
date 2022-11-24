version 1.0

task CalcMd5 {
  input {
    File input_file
    String hi=     "hi"
  }

  command {
    /bin/my_md5sum2 ${input_file}
    echo hi ; echo this is a command too
  }

 output {
    File value = "md5sum.txt"
    File value2 = "blah.txt"
 }

 runtime {
   docker: "quay.io/briandoconnor/dockstore-tool-md5sum:1.0.2"
   cpu: 1
   memory: "512 MB"
 }
}
